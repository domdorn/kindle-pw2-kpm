#!/usr/bin/env python3
"""
Build KPM packages for kindlepw2 and generate manifest.v2.json.

Usage:
    python build.py                    # build all packages
    python build.py koreader kterm     # build specific packages
    python build.py --manifest-only    # regenerate manifest from existing dist/

package.yml platform field variants:
    platform: kindlepw2                    # single platform (string)
    platform: [kindlepw2, kindlehf]        # single kpkg supports both platforms
    artifacts:                             # separate kpkg per platform (different downloads)
      - platform: kindlepw2
        source: ...
      - platform: kindlehf
        source: ...
"""

import argparse
import fnmatch
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

import yaml  # pip install pyyaml

PACKAGES_DIR = "packages"
DIST_DIR = "dist"
# MANIFEST_FILE override lets a local test build write a separate (gitignored)
# manifest, e.g. MANIFEST_FILE=test-manifest.v2.json for an on-device test repo.
MANIFEST_FILE = os.environ.get("MANIFEST_FILE", "manifest.v2.json")
# Default points at the GitHub Releases "latest" alias; CI overrides REPO_BASE_URL with the
# per-build release URL. For local on-device testing, override it (and REPO_ID/MANIFEST_FILE)
# to point a throwaway manifest at wherever you host the test kpkgs.
REPO_BASE_URL = os.environ.get("REPO_BASE_URL", "https://github.com/domdorn/kindlepw2-kpm/releases/latest/download")
REPO_ID = os.environ.get("REPO_ID", "dominikdorn")
REPO_NAME = os.environ.get("REPO_NAME", "Dominik Dorn KPM Repo")
REPO_DESC = os.environ.get("REPO_DESC", "kindlepw2-compatible packages pending upstream inclusion")


def gh_get(url):
    """GET a GitHub API URL with optional auth, return parsed JSON."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def gh_release(repo, tag=None):
    """Fetch release metadata: the pinned `tag` if given, else the latest release."""
    if tag:
        return gh_get(f"https://api.github.com/repos/{repo}/releases/tags/{tag}")
    return gh_get(f"https://api.github.com/repos/{repo}/releases/latest")


def find_asset(assets, pattern, exclude_pattern=None):
    """Find a release asset matching a glob pattern."""
    for asset in assets:
        name = asset["name"]
        if exclude_pattern and fnmatch.fnmatch(name, exclude_pattern):
            continue
        if fnmatch.fnmatch(name, pattern):
            return asset
    return None


def download(url, dest):
    print(f"  Downloading {url}")
    token = os.environ.get("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def extract_zip(zip_path, dest_dir, subdir=None):
    """Extract a zip or tarball, optionally pulling out one subdirectory as the root."""
    lower = zip_path.lower()
    if lower.endswith((".tar.gz", ".tgz", ".tar")):
        with tarfile.open(zip_path) as tf:
            tf.extractall(dest_dir)
    else:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
    if subdir:
        subdir_path = os.path.join(dest_dir, subdir)
        if not os.path.isdir(subdir_path):
            # Try to find it case-insensitively
            for name in os.listdir(dest_dir):
                if name.lower() == subdir.lower():
                    subdir_path = os.path.join(dest_dir, name)
                    break
        return subdir_path
    return dest_dir


def build_kpkg(pkg_dir, payload_dir, pkg_meta, version_tuple, output_path, platforms):
    """
    Build a clean .kpkg (gzipped tar, no macOS metadata).

    pkg_dir     — package source dir (contains install.sh etc.)
    payload_dir — extracted upstream release dir (the actual app files)
    platforms   — list of supported platform strings for manifest.json
    """
    with tempfile.TemporaryDirectory() as staging:
        # Copy package scripts
        for fname in ["install.sh", "launch.sh", "uninstall.sh"]:
            src = os.path.join(pkg_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(staging, fname))

        # Copy extra dirs defined in package (scriptlets/, extensions/, etc.)
        for extra in os.listdir(pkg_dir):
            src = os.path.join(pkg_dir, extra)
            if os.path.isdir(src) and not extra.startswith("."):
                shutil.copytree(src, os.path.join(staging, extra))

        # Copy the payload under its subdir name
        subdir_name = pkg_meta["source"].get("extract_subdir", pkg_meta["id"]) if "source" in pkg_meta else pkg_meta["id"]
        # payload_exclude: glob patterns dropped from the payload (e.g. ".git",
        # redundant bundled archives) so they don't bloat the kpkg.
        excludes = pkg_meta["source"].get("payload_exclude", []) if "source" in pkg_meta else []
        payload_dest = os.path.join(staging, subdir_name)
        if payload_dir != staging:
            if os.path.isdir(payload_dir):
                ignore = shutil.ignore_patterns(*excludes) if excludes else None
                shutil.copytree(payload_dir, payload_dest, ignore=ignore)
            else:
                shutil.copy2(payload_dir, payload_dest)

        # Write manifest.json
        manifest = {
            "manifest_version": 2,
            "id": pkg_meta["id"],
            "name": pkg_meta["name"],
            "author": pkg_meta["author"],
            "description": pkg_meta["description"],
            "version": list(version_tuple),
            "dependencies": pkg_meta.get("dependencies", []),
            "supported_platforms": platforms,
        }
        with open(os.path.join(staging, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

        # Pack — Python tarfile avoids macOS ._* resource forks
        print(f"  Packing {output_path}")
        with tarfile.open(output_path, "w:gz", compresslevel=5) as tar:
            for name in sorted(os.listdir(staging)):
                if name.startswith(".") or name.startswith("._"):
                    continue
                tar.add(os.path.join(staging, name), arcname=name)

        # Verify manifest is readable
        with tarfile.open(output_path, "r:gz") as tar:
            tar.extractfile(tar.getmember("manifest.json")).read()

    return manifest


def parse_version(tag):
    """Parse a GitHub release tag into a (major, minor, patch) tuple."""
    tag = tag.lstrip("v")
    parts = re.findall(r"\d+", tag)
    parts = [int(p) for p in parts[:3]]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def _resolve_platforms(raw):
    """Normalize platform field to a list."""
    if isinstance(raw, list):
        return raw
    return [raw]


def _fetch_source(source, tmpdir):
    """Download and extract a source, return (payload_dir, version_tuple)."""
    if source["type"] == "github_release":
        # `tag` pins the upstream release (tracked in git, bumped by Renovate);
        # without it, fall back to the latest release.
        release = gh_release(source["repo"], source.get("tag"))
        version = parse_version(release["tag_name"])
        pin = "pinned" if source.get("tag") else "latest"
        print(f"  Version: {'.'.join(str(v) for v in version)} (tag: {release['tag_name']}, {pin})")

        asset = find_asset(
            release["assets"],
            source["asset_pattern"],
            source.get("asset_exclude_pattern"),
        )
        if not asset:
            print(f"  [ERROR] No asset matching '{source['asset_pattern']}'")
            return None, None

        zip_path = os.path.join(tmpdir, asset["name"])
        download(asset["browser_download_url"], zip_path)
        payload_dir = extract_zip(zip_path, tmpdir, source.get("extract_subdir"))
        return payload_dir, version

    elif source["type"] == "url":
        version = parse_version(source.get("version", "1.0.0"))
        fname = source["url"].split("/")[-1]
        zip_path = os.path.join(tmpdir, fname)
        download(source["url"], zip_path)
        payload_dir = extract_zip(zip_path, tmpdir, source.get("extract_subdir"))
        return payload_dir, version

    else:
        print(f"  [ERROR] Unknown source type: {source['type']}")
        return None, None


def build_package(pkg_name):
    """Build all artifacts for a package. Returns list of result dicts."""
    pkg_dir = os.path.join(PACKAGES_DIR, pkg_name)
    yml_path = os.path.join(pkg_dir, "package.yml")
    if not os.path.exists(yml_path):
        print(f"[SKIP] {pkg_name}: no package.yml")
        return []

    with open(yml_path) as f:
        meta = yaml.safe_load(f)

    print(f"\n[BUILD] {meta['id']} ({meta['name']})")
    os.makedirs(DIST_DIR, exist_ok=True)

    # Multi-artifact mode: separate source download per platform
    if "artifacts" in meta:
        results = []
        for artifact_spec in meta["artifacts"]:
            platforms = _resolve_platforms(artifact_spec["platform"])
            source = artifact_spec["source"]
            # Inject extract_subdir default from top-level source if not set
            if "extract_subdir" not in source and "source" in meta and "extract_subdir" in meta["source"]:
                source = dict(source)
                source["extract_subdir"] = meta["source"]["extract_subdir"]

            with tempfile.TemporaryDirectory() as tmpdir:
                payload_dir, version = _fetch_source(source, tmpdir)
                if payload_dir is None:
                    continue

                ver_str = ".".join(str(v) for v in version)
                primary_platform = platforms[0]
                kpkg_name = f"{meta['id']}_{ver_str}_{primary_platform}.kpkg"
                kpkg_path = os.path.join(DIST_DIR, kpkg_name)

                # Temporarily patch meta so build_kpkg can find the subdir name
                meta_with_source = dict(meta)
                meta_with_source["source"] = source
                build_kpkg(pkg_dir, payload_dir, meta_with_source, version, kpkg_path, platforms)
                print(f"  Built: {kpkg_path} ({os.path.getsize(kpkg_path) // 1024}KB)")

                results.append({
                    "id": meta["id"],
                    "name": meta["name"],
                    "author": meta["author"],
                    "description": meta["description"],
                    "kpkg_name": kpkg_name,
                    "version": list(version),
                    "platforms": platforms,
                    "dependencies": meta.get("dependencies", []),
                })
        return results

    # Single-artifact mode: one download, platform can be string or list
    platforms = _resolve_platforms(meta.get("platform", "kindlepw2"))
    source = meta["source"]

    with tempfile.TemporaryDirectory() as tmpdir:
        payload_dir, version = _fetch_source(source, tmpdir)
        if payload_dir is None:
            return []

        ver_str = ".".join(str(v) for v in version)
        primary_platform = platforms[0]
        kpkg_name = f"{meta['id']}_{ver_str}_{primary_platform}.kpkg"
        kpkg_path = os.path.join(DIST_DIR, kpkg_name)

        build_kpkg(pkg_dir, payload_dir, meta, version, kpkg_path, platforms)
        print(f"  Built: {kpkg_path} ({os.path.getsize(kpkg_path) // 1024}KB)")

    return [{
        "id": meta["id"],
        "name": meta["name"],
        "author": meta["author"],
        "description": meta["description"],
        "kpkg_name": kpkg_name,
        "version": list(version),
        "platforms": platforms,
        "dependencies": meta.get("dependencies", []),
    }]


def generate_manifest(built_packages):
    """Generate manifest.v2.json from a list of built package results."""
    packages = {}
    for pkg in built_packages:
        pkg_id = pkg["id"]
        artifact = {
            "url": f"{REPO_BASE_URL}/{pkg['kpkg_name']}",
            "version": pkg["version"],
            "dependencies": pkg["dependencies"],
            "supported_platforms": pkg["platforms"],
        }
        if pkg_id not in packages:
            packages[pkg_id] = {
                "name": pkg["name"],
                "author": pkg["author"],
                "description": pkg["description"],
                "artifacts": [],
            }
        packages[pkg_id]["artifacts"].append(artifact)

    manifest = {
        "manifest_version": 2,
        "id": REPO_ID,
        "name": REPO_NAME,
        "description": REPO_DESC,
        "packages": packages,
    }
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest written to {MANIFEST_FILE}")
    return manifest


def load_existing_manifest():
    """Load existing manifest to merge with new builds."""
    if not os.path.exists(MANIFEST_FILE):
        return []
    with open(MANIFEST_FILE) as f:
        m = json.load(f)
    result = []
    for pkg_id, pkg in m.get("packages", {}).items():
        for artifact in pkg.get("artifacts", []):
            kpkg_name = artifact["url"].split("/")[-1]
            result.append({
                "id": pkg_id,
                "name": pkg["name"],
                "author": pkg["author"],
                "description": pkg["description"],
                "kpkg_name": kpkg_name,
                "version": artifact["version"],
                "platforms": artifact["supported_platforms"],
                "dependencies": artifact.get("dependencies", []),
            })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*", help="Package names to build (default: all)")
    parser.add_argument("--manifest-only", action="store_true", help="Regenerate manifest from existing dist/")
    args = parser.parse_args()

    if args.manifest_only:
        existing = load_existing_manifest()
        generate_manifest(existing)
        return

    # Discover packages
    all_packages = sorted(
        d for d in os.listdir(PACKAGES_DIR)
        if os.path.isdir(os.path.join(PACKAGES_DIR, d))
        and os.path.exists(os.path.join(PACKAGES_DIR, d, "package.yml"))
    )
    targets = args.packages if args.packages else all_packages

    built = []
    failed = []
    for pkg_name in targets:
        try:
            results = build_package(pkg_name)
            if results:
                built.extend(results)
            else:
                failed.append(pkg_name)
        except Exception as e:
            print(f"  [ERROR] {pkg_name}: {e}")
            failed.append(pkg_name)

    if not built:
        print("\nNothing built.")
        sys.exit(1)

    # When building a subset, merge with existing manifest so other packages aren't dropped
    if args.packages:
        built_ids = {p["id"] for p in built}
        existing = [p for p in load_existing_manifest() if p["id"] not in built_ids]
        built = existing + built

    generate_manifest(built)

    print(f"\nDone: {len(built)} artifact(s) built, {len(failed)} failed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
