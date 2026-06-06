# Real Book Songfinder

A tiny, self-contained web app to search the 4,893 songs indexed in *The Real Book
Songfinder* (3.14.2016) and see which Real Book volume(s) each one appears in.

## Use it

Just open **`index.html`** in any browser — double-click it, no server needed. It
runs entirely offline (all data is embedded in the one file, ~238 KB).

- Type any part of a song title; matches update as you type.
- Search ignores accents, apostrophes and punctuation, so `agua de beber`,
  `take the a train`, and `aint misbehavin` all find the right songs.
- Each result lists the song title and the full name of every book that contains it.

## Host it

It's a small set of static files, so you can host it anywhere:

- **GitHub Pages / Netlify / Cloudflare Pages:** drop the whole folder in a repo/folder and deploy.
- **Any web server:** copy the files to the web root.

Hosting must be over **HTTPS** (all the above are by default) for the app to be installable
and to work offline. The files use relative paths, so a project subfolder
(e.g. `https://you.github.io/songfinder/`) works fine.

## Install as an app (iPad & Android)

This is a **PWA** — once hosted over HTTPS it installs to the home screen with its own
icon, runs fullscreen, and works offline (no app store needed).

- **iPad / iPhone (Safari):** open the URL → Share → **Add to Home Screen**.
- **Android (Chrome):** open the URL → menu (⋮) → **Install app** (or "Add to Home screen").

### Build a real Android `.apk` / `.aab` (optional)

Generating a signed Android package needs the Android SDK, which isn't required to use the
PWA. The easiest no-toolchain route is **PWABuilder**:

1. Host the app over HTTPS (see above) and confirm it installs in Chrome.
2. Go to <https://www.pwabuilder.com>, enter your URL.
3. Choose **Android** → **Generate Package**. It produces a signed `.aab` (for Play Store)
   and a test `.apk`, plus the signing key. Sideload the `.apk` or upload the `.aab` to
   Google Play.

(A real iPad *App Store* build is not possible without a Mac + Xcode + Apple Developer
account — the Safari "Add to Home Screen" install above is the supported path on iOS.)

### Files needed for hosting

`index.html`, `manifest.webmanifest`, `sw.js`, and the four PNG icons
(`icon-192.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon-32.png`).

> When you rebuild `index.html`, bump `CACHE` in `sw.js` (e.g. `rbsf-v1` → `rbsf-v2`) so
> installed copies pick up the new data.

## Rebuilding from the PDF

The source data is extracted from `MiscRealbksongfind2016.pdf`. To regenerate:

```sh
py extract.py   # PDF -> songs.json (needs: py -m pip install pymupdf)
py build.py     # songs.json + template.html -> index.html
```

- `extract.py` — column-aware text extraction + song/book parsing.
- `template.html` — the app UI/logic, with a `/*__DATA__*/` placeholder.
- `build.py` — repairs mis-extracted accented characters and injects the data.
- `songs.json` — the parsed dataset (`{title, books:[codes]}` per song).
- `make_icons.py` — regenerates the app icons (`py make_icons.py`; needs Pillow).
