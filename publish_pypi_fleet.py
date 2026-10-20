"""
PyPI Fleet Automated Publisher
Uploads all built packages in pypi_npm_seo_fleet/pypi/*/dist to PyPI.
Usage:
    python publish_pypi_fleet.py --token pypi-AgEIcHlwaS5vcmc...
    or set environment variable PYPI_API_TOKEN
"""
import os
import sys
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYPI_DIR = os.path.join(BASE_DIR, "pypi_npm_seo_fleet", "pypi")


def main():
    parser = argparse.ArgumentParser(description="Upload CheckerLeak PyPI SEO Fleet to PyPI.org")
    parser.add_argument("--token", help="PyPI API Token (starts with pypi-...)")
    parser.add_argument("--test", action="store_true", help="Upload to TestPyPI instead of production")
    args = parser.parse_args()

    token = args.token or os.getenv("PYPI_API_TOKEN")

    if not token:
        print("\n" + "=" * 60)
        print("⚠️  PyPI API Token Required")
        print("=" * 60)
        print("1. Create an account at https://pypi.org if you don't have one.")
        print("2. Go to Account Settings -> API Tokens -> Add API Token.")
        print("3. Run this script:")
        print("   python publish_pypi_fleet.py --token pypi-YOUR_TOKEN_HERE")
        print("=" * 60 + "\n")
        sys.exit(1)

    packages = [d for d in os.listdir(PYPI_DIR) if os.path.isdir(os.path.join(PYPI_DIR, d))]
    print(f"Found {len(packages)} packages to upload to PyPI...\n")

    for pkg in packages:
        dist_dir = os.path.join(PYPI_DIR, pkg, "dist")
        if not os.path.exists(dist_dir):
            print(f"⚠️  No dist/ found for {pkg}, skipping.")
            continue

        cmd = [
            sys.executable, "-m", "twine", "upload",
            "--username", "__token__",
            "--password", token,
            f"{dist_dir}/*",
            "--skip-existing"
        ]

        if args.test:
            cmd.extend(["--repository", "testpypi"])

        print(f"Uploading {pkg} to PyPI...")
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print(f"✅ Successfully published {pkg} to https://pypi.org/project/{pkg}/")
        else:
            print(f"❌ Failed to upload {pkg}")


if __name__ == "__main__":
    main()
