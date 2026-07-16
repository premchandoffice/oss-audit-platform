import shutil
import subprocess
from pathlib import Path


class ScanOSSRunner:
    """
    Runs SCANOSS and generates a CycloneDX SBOM.
    """

    def __init__(self, output_dir="reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def check_installation(self):
        """
        Verify that scanoss-py is installed.
        """
        if shutil.which("scanoss-py") is None:
            raise RuntimeError(
                "SCANOSS CLI is not installed.\n"
                "Install it using:\n"
                "pip install scanoss-py"
            )

    def scan(self, repository="."):
        """
        Scan a repository and generate a CycloneDX SBOM.

        Args:
            repository (str): Repository path

        Returns:
            Path: Path to generated SBOM
        """

        self.check_installation()

        output_file = self.output_dir / "sbom.json"

        command = [
            "scanoss-py",
            "scan",
            repository,
            "--format",
            "cyclonedx",
            "--output",
            str(output_file),
        ]

        print("Running SCANOSS...")
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"SCANOSS failed:\n{result.stderr}"
            )

        if not output_file.exists():
            raise FileNotFoundError(
                "SCANOSS completed but SBOM was not generated."
            )

        print(f"SBOM generated: {output_file}")

        return output_file
