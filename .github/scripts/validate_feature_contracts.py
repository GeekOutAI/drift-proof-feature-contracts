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
    # --- YAML parsing with clear error handling ---
    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"{file_path} has invalid YAML: {e}")

    # --- Sanity check: must be a mapping/object ---
    if not isinstance(data, dict):
        raise ValueError(
            f"{file_path} must parse to a YAML object (mapping), got: {type(data)}"
        )

    # --- Required top-level keys check ---
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
