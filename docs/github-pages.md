# GitHub Pages publication

The complete multipage brand library is hosted at
[nonprophet-max.github.io/persistent-labs-design-system](https://nonprophet-max.github.io/persistent-labs-design-system/).
Publication and live verification passed on 10 November 2026. See [the release record](../reviews/alfred-brand/review.md).

The publication branch remains `codex/design-bible`. The repository's **Settings → Pages** source is **GitHub Actions**. The `github-pages` environment allows deployments from that branch. The checked-in workflow runs on pushes to `codex/design-bible` and can also be started manually from Actions. It packages skills, builds the whole library, uploads only `dist-pages/`, and deploys that artifact using the official GitHub Pages actions. It needs no account credentials or stored deployment tokens.

## Build and check

Python 3.9 or later and its standard library are sufficient:

```sh
python3 -m unittest discover -s scripts -p 'test_pages_base.py' -v
python3 scripts/package_skills.py
SITE_BASE_PATH=/persistent-labs-design-system python3 scripts/build_pages.py
```

`SITE_BASE_PATH` accepts an empty string, `/`, or an absolute plain path such as `/persistent-labs-design-system`. A trailing slash is normalized away. Invalid or ambiguous paths fail before the builder replaces the output. With the variable omitted, output uses root URLs and stays compatible with the existing local preview:

```sh
python3 scripts/package_skills.py
python3 scripts/build_pages.py
python3 -m http.server 8000 --directory dist-pages
```

For a Pages-path preview, build with the prefix above and serve a temporary parent directory whose `persistent-labs-design-system` entry points to `dist-pages`. Open `/persistent-labs-design-system/`. The published files themselves always remain directly inside `dist-pages/`; the builder does not create another repository-name folder.

`build/pages-manifest.json` retains the existing page-route list and adds each deployed `url`. `build/pages-validation.json` records the deployment prefix, page/chapter counts, redirects, and the output file inventory. The build validates local HTML links and fragments, CSS resources, and public source exclusions after removing the deployment prefix. Generated `.nojekyll` keeps the artifact a plain static site.

MemoryTree and FlameChorus remain subordinate parts of FireFlow. Their former routes have small static redirect pages to the corresponding FireFlow anchors, with a visible fallback link. GitHub Pages serves these pages as HTML redirects; they are not HTTP 301 responses. Netlify `_redirects` and `_headers` files are not used. The existing meta robots/robots.txt indexing preference remains; it is not access control.

All product pages, shared chapters, bundled fonts, assets and token downloads use the deployment prefix. External links and raw GitHub skill/resource links remain unchanged. Alfred's scoped interaction script is copied and defer-loaded on its product page when `src/alfred.js` exists. The generated library's source/archive/plugin directories are excluded as before; resources linked on GitHub stay in the public repository.

Browser validation uses the deployed prefix in both navigation targets and link expectations. `qa-pages.mjs` derives that prefix from `SITE_URL` or `SITE_BASE_PATH`. For the live library, run `SITE_URL=https://nonprophet-max.github.io/persistent-labs-design-system/ npm run check:pages`. The live suite passed all eleven pages and 110 layout/theme combinations; the focused Alfred suite passed 56 checks. Static component redirects and all hosted content files were also verified. Local build results alone do not demonstrate a successful deployment.

The workflow follows GitHub's [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [official deploy-pages action](https://github.com/actions/deploy-pages), using the versions verified on 10 November 2026: checkout v6, configure-pages v5, upload-pages-artifact v4 and deploy-pages v4.
