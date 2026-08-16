# kindlepw2-kpm

KPM package repository for `kindlepw2` Kindles (Paperwhite 2–4, Voyage, Oasis 1–3).

The official [KindleModding repo](https://repo.kindlemodding.org) only ships `kindlehf`
artifacts. This repo repackages upstream releases as clean `kindlepw2` kpkgs and hosts
them via GitHub Releases.

## Adding this repo to your Kindle

Download [setup-repo.sh](https://raw.githubusercontent.com/domdorn/kindlepw2-kpm/main/setup-repo.sh) to your Kindle's
`/mnt/us/documents/` folder (via USB or the Kindle browser), then open it from your library.

Then install packages normally:

```
;kpm install koreader
;kpm install kterm
;kpm install kinamp
```

## Packages

| ID | Name | Source |
|----|------|--------|
| koreader | KOReader | [koreader/koreader](https://github.com/koreader/koreader) |
| kterm | KTerm | [bfabiszewski/kterm](https://github.com/bfabiszewski/kterm) |
| kinamp | KinAMP | [kbarni/KinAMP](https://github.com/kbarni/KinAMP) |
| lark | LARK | [kbarni/LARKPlayer](https://github.com/kbarni/LARKPlayer) |
| kindlepuzzles | Kindle Puzzles | [kbarni/kindlepuzzles](https://github.com/kbarni/kindlepuzzles) |
| kindlefilemanagers | Kindle File Managers | [kbarni/kindlefilemanagers](https://github.com/kbarni/kindlefilemanagers) |
| kships | KShips (Battleship) | [LOT-PL/KShips](https://github.com/LOT-PL/KShips) |
| gambatte | Gambatte-K2 (Game Boy) | [crazy-electron/gambatte-k2](https://github.com/crazy-electron/gambatte-k2) |
| gnomegames | Gnome Chess & Mines | [crazy-electron/GnomeGames4Kindle](https://github.com/crazy-electron/GnomeGames4Kindle) |
| kanki | KAnki (Flashcards) | [crizmo/KAnki](https://github.com/crizmo/KAnki) |
| kreate | Kreate (Drawing) | [Foskya/Kreate](https://github.com/Foskya/Kreate) |
| koplugin-annas | Anna's Archive (KOReader plugin) | [fischer-hub/annas.koplugin](https://github.com/fischer-hub/annas.koplugin) |
| koplugin-zlibrary | Z-library (KOReader plugin) | [ZlibraryKO/zlibrary.koplugin](https://github.com/ZlibraryKO/zlibrary.koplugin) |
| koplugin-filebrowser | Filebrowser (KOReader plugin) | [b-/filebrowser.koplugin](https://github.com/b-/filebrowser.koplugin) |

KOReader plugins (`koplugin-*`) install into `koreader/plugins/` and require KOReader
(`;kpm install koreader` first).

## Adding a new package

1. Create `packages/<id>/package.yml`:

```yaml
id: mypackage
name: My Package
author: Author Name
description: "What it does"
platform: kindlepw2
source:
  type: github_release
  repo: owner/repo
  tag: "v1.2.3"               # pinned upstream release — bumped by Renovate (see below)
  asset_pattern: "mypackage-*.zip"
  extract_subdir: mypackage   # subfolder inside the zip to use as payload root
```

2. Add `install.sh`, `launch.sh`, `uninstall.sh` under `packages/<id>/`.

3. Run `python build.py <id>` locally to test, then push — CI builds and deploys automatically.

### Version pinning & automatic updates

Each `github_release` source pins an explicit upstream `tag:` (omit it to always take the
latest release). Pinning keeps builds reproducible and records every version bump in git.

[Renovate](https://docs.renovatebot.com/) watches upstream releases and opens a PR bumping
`tag:` when a new one appears — config in [`renovate.json`](renovate.json). Tags with odd
formats (commit-hash or date suffixes) get a per-package `extractVersion` rule there.
`type: url` packages and branch tarballs are not auto-tracked.

### package.yml reference

```yaml
id: string              # KPM package ID (lowercase, no spaces)
name: string            # Display name
author: string
description: string
platform: kindlepw2     # or kindlehf, kindle5, kindle
source:
  type: github_release  # or: url
  repo: owner/repo      # for github_release
  tag: "v1.2.3"         # optional: pin a release (Renovate-tracked); omit = latest
  asset_pattern: "*.zip"           # glob matched against release asset names
  asset_exclude_pattern: "*-armhf*"  # optional glob to exclude (e.g. wrong arch)
  extract_subdir: foldername       # subfolder inside zip to use as payload
  # For type: url:
  url: https://example.com/pkg.zip
  version: "1.0.0"
dependencies: []        # list of KPM package IDs this depends on
```

### Hook scripts

All hooks run with cwd = the extracted kpkg directory.

**install.sh** — runs after extraction, copies files to `/mnt/us/`  
**launch.sh** — runs when launched via `;kpm launch <id>`  
**uninstall.sh** — receives `"upgrade"` as `$1` when upgrading (skip data deletion)

Key paths on the Kindle:
```
/mnt/us/documents/    ← drop .sh here to add a library scriptlet
/mnt/us/extensions/   ← KUAL extensions
/mnt/us/koreader/     ← KOReader installation
```

## CI setup

The GitHub Actions workflow builds all packages and publishes them as GitHub Releases on
every push to `main` and on a weekly schedule to pick up upstream releases.

No secrets or variables need to be configured — the workflow uses the built-in
`GITHUB_TOKEN`. The following variables can optionally be set in repository settings to
customise the generated `manifest.v2.json`:

| Variable | Default |
|----------|---------|
| `REPO_ID` | `dominikdorn` |
| `REPO_NAME` | `Dominik Dorn KPM Repo` |
| `REPO_DESC` | `kindlepw2-compatible packages` |

## Known limitations

- **kompanion** requires compiled binaries for `kindlepw2` (armel) — not yet available
  upstream. Would need cross-compilation. PRs welcome.
- Generic app zips (kinamp, lark, etc.) are untested on kindlepw2 — please report issues.
- Goal: contribute working `kindlepw2` artifacts upstream to
  [KindleModding/repo](https://github.com/KindleModding/repo).
