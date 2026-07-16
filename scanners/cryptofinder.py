from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


class CryptoFinder:
    """
    Generates a CycloneDX CBOM using CryptoFinder.
    """

    def __init__(self, repository: str = ".", reports_dir: str = "reports"):
        self.repository = Path(repository).resolve()
        self.reports_dir = Path(reports_dir)

        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _repository_name(self) -> str:
        return self.repository.name

    def _output_file(self) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")

        return (
            self.reports_dir
            / f"{today}_{self._repository_name()}_cbom.cdx.json"
        )

    def run(self) -> Path:

        output_file = self._output_file()

        command = [
            "crypto-finder",
            "scan",
            str(self.repository),
            "--format",
            "cyclonedx",
            "--output",
            str(output_file),
        ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if process.returncode != 0:
            raise RuntimeError(
                f"\nCryptoFinder Scan Failed\n\n"
                f"STDOUT:\n{process.stdout}\n\n"
                f"STDERR:\n{process.stderr}"
            )

        if not output_file.exists():
            raise FileNotFoundError(
                "CryptoFinder finished successfully but CBOM was not generated."
            )

        return output_file


if __name__ == "__main__":

    cbom = CryptoFinder().run()

    print(cbom)
