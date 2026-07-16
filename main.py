from pathlib import Path
import argparse

from scanners.scanoss import ScanOSS
from scanners.cryptofinder import CryptoFinder


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="OSS Audit Platform"
    )

    parser.add_argument(
        "--repository",
        default=".",
        help="Repository path to scan"
    )

    parser.add_argument(
        "--reports",
        default="reports",
        help="Reports directory"
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    repository = Path(args.repository).resolve()

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found: {repository}"
        )

    print("=" * 60)
    print("OSS Audit Platform")
    print("=" * 60)

    print("\nGenerating SBOM...")

    sbom = ScanOSS(
        repository=str(repository),
        reports_dir=args.reports,
    ).run()

    print(f"SBOM : {sbom}")

    print("\nGenerating CBOM...")

    cbom = CryptoFinder(
        repository=str(repository),
        reports_dir=args.reports,
    ).run()

    print(f"CBOM : {cbom}")

    print("\nScan completed successfully.")


if __name__ == "__main__":
    main()
