# CyberWatch

A free cybersecurity portal with a Kaspersky live map, security headlines, practical safety guides, a searchable OSINT directory, security-tool buying guidance and career resources.

## Preview

Open `index.html` to view the site. For headline loading, serve this folder with a local web server, such as `python -m http.server 8765`, and open http://localhost:8765. Headlines are loaded from `data/news.json`; the map requires internet access.

## Publish on GitHub Pages

1. Create a public GitHub repository named `cyberwatch` (or another name).
2. Upload the contents of this folder to its `main` branch. Include the hidden `.github` folder, `scripts` and `data`. Keep `index.html` at the repository root.
3. In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
4. In **Actions**, select **Publish CyberWatch and refresh headlines** and choose **Run workflow** if it has not already started.
5. When it completes, GitHub Pages shows the published link, normally `https://YOUR-USERNAME.github.io/cyberwatch/`.

Official instructions: https://docs.github.com/en/pages/quickstart

The included workflow fetches RSS headline metadata and publishes on pushes, manual runs and approximately every six hours. Scheduled runs can be delayed; GitHub disables scheduled workflows in inactive public repositories after 60 days. Updates happen during deployment, not continuously in each visitor's browser. The Refresh button reloads the published snapshot. Source failures retain the previous snapshot where available, and the site has publisher links if headlines are unavailable.

## Content and third-party services

- Map widget: https://cybermap.kaspersky.com/en/widget/
- CISA RSS: https://www.cisa.gov/cybersecurity-advisories/all.xml
- BleepingComputer RSS: https://www.bleepingcomputer.com/feed/
- Guides link to original NCSC guidance. Tool links open the actual providers.
- Career links are external job-board resources, not hosted or vetted vacancies.
- Buying guidance is not a set of hands-on product reviews. No prices, test results or star ratings are invented.
- Availability of third-party services is outside the site's control. The map reports Kaspersky telemetry, not every attack worldwide.

## Customise

Edit the name, text, colours and resource list in `index.html`. It has no external libraries, build process or paid dependency. It works on mobile and desktop. No accounts, payments, ads or affiliate tracking are installed. Cloudflare Web Analytics measures page views, visits and performance.

## Monetisation later

This site does not earn money merely because someone visits or clicks an ordinary link. Display advertising requires an approved ad-network account and ad code. Affiliate income requires joining a programme and replacing eligible provider links with your own affiliate URLs. Add a clear disclosure near affiliate content and mark paid links `rel="sponsored noopener noreferrer"`. Configure any consent requirements for your chosen services before activating tracking. No ad approval or revenue is guaranteed.

Start with useful content and an audience. You can apply for monetisation later without adding a paywall. GitHub Pages is available free for public repositories; review GitHub's current usage limits and terms before expanding into paid transactions or other commercial workflows.

## Added widgets and refreshed branding

- CISA exploited-vulnerability panel with fetched timestamp, addition dates, affected products and expandable recommended actions. `scripts/update_kev.py` reads CISA’s official GitHub mirror. The existing six-hour publishing workflow updates this feed too.
- Cloudflare Radar: switch between global traffic trends and application-layer attack volume, using the official rolling-window dark embeds. These embeds collect third-party usage metrics; the site’s privacy disclosure reflects that.
- Five-example phishing practice quiz in Stay safe online, with answer explanations, score and restart. Examples are fictional; progress is kept only in memory.
- Bevelled metallic shield mark with layered depth and mint highlights. It remains an inline vector so it stays crisp at small sizes.
- Removed the header’s “Open access / No account required” text.

## Networking and Programming

Both sections focus on cybersecurity. Networking covers security zones, subnet ranges (/0 through /32), service exposure reviews, firewall rules and investigating outbound connections. Programming covers failed-authentication summaries, allowlist validation, safe text rendering, security-event JSON, regex log searches and fictional web-log investigation. Three code-reading examples are displayed without execution. The formatter parses small practice examples (maximum 50,000 characters); it does not run code, transmit input or save it. JavaScript numeric precision limits apply. Learning links point to original documentation and providers.

## Sticky header navigation

All seven section links now sit in the header, which stays visible during scrolling. The sidebar was removed to give content the full available width. On narrow screens, the navigation row scrolls horizontally; links remain keyboard accessible.

## Port reference, regex and sample logs

Networking includes a searchable 22-entry reference with TCP/UDP filtering, defensive checks for every service and a link to IANA. Programming includes a JavaScript regex playground with examples, g/i/m flags, safe text highlighting and a one-second worker timeout. Inputs are limited to 300 pattern characters and 10,000 text characters; results are capped at 200. The sample log analyser uses 18 fictional requests and documentation IP addresses, with search, response-class filtering, counts and repeated-error hints. These widgets do not transmit or persist input.

Plain-English explanations: dotted-underlined terms show help on hover, keyboard focus or tap. Press Escape or tap elsewhere to close. Definitions cover security, networking and programming terms, including subnet results and fictional log response codes.

## Launch additions

Start here provides a five-step beginner path. About & contact identifies the maintainer and links to public GitHub feedback. Kaspersky and Cloudflare frames are created only after the visitor presses Load; Remove destroys the embedded frame. Choosing a chart before loading makes no provider request. Decisions are kept only for the current page visit.

## Provider reliability fixes

External widget frames now use no-referrer to avoid the Kaspersky connection failure observed when the GitHub site origin was included. Widgets still require an explicit click.

The headline updater uses clear request headers, retries transient failures once, and falls back from CISA RSS to CISA’s official KEV repository. Catalogue additions are labelled CISA KEV with addition dates; they are not presented as RSS articles. Each source has an update timestamp and fresh/fallback/saved state. If every source fails, saved items and their previous timestamps are retained. The browser identifies the fallback and saved-source states.

## Visitor analytics

Cloudflare Web Analytics was added on 4 October 2026 for shiney1874.github.io. The public beacon token in index.html identifies the analytics site; it is not an account API credential. The site remains hosted on GitHub Pages.

View statistics in the owner's Cloudflare account under Observability > Analytics > Web analytics, then select shiney1874.github.io. Filter the path to /CyberWatch/ if other sites are added to this hostname. Cloudflare reports visits and page views, not an exact count of distinct people. Blocking extensions and disabled JavaScript can prevent collection. Earlier visits cannot be recovered, and our deployment verification visits may be included.

Cloudflare documents automatic SPA measurement, but section-by-section reporting for this site's hash navigation has not been verified; do not assume every section switch is recorded. Practice form input is not sent by our integration. Cloudflare's service uses no cookies or local storage to collect usage metrics. About and the footer privacy disclosure describe the integration separately from the optional embedded map and chart.

Setup: https://developers.cloudflare.com/web-analytics/get-started/
Privacy: https://www.cloudflare.com/privacypolicy/
