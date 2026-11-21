# Nila Leaf: influencer outreach assistant

A practical Python command-line prototype for the Sankar Group assignment. Nila Leaf is a **fictional** skincare brand exploring refillable packaging. The project uses an SQLite CRM, Anthropic's Claude API and Gmail API. Test records and the offline demonstration are fictional; they are not real Instagram research.

## Current coverage and limitations

- **Research:** `discover` uses the public-web index provided by Tavily to find Instagram profile candidates and store their sources, timestamps and unverified follower estimates. It does not access private Instagram profiles or bypass authentication. The result is not Instagram’s official API, can be stale or incomplete, and needs human review. Candidate business emails remain unverified until a reviewer explicitly records or approves them.
- **AI:** Claude or a local Ollama model scores records, drafts emails and classifies replies. `--mock` is an offline simulation, not an AI call; clearly name the provider used.
- **CRM:** SQLite is the CRM; `export` writes a CSV that can be imported into Google Sheets. It is not a live Sheets integration.
- **Mail:** Gmail OAuth sends approved drafts and detects inbound messages in the same Gmail thread. A follow-up worker can classify detected replies, generate reviewable response drafts, and send previously reviewed and approved individual follow-up drafts when due while the worker is running. Initial and AI reply messages require individual approval. A reply in a new thread is not detected automatically; check Gmail manually as well.
- **Timing:** first follow-up becomes due after 3 days and the second 5 days after the prior follow-up. A total of two follow-ups and 10 sends per rolling 24 hours are allowed. Incoming replies block follow-ups; declines and opt-outs stay suppressed. There is a small race between the last check and Gmail sending. Do not use for a real campaign without stronger safeguards and a compliance review.
- **Testing:** offline tests use mocks. Gmail sending and same-thread reply detection have been tested using the owner’s two test inboxes. Live Tavily search and local Ollama scoring were tested. Claude API access and a real multi-day follow-up send remain untested. Set up your own accounts and run your own tests; tests in the suite use mocks and do not send email.

## Requirements

Python 3.10 or newer; VS Code or another terminal; internet access to install dependencies and use APIs. Live operation needs a paid/eligible Anthropic API key and a Google Cloud project with Gmail API access. Never share `credentials.json`, `token.json`, API keys, local CRM databases, or real contact data in a public repository. `.gitignore` excludes the standard secret files.

## Public profile discovery

With internet access, run `python app.py discover --niche "skincare beauty" --location India --count 10`. Keyless Tavily Search is free and rate-limited; optionally set `TAVILY_API_KEY` for a keyed account. Add `--min-followers 10000 --max-followers 100000` to keep only profiles whose indexed snippets contain a follower estimate in range. Unknown counts are omitted when bounds are supplied. Query text is sent to Tavily.

Use `python app.py list` and `python app.py show ID` to inspect stored sources. Use `python app.py contacts ID` for possible business emails found near business-contact language in public snippets; these are suggestions, not verified contact details. `python app.py approve-contact ID EMAIL` records a suggested address only after explicit verification. If the public business contact is found manually, `python app.py record-contact ID EMAIL HTTPS_SOURCE_URL` records it after confirmation and stores the source. Use `python app.py enrich ID --name "Name" --niche "skincare" --followers 5000 --location "India"` only after checking the source. No candidate is contacted automatically. Research provider: https://tavily.com/; keyless mode: https://docs.tavily.com/documentation/keyless.

## Quick offline demo in VS Code

1. Unzip the project and open the `sankar-outreach` folder in VS Code.
2. Select **Terminal → New Terminal** and check `python3 --version`.
3. Run:

   ```sh
   python3 demo.py
   python3 -m unittest discover -s tests -v
   ```

The demo shows import, deduplication, mock scoring, mock drafts, a simulated follow-up deadline and a simulated reply. The temporary demo database is deleted afterward. It sends nothing and makes no API calls. It is useful for learning, but **does not meet the assignment's live demonstration requirement**.

## Setup for live Claude and Gmail

1. In the VS Code terminal, create an environment and install Google libraries:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

   On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and use `python` instead of `python3`. Install Python from python.org if necessary.
2. Create an Anthropic API key in the Claude Console and ensure the account has API access. In the terminal, set it without adding it to a file or sharing it:

   ```sh
   export ANTHROPIC_API_KEY='paste-your-key-here'
   export CLAUDE_MODEL='claude-sonnet-4-5'
   ```

   If the model is unavailable to your account, use an API model ID that your account can access. On Windows PowerShell use `$env:ANTHROPIC_API_KEY = '...'` and `$env:CLAUDE_MODEL = '...'`. API use may incur charges. Do not paste secrets into screenshots, screen recordings or GitHub.
3. In Google Cloud Console, create or select a project and enable the **Gmail API**. Configure the Google Auth consent screen. For an external app in testing mode, add the Gmail account you will sign into as a test user. Create an OAuth client of type **Desktop app**, download its JSON, and save it as `credentials.json` in the project folder. Use the account owner's own authorized account. See Google's Gmail Python quickstart for the current console steps.
4. The first `sync` or `send` opens a browser for Google authorization. Grant the requested Gmail read and send scopes. The app saves a local `token.json` for later use. Delete it when you no longer need access and revoke access in your Google account if desired. Never upload either JSON file.

## Live test using accounts you control

Use a separate test Gmail address you control as the influencer's business email. Never send to sample `example.com` addresses; the application blocks them. To simulate a response, send a reply from that test inbox to the message in the same Gmail thread.

1. Copy `sample_data/influencers.csv` to a new file `my_test_leads.csv`, keep the header, and keep one row. Change the name, username, profile URL and email to test values. The profile URL must match the username in the CSV. Avoid real people's information unless you have an appropriate basis to use it. Delete or anonymize this CSV before sharing.
2. Import and review the local CRM:

   ```sh
   python app.py import my_test_leads.csv
   python app.py list
   python app.py analyze 1
   python app.py show 1
   ```

   Use the actual ID printed by `list` if it is not 1. Re-importing a username skips it rather than updating it. Treat AI scores as suggestions; inspect the original profile yourself.
3. Create and review an initial Claude draft:

   ```sh
   python app.py draft 1 --kind initial
   ```

   Note the printed draft ID. `python app.py send DRAFT_ID` reprints the recipient, subject and body. Type `SEND` only after checking each one. This invokes Gmail and really sends a message. To edit a draft before approval, run `python app.py export-draft DRAFT_ID draft.json`, edit the JSON in VS Code, and run `python app.py update-draft DRAFT_ID draft.json`. Scheduled or sent drafts cannot be edited.
4. Reply from your test inbox in the **same thread**. Then run:

   ```sh
   python app.py sync
   python app.py classify 1
   python app.py draft 1 --kind reply
   python app.py show 1
   ```

   Review the classification and reply draft. `send` of a reply draft also needs approval; never send if the lead declined or opted out. The program stops follow-ups immediately on detecting an incoming reply, even if Claude classification fails.
5. On a separate test lead with no reply, draft a follow-up with `python app.py draft ID --kind followup`. Review and, if desired, edit it, then run `python app.py queue-followup DRAFT_ID --stage 1` and type `APPROVE` to schedule that exact message. Start `python app.py watch` to check Gmail and automatically send approved due messages. The worker also classifies new replies and generates drafts for human review; it never sends those replies automatically. The worker must stay running. The first follow-up is due after 3 days; a separately approved stage 2 is due 5 days after the first. `python app.py jobs` displays job state. If sending fails or its outcome is uncertain, the job is blocked rather than retried; inspect Gmail before taking further action. The `demo.py` simulation illustrates timing without waiting but is not a live send.
6. Export a sample CRM:

   ```sh
   python app.py export crm-export.csv
   ```

   Open it locally or import it into a Google Sheet. Review for private information before sharing.

## Record the required video

Record your screen while running the **live test** with your authorized test accounts. Show the public profile/research data, import and deduplication, Claude analysis and drafts, human approval of the initial test email, the Gmail test reply, sync/classification/reply draft, and CRM status. Explain that the follow-up worker must remain running and the real waiting periods were not tested and show the offline timing demo separately, clearly labelling it as simulated. Hide API keys, OAuth details, personal inbox contents and other sensitive data. Include `sample_data/example_emails.md`, a sample CRM export containing only fictional or authorized test data, and this source code with the submission.

## Useful commands

`python app.py list` lists leads; `python app.py show ID` displays a lead; `python app.py status ID 'Collaboration Confirmed'` records a manually confirmed outcome. Once a lead has replied, declined, opted out or been marked confirmed, it cannot be manually reset to an active outreach status. `python app.py --help` lists all commands. For isolated testing set `OUTREACH_DB` to an absolute path before running commands. Stop use and inspect Gmail manually if sync fails; do not send follow-ups until the cause is resolved.

## Free local model option

The prototype can use Ollama and a local model instead of the Claude API. This is an alternative provider, not Claude; it does not satisfy the assignment's specific Claude requirement unless the recruiter accepts it. Model results can be incorrect and must be reviewed. Local inference keeps profile text on your computer; the initial Ollama and model downloads require internet and disk space.

1. Install Ollama from https://ollama.com/download and start it. Check the installer instructions for your operating system.
2. Download a model (the first command downloads approximately 1.4 GB for qwen3:1.7b):

   ```sh
   ollama pull qwen3:1.7b
   ```

3. In the project terminal on macOS or Linux, select the local provider:

   ```sh
   source .venv/bin/activate
   export AI_PROVIDER=ollama
   export OLLAMA_MODEL=qwen3:1.7b
   python app.py analyze 1
   python app.py draft 1 --kind initial
   ```

   On Windows PowerShell use `.venv\Scripts\Activate.ps1`, `$env:AI_PROVIDER='ollama'`, and `$env:OLLAMA_MODEL='qwen3:1.7b'`. Ollama must be running on localhost port 11434. The first inference may take several minutes. To switch back, set `AI_PROVIDER=claude` and provide an Anthropic key and available API credits.


### Follow-up safeguards

Only explicitly queued and approved drafts are eligible for the worker. It syncs Gmail before processing and rechecks the thread immediately before sending. Any inbound message in that thread blocks queued follow-ups. A reply arriving after the final check can still race with the send, and replies in new threads are not detected. A crash or uncertain network result leaves a job in `sending` or `blocked` so it cannot automatically retry. Do not use this prototype for a real campaign without production-grade safeguards and testing.
