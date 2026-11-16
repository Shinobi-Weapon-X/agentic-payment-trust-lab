"""Regenerate frozen fictional CSVs and model benchmark outputs."""
from pathlib import Path
import json, sys
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.payments import generate_payments, classify_dataset, evaluate_holdout, sha256_file, AGENTS, SUPPLIERS, SCENARIOS


def main():
    df = generate_payments()
    classified = classify_dataset(df)
    holdout, report = evaluate_holdout(df)
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'artifacts').mkdir(exist_ok=True)
    classified.to_csv(ROOT/'data'/'fictional_payment_proposals.csv',index=False)
    holdout.to_csv(ROOT/'artifacts'/'holdout_predictions.csv',index=False)
    report['sha256_proposals_csv'] = sha256_file(ROOT/'data'/'fictional_payment_proposals.csv')
    report['sha256_holdout_csv'] = sha256_file(ROOT/'artifacts'/'holdout_predictions.csv')
    report['scenario_counts']={k:int(v[0]) for k,v in SCENARIOS.items()}
    report['policy_design'] = 'BLOCK for invalid mandate, account, amount, scope, duplicate or injection. HOLD for missing approval, pending bank change and risk-based enhanced review. No real execution.'
    (ROOT/'artifacts'/'evaluation_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k in ['total_synthetic_proposals','test_proposals','unsafe_holdout','legitimate_holdout','policy','anomaly_model','policy_false_hold_rate_legitimate','policy_legitimate_straight_through','scripted_unsafe_value_intervened_sgd','holdout_policy_outcomes']}, indent=2))

if __name__=='__main__': main()
