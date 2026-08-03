#!/usr/bin/env python3
import argparse, json, sys
STATUS={'明确违反','疑似风险','信息不足','通过'}; RISK={'低','中','高','严重'}
REQUIRED={'finding_id','location','excerpt','summary','status','risk','confidence','citations','reason','recommendation','annotated','human_review'}
def validate(report):
    errors=[]
    for i,f in enumerate(report.get('findings',[])):
        missing=REQUIRED-set(f)
        if missing: errors.append(f'finding {i} missing: {sorted(missing)}')
        if f.get('status') not in STATUS: errors.append(f'finding {i} invalid status')
        if f.get('risk') not in RISK: errors.append(f'finding {i} invalid risk')
        if f.get('status') != '通过' and not f.get('citations'): errors.append(f'finding {i} needs citations')
    return errors
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('report'); a=ap.parse_args(); errs=validate(json.load(open(a.report,encoding='utf-8')))
    print('\n'.join(errs)); sys.exit(bool(errs))
