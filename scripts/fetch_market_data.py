#!/usr/bin/env python3
import csv,json,statistics,urllib.request
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
SERIES={
 'GASDESW':('U.S. No. 2 Diesel Retail Price','$/gal','FRED GASDESW','https://fred.stlouisfed.org/series/GASDESW','Proxy for delivered-cost pressure in trucking and refrigerated distribution.'),
 'WPU012202':('PPI: Soybeans','index','FRED WPU012202','https://fred.stlouisfed.org/series/WPU012202','Feed/input proxy that can affect protein economics.'),
 'CPIUFDSL':('CPI: Food','index','FRED CPIUFDSL','https://fred.stlouisfed.org/series/CPIUFDSL','Broad consumer food inflation pressure.'),
 'CUSR0000SEFV':('CPI: Food Away From Home','index','FRED CUSR0000SEFV','https://fred.stlouisfed.org/series/CUSR0000SEFV','Restaurant pricing pressure and margin pass-through proxy.')}
SEED_LIVE_OBSERVED={
 'GASDESW':('2026-06-22',4.832),
 'WPU012202':('2026-05-01',185.55),
 'CPIUFDSL':('2026-05-01',348.892),
 'CUSR0000SEFV':('2026-05-01',394.728)}
def summarize_seed(sid,meta,error):
    label,unit,source,url,why=meta; d,v=SEED_LIVE_OBSERVED[sid]
    return {'id':sid,'label':label,'unit':unit,'source':source,'url':url,'why_it_matters':why,'latest_date':d,'latest_value':v,'previous_value':None,'change_vs_previous_pct':None,'change_1m_pct':None,'change_3m_pct':None,'change_1y_pct':None,'recent_min':v,'recent_max':v,'recent_avg':v,'fallback_from_live_probe':True,'fallback_reason':repr(error)}
def fetch(sid):
    url=f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}'
    last_error=None
    for attempt in range(1):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            txt=urllib.request.urlopen(req,timeout=8).read().decode()
            out=[]
            for r in csv.DictReader(txt.splitlines()):
                v=r.get(sid,'.')
                if v and v!='.': out.append((datetime.strptime(r['observation_date'],'%Y-%m-%d'),float(v)))
            return out
        except Exception as e:
            last_error=e
    raise last_error
def prior(rows,days):
    target=rows[-1][0].timestamp()-days*86400; p=None
    for d,v in rows:
        if d.timestamp()<=target: p=(d,v)
        else: break
    return p
def pc(a,b): return None if not b else round((a-b)/b*100,2)
def summarize(sid,meta):
    label,unit,source,url,why=meta; rows=fetch(sid); d,v=rows[-1]; prev=rows[-2]; m=prior(rows,31); q=prior(rows,92); y=prior(rows,366); recent=[x for _,x in rows[-12:]]
    return {'id':sid,'label':label,'unit':unit,'source':source,'url':url,'why_it_matters':why,'latest_date':d.date().isoformat(),'latest_value':round(v,4),'previous_value':round(prev[1],4),'change_vs_previous_pct':pc(v,prev[1]),'change_1m_pct':pc(v,m[1]) if m else None,'change_3m_pct':pc(v,q[1]) if q else None,'change_1y_pct':pc(v,y[1]) if y else None,'recent_min':round(min(recent),4),'recent_max':round(max(recent),4),'recent_avg':round(statistics.mean(recent),4)}
def main():
    DATA.mkdir(parents=True,exist_ok=True); signals=[]; errors=[]
    for sid,meta in SERIES.items():
        try: signals.append(summarize(sid,meta))
        except Exception as e:
            errors.append({'series':sid,'error':repr(e),'fallback':'live_observed_seed'})
            signals.append(summarize_seed(sid,meta,e))
    snap={'generated_at':datetime.utcnow().replace(microsecond=0).isoformat()+'Z','source_type':'public economic time series','signals':signals,'errors':errors,'notes':['Yahoo Finance futures endpoint returned 429 during build, so FRED is the durable no-key public data layer.','X/social context is stored in data/x_context.md from X Search summaries.']}
    (DATA/'market_snapshot.json').write_text(json.dumps(snap,indent=2))
    print(json.dumps({'ok':True,'signals':len(signals),'errors':errors,'output':str(DATA/'market_snapshot.json')},indent=2))
if __name__=='__main__': main()
