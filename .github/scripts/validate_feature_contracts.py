import yaml
import sys
import glob

REQUIRED_TOP_LEVEL_KEYS = [
    "feature",
    "entity",
    "time_semantics",
    "lineage",
    "definition",
    "schema",
    "data_quality",
    "monitoring",
    "parity",
    "security",
    "change_control",
    "tests",
    "signoff"
]

def validate_contract(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    missing = [k for k in REQUIRED_TOP_LEVEL_KEYS if k not in data]
    if missing:
        raise ValueError(f"{file_path} missing required keys: {missing}")

    print(f"✔ {file_path} passed basic validation")

def main():
    files = glob.glob("templates/**/*.yml", recursive=True) + \
            glob.glob("examples/**/*.yml", recursive=True)

    if not files:
        print("No feature contracts found.")
        return

    for f in files:
        validate_contract(f)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)
