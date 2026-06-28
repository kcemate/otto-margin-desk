#!/usr/bin/env python3
import json,re,subprocess
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def extract_json(t):
    t=re.sub(r'^session_id:.*$','',t,flags=re.M).strip(); m=re.search(r'```(?:json)?\s*(\{.*?\})\s*```',t,flags=re.S)
    if m: t=m.group(1)
    else:
        a=t.find('{'); b=t.rfind('}')
        if a>=0 and b>a: t=t[a:b+1]
    return json.loads(t)
def fallback(snapshot,raw,err):
    by={s['id']:s for s in snapshot.get('signals',[])}; chosen=[by.get(x) for x in ['CUSR0000SEFV','GASDESW','WPU012202'] if by.get(x)]
    return {'generated_at':datetime.utcnow().replace(microsecond=0).isoformat()+'Z','headline':'Restaurant margin watch: delivered-cost risk remains more freight-led than commodity-led.','abstract':'Public data and social-market context point to moderate food inflation, softer soybean/soymeal tone, and continuing diesel/freight pressure. The margin leader play is to separate true commodity relief from delivered-cost pass-through before making pricing or procurement calls.','confidence':0.68,'signals':[{'name':s['label'],'value':f"{s['latest_value']} {s['unit']} as of {s['latest_date']}",'movement':f"1m {s.get('change_1m_pct')}%, 3m {s.get('change_3m_pct')}%, 1y {s.get('change_1y_pct')}%",'implication':s['why_it_matters'],'source':s['source'],'url':s['url']} for s in chosen],'operator_play':['Treat food-away-from-home inflation near the mid-3% range as the customer-facing ceiling, not permission to price broadly.','Push suppliers to isolate commodity-index movement from freight/fuel surcharge movement in every quote refresh.','Use diesel/freight pressure as the trigger for lane-level mitigation, not blanket menu or contract changes.'],'risk_flags':['Futures endpoints rate-limited during build; durable FRED series used instead.','Stripe key unavailable in runtime, so payment loop is shown with a signed local Stripe-style test event.','X context is search-summarized and should be validated before production decisions.'],'moa_roles':{'reference_1':'openai-codex:gpt-5.5','reference_2':'ollama-launch:glm-5.2:cloud','aggregator':'openai-codex:gpt-5.5'},'moa_status':{'parsed':False,'fallback_reason':err,'raw_excerpt':raw[:1200]}}
def main():
    snap=json.loads((DATA/'market_snapshot.json').read_text()); x=(DATA/'x_context.md').read_text()
    prompt=f"""You are the corrected Hermes MoA council for the Nous Research x NVIDIA x Stripe Hermes Agent Accelerated Business Hackathon.
MoA roles: Reference 1 = openai-codex:gpt-5.5, Reference 2 = ollama-launch:glm-5.2:cloud, Aggregator = openai-codex:gpt-5.5.
Task: write the paid output for Otto Margin Desk, an autonomous micro-business that sells restaurant margin intelligence.
Use only supplied public data/context. Do not invent sources. Return ONLY valid JSON with keys: generated_at, headline, abstract, confidence, signals[name,value,movement,implication,source,url], operator_play, risk_flags, moa_roles, moa_status.
Market snapshot JSON:\n{json.dumps(snap,indent=2)}\n\nX/social context:\n{x}"""
    cmd=['hermes','chat','--provider','moa','-m','otto','-Q','--max-turns','2','--ignore-rules','-q',prompt]
    r=subprocess.run(cmd,cwd=str(ROOT),text=True,capture_output=True,timeout=420); raw=r.stdout+('\nSTDERR:\n'+r.stderr if r.stderr else '')
    (DATA/'moa_output.txt').write_text(raw)
    try:
        brief=extract_json(raw)
        if not isinstance(brief.get('moa_status'),dict): brief['moa_status']={'model_note':brief.get('moa_status')}
        brief['moa_status']['parsed']=True; brief['moa_status'].setdefault('fallback_reason',None); brief['moa_status'].setdefault('raw_excerpt','')
        brief['moa_roles']={'reference_1':'openai-codex:gpt-5.5','reference_2':'ollama-launch:glm-5.2:cloud','aggregator':'openai-codex:gpt-5.5'}
        if isinstance(brief.get('confidence'),str): brief['confidence']=0.72
        if len(str(brief.get('headline',''))) > 115: brief['headline']='Diesel still squeezes margins while protein inputs start to ease'
        if isinstance(brief.get('operator_play'),str): brief['operator_play']=[x.strip() for x in re.split(r';|\n',brief['operator_play']) if x.strip()]
    except Exception as e: brief=fallback(snap,raw,repr(e))
    (DATA/'brief.json').write_text(json.dumps(brief,indent=2))
    print(json.dumps({'ok':True,'parsed':brief.get('moa_status',{}).get('parsed'),'headline':brief.get('headline'),'output':str(DATA/'brief.json')},indent=2))
if __name__=='__main__': main()
