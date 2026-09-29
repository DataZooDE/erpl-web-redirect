#!/usr/bin/env python3
"""Smoke test for the erpl_web redirect stub.

The stub exists only to tell users of the old extension name where the extension went,
so the assertion is inverted compared to a normal smoke test: LOAD must FAIL, and the
failure must name the replacement.

Usage: python3 scripts/smoke_test.py <extension_path> <duckdb_version> <arch>

Set DUCKDB_BIN to test against a local duckdb binary instead of downloading the
official CLI (used by `make test_redirect`).
"""

import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ARCH_TO_CLI_ZIP = {
    "linux_amd64": "duckdb_cli-linux-amd64.zip",
    "linux_arm64": "duckdb_cli-linux-aarch64.zip",
    "osx_amd64": "duckdb_cli-osx-universal.zip",
    "osx_arm64": "duckdb_cli-osx-universal.zip",
    "windows_amd64": "duckdb_cli-windows-amd64.zip",
}

REQUIRED_FRAGMENTS = ("renamed to erpl_odata", "INSTALL erpl_odata")


def download_duckdb_cli(version: str, arch: str, dest_dir: str) -> str:
    zip_name = ARCH_TO_CLI_ZIP.get(arch)
    if zip_name is None:
        raise SystemExit(f"Unsupported arch '{arch}'. Supported: {sorted(ARCH_TO_CLI_ZIP)}")

    url = f"https://github.com/duckdb/duckdb/releases/download/{version}/{zip_name}"
    zip_path = os.path.join(dest_dir, "duckdb_cli.zip")
    print(f"Downloading DuckDB {version} CLI ({arch}):\n  {url}")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)

    binary = os.path.join(dest_dir, "duckdb.exe" if platform.system() == "Windows" else "duckdb")
    if not os.path.isfile(binary):
        raise SystemExit(f"DuckDB binary not found after extraction: {binary}")
    if platform.system() != "Windows":
        os.chmod(binary, 0o755)
    return binary


def run_smoke_test(extension_path: str, duckdb_version: str, arch: str) -> None:
    if not os.path.isfile(extension_path):
        raise SystemExit(f"Extension artifact not found: {extension_path}")

    ext_sql_path = extension_path.replace("\\", "/")
    sql = f"LOAD '{ext_sql_path}';"

    with tempfile.TemporaryDirectory() as tmpdir:
        duckdb_bin = os.environ.get("DUCKDB_BIN") or download_duckdb_cli(duckdb_version, arch, tmpdir)
        proc = subprocess.run(
            # -c rather than stdin: the CLI keeps executing piped statements after an error
            # and exits 0, which would make a failed LOAD look like a success.
            [duckdb_bin, "-unsigned", "-c", sql], capture_output=True,
            text=True, encoding="utf-8", errors="replace",
        )

    combined = (proc.stdout or "") + (proc.stderr or "")
    print(combined)

    if proc.returncode == 0:
        raise SystemExit("Smoke test FAILED: LOAD of the erpl_web stub succeeded; it must fail")
    missing = [fragment for fragment in REQUIRED_FRAGMENTS if fragment not in combined]
    if missing:
        raise SystemExit(f"Smoke test FAILED: LOAD failed but the message lacks {missing}")
    print("Smoke test PASSED: LOAD erpl_web fails and points to erpl_odata")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(f"Usage: {sys.argv[0]} <extension_path> <duckdb_version> <arch>")
    run_smoke_test(*sys.argv[1:4])
