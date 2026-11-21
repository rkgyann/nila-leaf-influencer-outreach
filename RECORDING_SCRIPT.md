# Recording script: Sankar Group assignment

This script is a guide for a live screen recording, not a claim that a video was recorded. The model used here is Qwen through Ollama, not Claude. Run only commands you understand and do not display API keys, credentials.json, token.json, private email contents, or unrelated browser tabs. Recording your screen can also expose notifications; turn them off before starting.

## Before recording

Open the project in VS Code. Start Ollama if it is not already running. In the terminal run:

```sh
source .venv/bin/activate
export AI_PROVIDER=ollama OLLAMA_MODEL=qwen3:1.7b
```

Use macOS Shift-Command-5, choose Record Selected Portion or Record Entire Screen, choose a microphone in Options if desired, then record. To stop, click the stop icon in the macOS menu bar. Play the recording back before sharing.

## Suggested narration and live commands (3–5 minutes)

1. **Introduction.** “This is Nila Leaf, a fictional skincare campaign. This prototype searches an indexed public web source for Instagram profiles, stores candidates in an SQLite CRM, and uses a local model to analyze profiles and prepare drafts.”

2. **Discovery.** Run:

   ```sh
   python app.py discover --niche 'skincare beauty' --location India --count 10
   python app.py list
   ```

   “These are public-web search results, not official Instagram API results. Follower counts are estimates, and profiles and business contacts need human verification.” Some results may already exist and be skipped. The search query is sent to Tavily.

3. **Source and AI filtering.** Pick a newly discovered candidate ID from the list, then run `python app.py show ID` and `python app.py analyze ID`, replacing ID with that number. “The program stores the source and asks a local AI model for a score and summary. The output is a suggestion that a human must check; the model can invent or misinterpret details.” Use `python app.py contacts ID` to show any business contact candidates; do not add or contact real people during this test.

4. **Gmail test and reply.** The earlier test email and reply have already been sent between two user-controlled inboxes. Show the test lead's status with `python app.py show 4` if it is still ID 4 in this project. This displays the test address and message; do not show unrelated messages. Explain: “We sent an approved initial test email, received a reply, and the app classified it as Interested. The reply draft is for human review.” The local model's draft requires editing. The app does not automatically send AI reply drafts.

5. **Follow-up and checks.** Show `python app.py jobs` and `python -m unittest discover -s tests -v`. “The scheduler queues individually approved drafts, checks the original Gmail thread for replies and can send them when due while the worker runs. The 3- and 5-day timeline is verified using a simulated clock and fake Gmail in automated tests; we have not waited for or sent a live scheduled follow-up.”

6. **Export and limitations.** Show `python app.py export /private/tmp/nila-demo-crm.csv`. “SQLite is the CRM and CSV can be imported into Sheets. This is a snapshot, not a live Sheets integration. Claude integration is included but unverified because the account has no API credits; this demo uses Qwen. The system is a prototype and generated messages require review.”

Do not record the demo as if a mock or simulated send were real. When finished, verify the video opens, audio is understandable, no secrets are visible, and upload it with the code ZIP and sample files.
