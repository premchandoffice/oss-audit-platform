from scanner.scanoss_runner import ScanOSSRunner


def main():

    runner = ScanOSSRunner()

    sbom = runner.scan(".")

    print(f"SBOM Location : {sbom}")


if __name__ == "__main__":
    main()
