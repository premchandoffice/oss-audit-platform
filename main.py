from pathlib import Path

from scanners.scanoss import ScanOSS
from scanners.cryptofinder import CryptoFinder
from scanners.parser import AuditParser

from ai.claude import ClaudeAI
from ai.report import ReportGenerator


REPORTS_DIR = "reports"


def get_repository_name(repository: Path) -> str:
    return repository.resolve().name


def main():

    repository = Path(".")

    repository_name = get_repository_name(repository)

    print("=" * 70)
    print("OSS Audit Platform")
    print("=" * 70)

    print("\n[1/5] Generating SBOM...")
    sbom = ScanOSS(
        repository=str(repository),
        reports_dir=REPORTS_DIR,
    ).run()

    print(f"SBOM Generated : {sbom.name}")

    print("\n[2/5] Generating CBOM...")
    cbom = CryptoFinder(
        repository=str(repository),
        reports_dir=REPORTS_DIR,
    ).run()

    print(f"CBOM Generated : {cbom.name}")

    print("\n[3/5] Parsing Reports...")
    parser = AuditParser(REPORTS_DIR)

    summary = parser.parse()

    summary_file = (
        Path(REPORTS_DIR)
        / f"{summary['repository']}_summary.json"
    )

    print(f"Summary Generated : {summary_file.name}")

    print("\n[4/5] Running Claude Analysis...")

    markdown = ClaudeAI().analyze(summary_file)

    print("Claude Analysis Completed")

    print("\n[5/5] Generating Report...")

    report = ReportGenerator().generate(
        repository=repository_name,
        report=markdown,
    )

    print(f"Audit Report : {report.name}")

    print("\nCompleted Successfully")


if __name__ == "__main__":
    main()
