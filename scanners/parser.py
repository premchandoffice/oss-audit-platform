from __future__ import annotations

import json
from pathlib import Path


class AuditParser:

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)

    def _latest_file(self, pattern: str) -> Path:

        files = sorted(self.reports_dir.glob(pattern))

        if not files:
            raise FileNotFoundError(
                f"No file found matching: {pattern}"
            )

        return files[-1]

    def _load_json(self, file: Path):

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse(self):

        sbom_file = self._latest_file("*_sbom.cdx.json")
        cbom_file = self._latest_file("*_cbom.cdx.json")

        sbom = self._load_json(sbom_file)
        cbom = self._load_json(cbom_file)

        summary = {
            "repository": sbom_file.stem.replace("_sbom.cdx", ""),
            "sbom_file": sbom_file.name,
            "cbom_file": cbom_file.name,
            "components": self._extract_components(sbom),
            "licenses": self._extract_licenses(sbom),
            "crypto_algorithms": self._extract_crypto(cbom),
        }

        summary_file = self.reports_dir / (
            summary["repository"] + "_summary.json"
        )

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4)

        return summary

    def _extract_components(self, sbom):

        return len(sbom.get("components", []))

    def _extract_licenses(self, sbom):

        licenses = {}

        for component in sbom.get("components", []):

            for lic in component.get("licenses", []):

                if isinstance(lic, dict):

                    license_id = (
                        lic.get("license", {}).get("id")
                        or lic.get("license", {}).get("name")
                        or "UNKNOWN"
                    )

                    licenses[license_id] = (
                        licenses.get(license_id, 0) + 1
                    )

        return licenses

    def _extract_crypto(self, cbom):

        algorithms = set()

        for component in cbom.get("components", []):

            for evidence in component.get("evidence", []):

                algorithm = evidence.get("algorithm")

                if algorithm:
                    algorithms.add(algorithm)

        return sorted(algorithms)


if __name__ == "__main__":

    parser = AuditParser()

    summary = parser.parse()

    print(json.dumps(summary, indent=4))
