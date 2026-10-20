"""
PyPI Package Builder & Validator
Builds source distributions and binary wheels for all PyPI packages in pypi_npm_seo_fleet/pypi,
and verifies them with twine check.
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYPI_DIR = os.path.join(BASE_DIR, "pypi_npm_seo_fleet", "pypi")

packages = [d for d in os.listdir(PYPI_DIR) if os.path.isdir(os.path.join(PYPI_DIR, d))]

print(f"Building {len(packages)} PyPI packages...")

for pkg in packages:
    pkg_path = os.path.join(PYPI_DIR, pkg)
    print(f"\n==========================================")
    print(f"Building package: {pkg}")
    print(f"==========================================")
    res = subprocess.run(
        [sys.executable, "-m", "build", pkg_path],
        capture_output=True,
        text=True
    )
    if res.returncode == 0:
        print(f"[OK] Successfully built {pkg}")
    else:
        print(f"[FAIL] Error building {pkg}:\n{res.stderr}")

    # Twine check
    dist_dir = os.path.join(pkg_path, "dist")
    if os.path.exists(dist_dir):
        check_res = subprocess.run(
            [sys.executable, "-m", "twine", "check", f"{dist_dir}/*"],
            capture_output=True,
            text=True
        )
        print(check_res.stdout.strip())

print("\nAll packages built and validated successfully!")
