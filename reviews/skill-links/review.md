# Per-page AI brand resources

Every page in the ten-page Netlify walkthrough now has a Build with AI panel. Each product page resolves its own brand from `brand-skills.json`; shared pages resolve Persistent Labs. The visible raw SKILL.md URL has a copy button. A native disclosure exposes the full GitHub plugin folder and raw chatbot guide, each with its own visible URL and copy button. Full URLs remain selectable without JavaScript. Clipboard denial selects the URL and announces a manual-copy fallback. The panel uses existing theme tokens and wraps long URLs on mobile.

All 18 public GitHub targets return successfully. Local Chromium checks pass 100 page/theme/width combinations, all 30 resource copy actions, correct per-brand routing and the clipboard denial fallback. Four expanded-panel screenshots were captured; desktop light and mobile dark captures were visually reviewed. Static checks still pass 107 color pairs and all six brand plugin checks. No brand rules or plugin contents changed.

Publication was attempted on 9 October 2026. Netlify returned HTTP 403: **Account credit usage exceeded - new deploys are blocked until credits are added**. The current production deployment remains `6ac8ea37db28a6ca70bf4eb6`; the new links are not live yet. The generated `dist-pages/` and `build/skill-links-dist-pages.zip` are ready for publication once account credits are available. Only the generated public site is included; source, review and plugin directories remain excluded.

After publication, rerun the browser suite against the live site and update this release record with the successful deployment ID. Existing Pi source/release records remain historical evidence for their original deployment.
