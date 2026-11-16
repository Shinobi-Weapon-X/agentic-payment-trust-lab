"""Project 05 - Agentic Payment Trust Lab (fictional, offline, no funds movement)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.payments import AGENTS, SUPPLIERS, policy_gate, audit_record, contains_prompt_injection, sha256_file

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'fictional_payment_proposals.csv'
HOLDOUT = ROOT / 'artifacts' / 'holdout_predictions.csv'
MANIFEST = ROOT / 'artifacts' / 'evaluation_manifest.json'
CASESTUDY = ROOT / 'docs' / 'PROJECT_CASE_STUDY.pdf'

st.set_page_config(page_title='Agentic Payment Trust Lab | Project 05', page_icon='💳', layout='wide')
st.markdown('''<style>
.block-container {max-width: 1370px; padding-top:1.6rem; padding-bottom:3rem;}
h1,h2,h3 {letter-spacing: -.025em;}
[data-testid="stMetric"] {background:#14253D; border:1px solid #28425C; padding:14px 18px; border-radius:14px;}
[data-testid="stMetricLabel"] {color:#9AC5CD;}
[data-testid="stTabs"] button {font-weight:600;}
a {color:#72E7D3!important;}
.labeyebrow {font-size:.84rem; font-weight:700; letter-spacing:.12em; color:#6CE0CF; text-transform:uppercase;}
.labintro {color:#BDCCDB; max-width:980px; font-size:1.04rem;}
.labnote {background:#14253D; padding:14px 17px; border-left:3px solid #56DFC9; border-radius:8px; margin:1.2rem 0;}
hr {border-color:#294459!important;}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_all():
    frame = pd.read_csv(DATA)
    hold = pd.read_csv(HOLDOUT)
    report = json.loads(MANIFEST.read_text(encoding='utf-8'))
    return frame, hold, report

proposals, test_set, metrics = load_all()
for k,v in {'revoked':set(), 'audit':[], 'settled':set()}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def selected_event(prompt: str, key: str, frame: pd.DataFrame) -> pd.Series:
    options = frame['proposal_id'].astype(str).tolist()
    scenario_by_id = dict(zip(options, frame['scenario'].astype(str)))
    choice = st.selectbox(prompt, options, key=key, format_func=lambda x: f"{x}  ·  {scenario_by_id[x].replace('_',' ').title()}")
    return frame.loc[frame.proposal_id.eq(choice)].iloc[0]

def show_outcome(p: pd.Series):
    gate = policy_gate(p, st.session_state.revoked)
    typ = gate['outcome']
    if typ=='ALLOW': st.success('ALLOW  |  Fictional proposal passes configured preventive rules')
    elif typ=='HOLD': st.warning('HOLD  |  No payment may proceed until approved evidence and independent checks are revalidated')
    else: st.error('BLOCK  |  Fictional payment proposal prohibited')
    st.markdown(f"**Rule** `{gate['rule_id']}`  ·  **Explanation** {gate['explanation']}")
    return gate

def event_summary(p: pd.Series):
    cols = st.columns(4)
    cols[0].metric('Proposed amount', f"SGD {float(p.amount_sgd):,.2f}")
    cols[1].metric('Delegated limit', f"SGD {float(p.mandate_limit_sgd):,.0f}")
    cols[2].metric('Agent', str(p.agent_id))
    cols[3].metric('Supplier', str(p.supplier_id))
    with st.expander('Inspect fictional invoice and approval evidence', expanded=False):
        st.json({k: (bool(p[k]) if k in ('buyer_approved','already_paid','mandate_active') else str(p[k])) for k in ['invoice_id','approval_reference','buyer_approved','beneficiary_account','beneficiary_status','already_paid','mandate_active','invoice_note']})
        st.caption('Invoice text is treated as untrusted data. It is never passed to an agent, API or tool executor.')

def session_csv():
    cols = ['timestamp_utc','event_type','proposal_id','invoice_id','agent_id','amount_sgd','policy_outcome','policy_rule','reviewer','decision','rationale','provenance','real_payment_executed']
    return pd.DataFrame(st.session_state.audit, columns=cols).to_csv(index=False).encode('utf8')

st.markdown('<div class="labeyebrow">Project 05 · Responsible AI Engineering Portfolio</div>',unsafe_allow_html=True)
st.title('💳 Agentic Payment Trust Lab')
st.markdown('<p class="labintro">Can a delegated AI payment agent process approved supplier invoices efficiently while independent safeguards prevent unauthorised transactions, detect anomalous behaviour and preserve accountable human decisions?</p>',unsafe_allow_html=True)
st.info('**Educational simulation only.** Every agent, supplier, invoice, beneficiary and payment is fictional. There are no payment APIs, credentials, live AI agents or real funds transfers. A simulated settlement is a browser-session event, not a transaction.')

k1,k2,k3,k4 = st.columns(4)
k1.metric('Synthetic proposals',f"{len(proposals):,}")
k2.metric('Holdout proposals',f"{len(test_set):,}")
k3.metric('Fictional agent mandates',str(len(AGENTS)))
k4.metric('Currency simulated','SGD')

with st.sidebar:
    st.markdown('### Project 05')
    st.caption('AI governance for delegated B2B supplier payment proposals')
    st.markdown('**No funds move** · All actions are mocked')
    st.metric('Revoked agents in session', len(st.session_state.revoked))
    st.metric('Session audit records', len(st.session_state.audit))
    st.caption('Policy baseline: src/payments.py. ML benchmark: training-only benign calibration; separate scripted holdout.')
    st.markdown('**Sources for business context**')
    st.markdown('[Visa / BILL / Billtrust pilot](https://corporate.visa.com/en/sites/visa-perspectives/press-releases/visa-bill-billtrust-launch-pilot.html)')
    st.markdown('[MAS AI risk guidelines](https://www.mas.gov.sg/regulation/guidelines/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions)')
    st.markdown('[MAS SAFR paper](https://www.mas.gov.sg/publications/monographs-or-information-paper/2026/safeguards-for-agentic-finance-at-runtime)')

t1,t2,t3,t4,t5,t6 = st.tabs(['🪪 Mandate Registry','💸 Payment Simulator','📈 Fraud & Anomalies','🛑 Policy Enforcement','👤 Human Review','🛡️ AI Governance'])

with t1:
    st.subheader('Agent identity and delegated payment authority')
    st.markdown('Each simulated mandate binds one agent to an accountable owner, specific suppliers, a spending ceiling and one permitted proposal tool. Revocation affects the current browser session only.')
    register=[]
    for a, info in AGENTS.items():
        register.append({'agent_id':a,'business_owner':info['owner'],'mandate_id':info['mandate'],'max_payment_sgd':info['limit_sgd'],'permitted_supplier_ids':', '.join(info['suppliers']),'permitted_tool':info['tool'],'session_status':'REVOKED' if a in st.session_state.revoked else 'ACTIVE'})
    st.dataframe(pd.DataFrame(register),hide_index=True,use_container_width=True)
    c1,c2=st.columns([2,1])
    with c1:
        chosen = st.selectbox('Select fictional agent for mandate inspection',list(AGENTS), key='mandate_agent')
        st.write(f"**Owner** {AGENTS[chosen]['owner']}  ·  **Mandate** {AGENTS[chosen]['mandate']}  ·  **Limit** SGD {AGENTS[chosen]['limit_sgd']:,}")
        st.write('**Permitted suppliers**', ', '.join(AGENTS[chosen]['suppliers']))
    with c2:
        st.markdown('**Exercise emergency revocation**')
        if chosen not in st.session_state.revoked:
            if st.button('Revoke selected mandate',key='revoke_mandate'):
                st.session_state.revoked.add(chosen)
                st.success('Simulated mandate revoked for this session.')
                st.rerun()
        else:
            if st.button('Restore fictional mandate',key='restore_mandate'):
                st.session_state.revoked.discard(chosen)
                st.success('Mandate restored for educational testing.')
                st.rerun()
    st.markdown('#### Approved supplier registry')
    sup = pd.DataFrame([{'supplier_id': k, **v} for k,v in SUPPLIERS.items()])
    st.dataframe(sup,hide_index=True,use_container_width=True)
    st.caption('Identifiers are intentionally fictional. Registry membership alone is not a substitute for bank beneficiary validation or production identity assurance.')

with t2:
    st.subheader('Fictional payment proposal simulator')
    st.markdown('The agent proposes a payment; a separate deterministic policy evaluates it before any simulated settlement. This is **not** a real agent executing a transaction.')
    scenario = st.selectbox('Select a demonstration scenario', ['All scenarios']+sorted(proposals.scenario.unique().tolist()), key='sim_scenario', format_func=lambda x:x.replace('_',' ').title())
    f = proposals if scenario=='All scenarios' else proposals.loc[proposals.scenario.eq(scenario)]
    p = selected_event('Inspect payment proposal', 'sim_proposal', f)
    event_summary(p)
    gate = show_outcome(p)
    st.write('**Scenario**', str(p.scenario_description))
    if p.proposal_id in st.session_state.settled:
        st.info('This invoice already has one simulated completion event in this browser session. Replay is blocked to illustrate idempotency.')
    can_complete = gate['outcome']=='ALLOW' and p.proposal_id not in st.session_state.settled
    if st.button('Record fictional payment completion',disabled=not can_complete,type='primary', key='complete_sim'):
        st.session_state.settled.add(p.proposal_id)
        st.session_state.audit.append(audit_record(p,'SIMULATED_COMPLETION','Demo simulator','Approved policy-only demonstration; no real money moved.',gate,event_type='MOCK_SETTLEMENT'))
        st.success('Fictional settlement event recorded. No payment provider was contacted and no funds were moved.')
    if gate['outcome'] != 'ALLOW':
        st.caption('Blocked and held proposals cannot be completed from this tab, even if their invoice text requests it.')
    st.markdown('#### Proposal register')
    cols = ['proposal_id','agent_id','supplier_id','amount_sgd','scenario','outcome','rule_id']
    st.dataframe(proposals[cols].head(60),hide_index=True,use_container_width=True)
    st.download_button('Download complete fictional payment proposals CSV',DATA.read_bytes(),'fictional_payment_proposals.csv','text/csv')

with t3:
    st.subheader('Fraud, anomaly detection and intervention trade-offs')
    st.markdown('**Isolation Forest** is an unsupervised anomaly detector. A separate **preventive policy gate** enforces explicit permissions. The holdout is stratified by scenario family; benign calibration is drawn from training data only.')
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Holdout unsafe proposals',str(metrics['unsafe_holdout']))
    c2.metric('Policy intervention recall',f"{100*metrics['policy']['recall']:.1f}%")
    c3.metric('Anomaly recall',f"{100*metrics['anomaly_model']['recall']:.1f}%")
    c4.metric('Legitimate straight-through',f"{100*metrics['policy_legitimate_straight_through']:.1f}%")
    st.warning('A perfect policy recall on these **scripted scenario families** reflects the rules covered by the lab. This is not evidence of production fraud prevention. Some legitimate proposals are held for review.')
    compare = pd.DataFrame([
        {'Approach':'Independent policy (HOLD or BLOCK)','Precision':metrics['policy']['precision'],'Recall':metrics['policy']['recall'],'F1':metrics['policy']['f1']},
        {'Approach':'Isolation Forest anomaly alert','Precision':metrics['anomaly_model']['precision'],'Recall':metrics['anomaly_model']['recall'],'F1':metrics['anomaly_model']['f1']},
    ])
    st.dataframe(compare,hide_index=True,use_container_width=True)
    st.bar_chart(compare.set_index('Approach')[['Precision','Recall','F1']])
    st.markdown('#### Cost and customer-friction perspective')
    c1,c2,c3=st.columns(3)
    c1.metric('Unsafe SGD value intercepted',f"SGD {metrics['scripted_unsafe_value_intervened_sgd']:,.2f}")
    c2.metric('Legitimate proposals held', f"{100*metrics['policy_false_hold_rate_legitimate']:.1f}%")
    c3.metric('Legitimate proposals blocked', f"{100*metrics['policy_false_block_rate_legitimate']:.1f}%")
    st.caption('"Value intercepted" is not actual losses prevented. It is the total face value of unsafe scripted proposals held or blocked before a fictional settlement.')
    with st.expander('Inspect holdout predictions and counterexamples'):
        view = st.radio('Show examples',['All cases','Policy interventions','Model missed unsafe cases','Unnecessary holds'],horizontal=True,key='ml_view')
        filtered=test_set
        if view=='Policy interventions': filtered=filtered.loc[filtered.outcome.isin(['HOLD','BLOCK'])]
        elif view=='Model missed unsafe cases': filtered=filtered.loc[filtered.reference_unsafe & (~filtered.anomaly_alert)]
        elif view=='Unnecessary holds': filtered=filtered.loc[(~filtered.reference_unsafe) & filtered.outcome.eq('HOLD')]
        st.dataframe(filtered[['proposal_id','scenario','amount_sgd','reference_unsafe','outcome','rule_id','anomaly_score','anomaly_alert']].head(120), hide_index=True,use_container_width=True)
    st.download_button('Download holdout predictions CSV',HOLDOUT.read_bytes(),'agentic_payment_holdout_predictions.csv','text/csv')

with t4:
    st.subheader('Independent payment policy enforcement')
    st.markdown('Preventive controls operate on **proposed** payment events; the simulator cannot call banks or move money. Invoice content has no authority to override payment rules.')
    outcome_filter = st.selectbox('Filter by original policy outcome',['All','BLOCK','HOLD','ALLOW'],key='enforce_filter')
    ff = proposals if outcome_filter=='All' else proposals.loc[proposals.outcome.eq(outcome_filter)]
    event = selected_event('Inspect proposed payment', 'enforcement_proposal', ff)
    event_summary(event)
    verdict = show_outcome(event)
    st.code(str(event.invoice_note),language='text')
    if contains_prompt_injection(str(event.invoice_note)):
        st.error('The text above includes a scripted prompt injection. It is treated as untrusted invoice data; no language model or tool executes it.')
    st.markdown('#### Policy outcomes across all fictional proposals')
    st.bar_chart(proposals.outcome.value_counts().rename_axis('Outcome').rename('Count'))
    st.dataframe(proposals[['proposal_id','agent_id','amount_sgd','scenario','outcome','rule_id']].head(100),hide_index=True,use_container_width=True)
    st.markdown('<div class="labnote">Session revocations from the Mandate Registry are applied when an event is inspected. Cached baseline totals above are frozen before any session revocation.</div>',unsafe_allow_html=True)

with t5:
    st.subheader('Human approval, exception review and dispute handling')
    st.markdown('Reviewers can record decisions and documentation gaps. **A reviewer note alone never releases a HOLD or overrides a BLOCK.** Approved payments still require refreshed buyer mandates and verified beneficiary records.')
    reviewable = proposals.loc[proposals.outcome.isin(['HOLD','BLOCK'])]
    rp = selected_event('Select fictional exception', 'human_event', reviewable)
    event_summary(rp)
    verdict=show_outcome(rp)
    with st.form('human_review',clear_on_submit=True):
        reviewer=st.text_input('Reviewer alias',value='Demo reviewer')
        decision=st.selectbox('Human decision',['Request supporting approval','Escalate to fraud team','Validate beneficiary independently','Reject proposed instruction','Open fictional dispute'])
        rationale=st.text_area('Review rationale (40–600 characters)',height=130,placeholder='Describe evidence reviewed, procedural safeguards and why no wrongdoing is presumed.')
        submit=st.form_submit_button('Record fictional human decision',type='primary')
    if submit:
        if len(reviewer.strip())<2:
            st.error('Provide a reviewer alias of at least two characters.')
        elif not 40<=len(rationale.strip())<=600:
            st.error('Please provide a substantive rationale containing 40–600 characters.')
        else:
            st.session_state.audit.append(audit_record(rp,decision,reviewer.strip(),rationale.strip(),verdict))
            st.success('Fictional human review recorded in this browser session. No payment has been authorised or released.')
    st.markdown('#### Browser-session audit trail')
    if st.session_state.audit:
        st.dataframe(pd.DataFrame(st.session_state.audit),hide_index=True,use_container_width=True)
    else:
        st.info('No session decisions recorded yet. Submit a fictional review or record an ALLOW payment in Tab 2.')
    st.download_button('Export fictional session audit CSV',session_csv(),'agentic_payment_session_audit.csv','text/csv')
    if st.button('Clear session audit records',key='clear_audit'):
        st.session_state.audit=[]
        st.success('Session audit cleared. Already-completed fictional invoice IDs remain idempotently protected this session.')
    st.caption('Session audit is in-memory and exportable; it is not a secure, persistent, tamper-evident audit log.')

with t6:
    st.subheader('AI governance, evidence and reproducibility')
    st.markdown('The lab demonstrates testable control concepts but **does not implement tokenisation, authenticated mandates, payment networks, AML screening, transaction monitoring, production security or MAS compliance certification**.')
    controls = [
        ('Fictional agent identity / ownership','Demonstrated in demo','Static registry and business owner'),
        ('Delegated spending and supplier boundaries','Demonstrated in demo','Deterministic policy checks'),
        ('Independent authorisation gate','Demonstrated in demo','ALLOW / HOLD / BLOCK before mock completion'),
        ('Mandate revocation','Demonstrated in demo','Browser-session effect only'),
        ('Duplicate invoice and beneficiary checks','Demonstrated in demo','Synthetic flags and registry'),
        ('Invoice prompt injection boundary','Demonstrated in demo','Literal scripted text patterns'),
        ('Human review and record export','Partial','Session-only, non-tamper-evident CSV'),
        ('Anomaly model validation','Partial','Synthetic scenario split, no external validity'),
        ('Authentic buyer identity / credentials','Not implemented','No external authentication'),
        ('Payment tokenisation and bank settlement','Not implemented','No payment API or money movement'),
        ('Independent live bank beneficiary verification','Not implemented','All bank data fictional'),
        ('Fraud, AML and sanctions production checks','Not implemented','No real-world screening'),
    ]
    ctl=pd.DataFrame(controls,columns=['Governance domain','Coverage','Important limitation'])
    st.dataframe(ctl,hide_index=True,use_container_width=True)
    st.markdown('#### Benchmark and provenance')
    a,b,c=st.columns(3)
    a.metric('Training proposals',str(metrics['train_proposals']))
    b.metric('Clean training fit',str(metrics['clean_fit_proposals']))
    c.metric('Clean calibration',str(metrics['clean_calibration_proposals']))
    with st.expander('Inspect hashes and benchmark methodology',expanded=True):
        st.json({"seed":metrics['seed'],"total_synthetic_proposals":metrics['total_synthetic_proposals'],"train_proposals":metrics['train_proposals'],"test_proposals":metrics['test_proposals'],"sha256_proposals_csv":metrics['sha256_proposals_csv'],"sha256_holdout_csv":metrics['sha256_holdout_csv'],"anomaly_threshold":metrics['threshold_calibrated_on_benign'],"evaluation_caveat":metrics['eval_caveat']})
        st.caption('Hashes help identify whether downloaded bytes match the generated fictional benchmark; they are not a cryptographic proof of payment validity.')
    st.markdown('#### Official reference material')
    st.markdown('- [MAS Guidelines on AI Risk Management for Financial Institutions](https://www.mas.gov.sg/regulation/guidelines/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions) (issued 7 October 2026; phased implementation begins 7 October 2027)')
    st.markdown('- [MAS Safeguards for Agentic Finance at Runtime (SAFR)](https://www.mas.gov.sg/publications/monographs-or-information-paper/2026/safeguards-for-agentic-finance-at-runtime) (industry paper, July 2026)')
    st.markdown('- [Visa / BILL / Billtrust agentic payment pilot](https://corporate.visa.com/en/sites/visa-perspectives/press-releases/visa-bill-billtrust-launch-pilot.html) (20 October 2026; buyer-approved invoice payments only)')
    st.download_button('Download evaluation methodology JSON',MANIFEST.read_bytes(),'agentic_payment_evaluation_manifest.json','application/json')
    if CASESTUDY.exists():
        st.download_button('Download four-page Project 05 case study',CASESTUDY.read_bytes(),'Agentic_Payment_Trust_Lab_Case_Study.pdf','application/pdf')
    st.caption('Authorship: educational prototype and interpretation by Adiputera Saadon. Design and code created with AI assistance; review and testing remain the author’s responsibility.')

st.divider()
st.caption('PROJECT 05 · FICTIONAL PAYMENT PROPOSALS ONLY · NO REAL AGENTS, CREDENTIALS, ACCOUNT DATA OR SETTLEMENT · NOT A PRODUCTION FINANCIAL CONTROL')
