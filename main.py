import os

def main():
    print("=" * 50)
    print("OSS Audit Platform")
    print("=" * 50)

    if os.getenv("GITHUB_ACTIONS"):
        print("Running inside GitHub Actions")
    else:
        print("Running locally")

if __name__ == "__main__":
    main()
