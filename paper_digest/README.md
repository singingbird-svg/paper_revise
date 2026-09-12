# Paper Digest

`paper_digest` is a small Python CLI that collects recent papers from multiple public sources, filters them by keywords, and writes a daily Markdown digest in Chinese.

## What it does

- Fetches paper metadata from `arXiv`, `OpenAlex`, `Crossref`, `Semantic Scholar`, and `IEEE Xplore`
- Optionally reads Google alert emails from Gmail through IMAP
- Filters by date, include keywords, and exclude keywords
- Supports a required keyword layer for must-have concepts
- Supports `all` or `any` keyword matching
- Deduplicates records by DOI and normalized title
- Produces:
  - a short Chinese summary of the abstract
  - a best-effort "main innovation" note extracted from cue phrases
- Writes a Markdown report you can review, edit, and commit

## Quick start

```bash
cd /home/wenjing/paper/paper_digest
python3 -m paper_digest --date today --keywords "multi-agent,ltl,task allocation"
```

Example with excludes and a custom output path:

```bash
python3 -m paper_digest \
  --date 2026-04-11 \
  --keywords "robotics,planning" \
  --exclude-keywords "medical,biology" \
  --max-per-source 15 \
  --output reports/2026-04-11.md
```

For a wider catch, set `"lookback_days": 365` and `"keyword_match_mode": "any"` in `config.example.json`.
You can also use `"required_keywords"` for concepts that must always appear, such as `"temporal logic"`.
The config field `"output": "reports/{date}.md"` writes one file per day and avoids overwriting yesterday's report.

## Notes

- This tool uses public APIs, so network access is required when you actually run a query.
- Gmail support uses IMAP. Google documents IMAP access for Gmail and the secure endpoint `imap.gmail.com:993`, and Semantic Scholar exposes a public paper search API. Sources: https://developers.google.com/gmail/imap/imap-smtp and https://www.semanticscholar.org/product/api/tutorial
- IEEE Xplore support uses the official Metadata API and requires an API key. IEEE documents the `search/articles` endpoint, `querytext`, and `max_records` parameters in its developer docs. Sources: https://developer.ieee.org/docs/read/Searching_the_IEEE_Xplore_Metadata_API and https://developer.ieee.org/docs/read/Metadata_API_details
- The default summarizer is heuristic and fully local.
- If a paper has no abstract, the report still keeps the title, source, link, date, and venue.

## IEEE Xplore

1. Register for an IEEE developer account and request an API key.
2. Put the key into an environment variable.
3. Keep `ieee_api_key_env` in `config.example.json` pointing to that variable name.

Linux or macOS:

```bash
export PAPER_DIGEST_IEEE_API_KEY="your-ieee-key"
python3 -m paper_digest --config config.example.json
```

Windows PowerShell:

```powershell
$env:PAPER_DIGEST_IEEE_API_KEY="your-ieee-key"
python -m paper_digest --config config.example.json
```

## Gmail alerts

If Google is already emailing you paper alerts, the tool can fold those results into the same digest.

1. Enable IMAP in Gmail.
2. Put your Gmail username into `config.example.json`.
3. Put your mail password or app-specific password into an environment variable.
4. Set `"gmail.enabled": true`.

Linux or macOS:

```bash
export PAPER_DIGEST_GMAIL_PASSWORD="your-secret"
python3 -m paper_digest --config config.example.json
```

Windows PowerShell:

```powershell
$env:PAPER_DIGEST_GMAIL_PASSWORD="your-secret"
python -m paper_digest --config config.example.json
```

## Windows

This project is cross-platform because it only depends on the Python standard library.

1. Install Python 3.9 or newer on Windows.
2. Open PowerShell in the project directory.
3. Run:

```powershell
python -m paper_digest --config config.example.json
```

You can also double-click `run_daily.bat`.

## Schedule it daily on Windows

Edit `config.example.json` first, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\schedule_windows_task.ps1 -TaskName "PaperDigestDaily" -Time "08:00"
```

That creates a Windows Task Scheduler job which runs every day at `08:00`.

## Optional install

If you want a reusable command on Windows or Linux:

```bash
pip install -e .
paper-digest --config config.example.json
```

## Suggested workflow

1. Run the tool in the morning for your topic keywords.
2. Review the generated Markdown in VS Code.
3. Keep the papers worth reading and remove the noise.
4. Commit the report or sync it to GitHub.
