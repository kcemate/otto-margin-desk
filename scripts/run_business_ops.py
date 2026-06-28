#!/usr/bin/env python3
import hashlib,hmac,json,os,time,urllib.parse,urllib.request
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; PRICE=300; LOCAL_DEMO_SIGNING_SALT='not-a-real-secret-demo-salt'
def now(): return datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
def stripe_api(path,payload,key):
    req=urllib.request.Request('https://api.stripe.com'+path,data=urllib.parse.urlencode(payload).encode(),method='POST')
    req.add_header('Authorization','Bearer '+key); req.add_header('Content-Type','application/x-www-form-urlencoded')
    return json.loads(urllib.request.urlopen(req,timeout=30).read().decode())
def payment_link():
    key=os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_API_KEY') or ''
    if key.startswith('sk_test_'):
        product=stripe_api('/v1/products',{'name':'Otto Margin Desk - Daily Brief'},key)
        price=stripe_api('/v1/prices',{'product':product['id'],'unit_amount':str(PRICE),'currency':'usd'},key)
        link=stripe_api('/v1/payment_links',{'line_items[0][price]':price['id'],'line_items[0][quantity]':'1','metadata[agent]':'otto-margin-desk'},key)
        return {'mode':'stripe_test_live_api','payment_link':link.get('url'),'product_id':product.get('id'),'price_id':price.get('id'),'payment_link_id':link.get('id')}
    if key.startswith('sk_live_'): return {'mode':'blocked_live_key','payment_link':None,'reason':'Live Stripe key detected; creation blocked without explicit approval.'}
    return {'mode':'local_stripe_style_test_event','payment_link':None,'reason':'No Stripe test secret in runtime; using signed local checkout.session.completed event.'}
def main():
    brief=json.loads((DATA/'brief.json').read_text()); pay=payment_link()
    event={'id':'evt_otto_demo_'+str(int(time.time())),'type':'checkout.session.completed','created':int(time.time()),'livemode':False,'data':{'object':{'id':'cs_test_otto_margin_desk','amount_total':PRICE,'currency':'usd','customer_email':'buyer@example.com','metadata':{'brief_headline':brief.get('headline','')[:120]}}}}
    event['local_signature']=hmac.new(LOCAL_DEMO_SIGNING_SALT.encode(),json.dumps(event,sort_keys=True).encode(),hashlib.sha256).hexdigest()
    costs=[('MoA council synthesis',-42),('Public-source scouting / X Search',-8),('Static hosting allocation',-2)]
    entries=[{'type':'revenue','label':'Daily brief checkout','amount_cents':PRICE,'source':event['id'],'timestamp':now()}]+[{'type':'spend','label':l,'amount_cents':a,'approved_by':'policy:max_cycle_spend_100c','timestamp':now()} for l,a in costs]+[{'type':'reserve','label':'Reinvested into next scout cycle','amount_cents':-50,'approved_by':'policy:retain_positive_balance','timestamp':now()}]
    ledger={'generated_at':now(),'business':'Otto Margin Desk','price_cents':PRICE,'currency':'usd','payment':pay,'safety_limits':{'max_spend_per_cycle_cents':100,'live_spend_requires_human_approval':True,'public_data_only':True},'stripe_event':event,'entries':entries,'balance_cents':sum(e['amount_cents'] for e in entries),'gross_margin_cents_before_reinvestment':PRICE+sum(a for _,a in costs),'delivery_status':'prepared'}
    (DATA/'ledger.json').write_text(json.dumps(ledger,indent=2))
    delivery=f"# Buyer delivery payload\n\n**{brief.get('headline')}**\n\n{brief.get('abstract')}\n\n## Margin leader play\n"+''.join('- '+x+'\n' for x in brief.get('operator_play',[]))+"\n## Signals\n"+''.join(f"- **{s.get('name')}**: {s.get('value')} ({s.get('movement')}). {s.get('implication')} Source: {s.get('source')}\n" for s in brief.get('signals',[]))+f"\nDelivered by Otto Margin Desk. Payment/event: `{event['id']}`.\n"
    (DATA/'delivery_payload.md').write_text(delivery)
    print(json.dumps({'ok':True,'payment_mode':pay['mode'],'balance_cents':ledger['balance_cents'],'ledger':str(DATA/'ledger.json')},indent=2))
if __name__=='__main__': main()
