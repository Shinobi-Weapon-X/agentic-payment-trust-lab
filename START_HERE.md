# Project 05 — START HERE

**Agentic Payment Trust Lab** by Adiputera Saadon

This folder is a complete offline Streamlit demonstration. **Do not enter real beneficiary accounts, credentials or private customer information. No payments can be made through this application.**

## A. Publish the source code on GitHub

1. Unzip `Agentic_Payment_Trust_Lab_Project_05.zip` on your Mac.
2. Visit https://github.com/new and sign in as `Shinobi-Weapon-X`.
3. Create public repository **`agentic-payment-trust-lab`**. Do not create another README or `.gitignore` during setup.
4. Open **Add file → Upload files**. Upload the **contents** of `agentic-payment-trust-lab` rather than the parent folder itself.
5. Include `app.py`, `README.md`, `requirements.txt`, `START_HERE.md`, `LICENSE`, `src/`, `data/`, `artifacts/`, `docs/`, `images/`, `tests/`, `scripts/`, `.streamlit/` and `.github/`.
6. macOS hides dotfolders. In Finder, press **Command + Shift + .** to show `.streamlit` and `.github` if needed. The app can run without the theme folder, but your intended design and CI file may be missing.
7. Enter commit message **Initial commit — Agentic Payment Trust Lab Project 05**, then press **Commit changes**.

## B. Deploy on Streamlit Community Cloud

1. Visit https://share.streamlit.io and select **Create app** → existing GitHub app.
2. **Repository** `Shinobi-Weapon-X/agentic-payment-trust-lab`
3. **Branch** `main`
4. **Main file path** `app.py`
5. **Python version** `3.11`
6. **App URL** `agentic-payment-trust-lab` if available, otherwise accept the generated URL.
7. Click **Deploy** and open the running application.

## C. Validate before sharing publicly

Use `docs/FUNCTIONAL_TEST_CHECKLIST.md` to test each of the six tabs. Pay particular attention to BLOCK, HOLD, mandate revocation, mock settlement replay prevention, human review records, audit CSV, and evaluation JSON. All data must remain fictional.

## D. Professional GitHub presentation

In the repository's **About** gear menu, enter the live Streamlit URL under **Website**, then add these topics individually with Enter between them:

`agentic-ai` · `agentic-payments` · `ai-governance` · `payment-security` · `fraud-detection` · `financial-crime` · `responsible-ai` · `streamlit`

Finally, edit line near the top of the README that says "Live URL" and replace it with a Markdown link to your Streamlit application. Commit the README update. Check GitHub and Streamlit public links from a separate browser profile without signing in.

## E. Use the case study on LinkedIn

The four-page portfolio PDF is at `docs/PROJECT_CASE_STUDY.pdf`. It includes **By Adiputera Saadon** at the end of page four. Upload as a LinkedIn Document rather than individual screenshots.

## F. Local run (optional)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `pytest -q` after installing pytest. To regenerate CSV and JSON artifacts, run `python scripts/generate_artifacts.py`.

**All payments are mocked. There is no AI agent orchestration, no bank integration and no real money movement.**
