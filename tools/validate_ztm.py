import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


REQUIRED_RESOURCES = {
    "colors",
    "typography",
    "dimensions",
    "effects",
    "animations",
    "windows",
    "taskbar",
    "startmenu",
    "controls",
}


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=reject_duplicate_keys)


def safe_package_path(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("resource path must be a non-empty relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"unsafe package path: {value}")
    target = root.joinpath(*path.parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"package path escapes its root: {value}")
    return target


def validate(package):
    root = Path(package).resolve()
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError("manifest.json is missing")

    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    if manifest.get("format") != "ZTM" or manifest.get("format_version") != 1:
        raise ValueError("only ZTM format version 1 is supported")
    if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", manifest.get("id", "")):
        raise ValueError("manifest id is missing or invalid")
    if not isinstance(manifest.get("name"), str) or not manifest["name"].strip():
        raise ValueError("manifest name is missing")
    if not isinstance(manifest.get("version"), str):
        raise ValueError("manifest version is missing")

    resources = manifest.get("resources")
    if not isinstance(resources, dict):
        raise ValueError("manifest resources must be an object")
    missing = REQUIRED_RESOURCES - resources.keys()
    if missing:
        raise ValueError("missing resource entries: " + ", ".join(sorted(missing)))

    for name, relative_path in resources.items():
        target = safe_package_path(root, relative_path)
        if not target.is_file():
            raise ValueError(f"resource {name} does not exist: {relative_path}")
        if not isinstance(load_json(target), dict):
            raise ValueError(f"resource {name} must contain a JSON object")

    assets = manifest.get("assets", {})
    if not isinstance(assets, dict):
        raise ValueError("manifest assets must be an object")
    for name, relative_path in assets.items():
        target = safe_package_path(root, relative_path)
        if target.exists() and not target.is_dir():
            raise ValueError(f"asset location {name} must be a directory")

    return len(resources)


def main():
    parser = argparse.ArgumentParser(description="Validate a Zev Theme Manifest package")
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    try:
        count = validate(args.package)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ZTM validation failed: {error}", file=sys.stderr)
        return 1
    print(f"ZTM v1 package valid: {count} resource documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
