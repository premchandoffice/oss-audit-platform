from __future__ import annotations

from datetime import datetime
from pathlib import Path


class ReportGenerator:

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        repository: str,
        report: str,
    ) -> Path:

        today = datetime.now().strftime("%Y-%m-%d")

        output = (
            self.reports_dir
            / f"{today}_{repository}_audit_report.md"
        )

        with open(output, "w", encoding="utf-8") as f:
            f.write(report)

        return output
