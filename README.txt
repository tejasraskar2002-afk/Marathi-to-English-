# Marathi2English AI Web App (mobile-first)

## Files
- `index.html`: main app
- `manifest.json`: installable web app metadata
- `icon.svg`: home-screen icon

## Important limitation
This folder is a static website project, not an already-hosted website. Android Chrome generally requires a secure HTTPS origin for microphone APIs and installable PWA behavior. Opening `index.html` directly from Downloads may not allow speech recognition or installation.

## Phone-only publishing workflow
1. Download/extract the ZIP on your Samsung phone using My Files.
2. To publish it without a computer, use a mobile-friendly static hosting service that accepts uploaded files or a repository website that lets you create/upload files from the browser. Upload all three files (`index.html`, `manifest.json`, `icon.svg`) to the site's public root.
3. Use the host's HTTPS URL. Open it in Chrome and allow microphone access.
4. Tap Chrome's `⋮` menu, then choose `Add to Home screen` or `Install app` if offered.
5. Open from the new home-screen icon.

## App behavior
- Requests browser speech recognition in Marathi (`mr-IN`) and sets continuous mode, with a 120-second timer.
- Speech support varies by Android browser/device; pauses can end recognition early. It is not guaranteed to capture every two-minute recording in one segment.
- Translation uses the MyMemory public endpoint (`mr|en`); Marathi support and rate limits may vary.
- Grammar suggestions use LanguageTool's public API. Public endpoints may change or limit usage.
- Text is sent to third-party online services. Do not submit private or confidential information.
- For a production service, use a trusted backend, privacy notice, error handling, and reviewed provider terms.
