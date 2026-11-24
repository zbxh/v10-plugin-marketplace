#!/usr/bin/env python3
"""Read a V10 plugin ZIP and check its structure, CRC, and PHP syntax."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import zipfile


def check_layout(archive, root, entry):
    seen = set()
    files = []
    for member in archive.infolist():
        original = member.orig_filename
        name = original[:-1] if member.is_dir() else original
        parts = name.split("/")
        if (
            parts[0] != root
            or any(part in {"", ".", ".."} for part in parts)
            or "\\" in name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
            or (len(parts) == 1 and not member.is_dir())
        ):
            raise ValueError(f"Invalid path for plugin root {root!r}: {original!r}")
        if name in seen:
            raise ValueError(f"Duplicate ZIP member: {name!r}")
        seen.add(name)
        mode_type = stat.S_IFMT(member.external_attr >> 16)
        expected_type = stat.S_IFDIR if member.is_dir() else stat.S_IFREG
        if mode_type not in {0, expected_type}:
            raise ValueError(f"ZIP member is not a regular file or directory: {name!r}")
        if not member.is_dir():
            files.append(PurePosixPath(name))
    file_paths = set(files)
    if PurePosixPath(root, entry) not in file_paths:
        raise ValueError(f"Missing plugin entry: {root}/{entry}")
    for name in seen:
        if any(parent in file_paths for parent in PurePosixPath(name).parents):
            raise ValueError(f"ZIP directory conflicts with a file: {name!r}")
    return files


def check_archive(archive, root, entry, php):
    files = check_layout(archive, root, entry)
    damaged = archive.testzip()
    if damaged is not None:
        raise ValueError(f"ZIP CRC failed: {damaged!r}")
    version = subprocess.run(
        [php, "-v"], capture_output=True, check=True, text=True, timeout=30
    )
    php_version = version.stdout.splitlines()[0] if version.stdout else ""
    if not php_version.startswith("PHP "):
        raise ValueError("The specified executable did not identify itself as PHP.")
    php_files = [path for path in files if path.suffix.lower() == ".php"]
    for path in php_files:
        lint = subprocess.run(
            [php, "-l"], input=archive.read(str(path)), capture_output=True, timeout=30
        )
        if lint.returncode:
            output = (lint.stderr or lint.stdout).decode("utf-8", errors="replace").strip()
            raise ValueError(f"PHP lint failed for {str(path)!r}: {output}")
    return {"files": len(files), "php_files_checked": len(php_files), "php": php_version}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--root", required=True, help="Expected top-level plugin directory")
    parser.add_argument("--entry", required=True, help="PHP entry path relative to the plugin directory")
    parser.add_argument("--php", required=True, help="PHP CLI executable matching the target V10 site")
    args = parser.parse_args()
    if not args.root.isascii() or not args.root.replace("_", "").isalnum():
        parser.error("--root must be a plugin directory identifier")
    if not args.entry.lower().endswith(".php"):
        parser.error("--entry must identify a PHP file")
    try:
        with args.package.open("rb") as package:
            with zipfile.ZipFile(package) as archive:
                result = check_archive(archive, args.root, args.entry, args.php)
            package.seek(0)
            digest = hashlib.sha256()
            for chunk in iter(lambda: package.read(1024 * 1024), b""):
                digest.update(chunk)
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        parser.exit(1, f"{parser.prog}: {exc}\n")
    result["sha256"] = digest.hexdigest()
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
