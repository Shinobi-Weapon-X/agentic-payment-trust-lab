# Boardroom-style QA checklist — Agentic Payment Trust Lab

Check the deployed application in the main browser and again in a separate browser/profile without GitHub credentials.

## 1 — Mandate Registry
- [ ] Three fictional agent mandates and 12 registered suppliers display.
- [ ] Revoke `PAY-AGENT-A` and confirm an otherwise ALLOW proposal from that agent switches to BLOCK when inspected.
- [ ] Restore the fictional mandate and confirm the original policy result returns.

## 2 — Payment Simulator
- [ ] Select `routine_approved`, confirm ALLOW and simulate a completion; the screen explicitly says no real funds moved.
- [ ] Attempt to simulate the same case again and confirm the replay is disabled in this session.
- [ ] Select `duplicate_invoice`, confirm BLOCK, and verify the mock completion button is disabled.
- [ ] Export the fictional proposals CSV and inspect the data.

## 3 — Fraud & Anomalies
- [ ] Examine holdout metrics, baseline comparison chart, threshold description and limitations.
- [ ] Filter model misses and unnecessary holds; confirm results are displayed.
- [ ] Export the holdout CSV and compare fields with the dashboard.

## 4 — Policy Enforcement
- [ ] Filter BLOCK and select an `invoice_prompt_injection` event; verify BLOCK and display of inert untrusted invoice text.
- [ ] Filter HOLD and select a `pending_bank_change` event; verify HOLD explanation.
- [ ] Inspect ALLOW and verify active mandate and verified beneficiary.

## 5 — Human Review
- [ ] Try short rationale under 40 characters; verify error.
- [ ] Submit substantive reviewer alias and rationale; confirm session recording success.
- [ ] Export session audit CSV and confirm decision, timestamp, rule, reason and `real_payment_executed=False`.
- [ ] Confirm a review cannot turn BLOCK/HOLD into an executed payment.

## 6 — AI Governance
- [ ] Review table of demonstrated / partial / not implemented controls.
- [ ] Expand reproducibility details; inspect SHA-256 hashes.
- [ ] Export evaluation JSON.
- [ ] Open official MAS and Visa references (not private, unrelated or suspicious domains).
- [ ] Download four-page case study.

## Final publishing checks
- [ ] Public GitHub README renders correctly, case study link works, Streamlit launch link inserted.
- [ ] Dashboard loads from another Chrome profile without signed-in GitHub credentials.
- [ ] Public page displays six tabs and the explicit fictional simulation disclosure.
- [ ] `.streamlit/config.toml` was included when uploading hidden folders.

Report observed defects and fix them before claiming project readiness. Simulation results are not independent real-world model validation.
