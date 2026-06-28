#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for step in [['python3','scripts/fetch_market_data.py'],['python3','scripts/run_moa_brief.py'],['python3','scripts/run_business_ops.py'],['python3','scripts/render_site.py']]:
    print('\n$ '+' '.join(step),flush=True)
    r=subprocess.run(step,cwd=str(ROOT),text=True,capture_output=True,timeout=480)
    print(r.stdout)
    if r.stderr: print(r.stderr,file=sys.stderr)
    if r.returncode: sys.exit(r.returncode)
print('\nOtto Margin Desk cycle complete.')
