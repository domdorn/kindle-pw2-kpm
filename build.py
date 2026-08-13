#!/usr/bin/env python3
"""
Build KPM packages for kindlepw2 and generate manifest.v2.json.

Usage:
    python build.py                    # build all packages
    python build.py koreader kterm     # build specific packages
    python build.py --manifest-only    # regenerate manifest from existing dist/
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
MANIFEST_FILE = "manifest.v2.json"
REPO_BASE_URL = os.environ.get("REPO_BASE_URL", "https://dominikdorn.com/kpm")
REPO_ID = os.environ.get("REPO_ID", "dominikdorn")
REPO_NAME = os.environ.get("REPO_NAME", "Dominik Dorn KPM Repo")
REPO_DESC = os.environ.get("REPO_DESC", "kindlepw2-compatible packages pending upstream inclusion")


def gh_latest_release(repo):
    """Fetch latest release metadata from GitHub API."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


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
    """Extract a zip, optionally pulling out only one subdirectory as the root."""
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


def build_kpkg(pkg_dir, payload_dir, pkg_meta, version_tuple, output_path):
    """
    Build a clean .kpkg (gzipped tar, no macOS metadata).

    pkg_dir     — package source dir (contains install.sh etc.)
    payload_dir — extracted upstream release dir (the actual app files)
    """
    # Build the staging directory
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
        subdir_name = pkg_meta["source"].get("extract_subdir", pkg_meta["id"])
        payload_dest = os.path.join(staging, subdir_name)
        if payload_dir != staging:  # avoid copying into itself
            if os.path.isdir(payload_dir):
                shutil.copytree(payload_dir, payload_dest)
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
            "supported_platforms": [pkg_meta["platform"]],
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


def build_package(pkg_name):
    pkg_dir = os.path.join(PACKAGES_DIR, pkg_name)
    yml_path = os.path.join(pkg_dir, "package.yml")
    if not os.path.exists(yml_path):
        print(f"[SKIP] {pkg_name}: no package.yml")
        return None

    with open(yml_path) as f:
        meta = yaml.safe_load(f)

    print(f"\n[BUILD] {meta['id']} ({meta['name']})")

    source = meta["source"]
    os.makedirs(DIST_DIR, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        if source["type"] == "github_release":
            release = gh_latest_release(source["repo"])
            version = parse_version(release["tag_name"])
            print(f"  Version: {'.'.join(str(v) for v in version)} (tag: {release['tag_name']})")

            asset = find_asset(
                release["assets"],
                source["asset_pattern"],
                source.get("asset_exclude_pattern"),
            )
            if not asset:
                print(f"  [ERROR] No asset matching '{source['asset_pattern']}'")
                return None

            zip_path = os.path.join(tmpdir, asset["name"])
            download(asset["browser_download_url"], zip_path)

            payload_dir = extract_zip(
                zip_path, tmpdir, source.get("extract_subdir")
            )

        elif source["type"] == "url":
            version = parse_version(source.get("version", "1.0.0"))
            fname = source["url"].split("/")[-1]
            zip_path = os.path.join(tmpdir, fname)
            download(source["url"], zip_path)
            payload_dir = extract_zip(
                zip_path, tmpdir, source.get("extract_subdir")
            )
        else:
            print(f"  [ERROR] Unknown source type: {source['type']}")
            return None

        platform = meta["platform"]
        ver_str = ".".join(str(v) for v in version)
        kpkg_name = f"{meta['id']}_{ver_str}_{platform}.kpkg"
        kpkg_path = os.path.join(DIST_DIR, kpkg_name)

        manifest = build_kpkg(pkg_dir, payload_dir, meta, version, kpkg_path)
        print(f"  Built: {kpkg_path} ({os.path.getsize(kpkg_path) // 1024}KB)")

    return {
        "id": meta["id"],
        "name": meta["name"],
        "author": meta["author"],
        "description": meta["description"],
        "kpkg_name": kpkg_name,
        "version": list(version),
        "platform": platform,
        "dependencies": meta.get("dependencies", []),
    }


def generate_manifest(built_packages):
    """Generate manifest.v2.json from a list of built package results."""
    packages = {}
    for pkg in built_packages:
        pkg_id = pkg["id"]
        ver_str = ".".join(str(v) for v in pkg["version"])
        tag = f"{pkg_id}-{ver_str}"
        artifact = {
            "url": f"{REPO_BASE_URL}/{tag}/{pkg['kpkg_name']}",
            "version": pkg["version"],
            "dependencies": pkg["dependencies"],
            "supported_platforms": [pkg["platform"]],
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
        return {}
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
                "platform": artifact["supported_platforms"][0],
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
            result = build_package(pkg_name)
            if result:
                built.append(result)
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

    print(f"\nDone: {len(built)} built, {len(failed)} failed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
