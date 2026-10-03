#!/usr/bin/env python3
"""Add legacy app-level fields for LBox while preserving the upstream source."""
import argparse
import copy
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://raw.githubusercontent.com/bebound/AltGallery/master/all-apps.json"
OUTPUT_URL = "https://raw.githubusercontent.com/andykeppel/AltGallery-LBox/main/altgallery-lbox.json"

def convert(source):
    if not isinstance(source, dict) or not isinstance(source.get("apps"), list) or not source["apps"]:
        raise ValueError("Upstream must contain a non-empty apps array")
    result = copy.deepcopy(source)
    result["name"] = "AltGallery · LBox"
    result["identifier"] = "com.andykeppel.altgallery.lbox"
    result["sourceURL"] = OUTPUT_URL
    for app in result["apps"]:
        versions = app.get("versions")
        if not isinstance(versions, list) or not versions:
            raise ValueError(f"{app.get('name')}: missing versions")
        # AltStore sources list the preferred/latest release first; retain that order.
        latest = versions[0]
        for field in ("version", "date", "downloadURL", "size"):
            if field not in latest:
                raise ValueError(f"{app.get('name')}: missing {field}")
        if not isinstance(latest["version"], str) or not latest["version"]:
            raise ValueError("Invalid version")
        if not isinstance(latest["downloadURL"], str) or not latest["downloadURL"].startswith(("https://", "http://")):
            raise ValueError("Invalid download URL")
        if type(latest["size"]) is not int or latest["size"] < 0:
            raise ValueError("Invalid download size")
        app["version"] = latest["version"]
        app["versionDate"] = latest["date"]
        app["downloadURL"] = latest["downloadURL"]
        app["size"] = latest["size"]
        for original, legacy in (("localizedDescription", "versionDescription"),
                                 ("minOSVersion", "minOSVersion"),
                                 ("maxOSVersion", "maxOSVersion"),
                                 ("buildVersion", "buildVersion")):
            app.pop(legacy, None)
            if original in latest:
                app[legacy] = latest[original]
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Use a local source JSON for validation")
    parser.add_argument("--output", type=Path, default=Path("altgallery-lbox.json"))
    args = parser.parse_args()
    if args.input:
        source = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        request = Request(SOURCE_URL, headers={"User-Agent": "AltGallery-LBox/1.0"})
        with urlopen(request, timeout=60) as response:
            source = json.load(response)
    result = convert(source)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    # Never replace the last working feed with a failed/partial conversion.
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, args.output)
    print(f"Converted {len(result['apps'])} apps -> {args.output}")

if __name__ == "__main__":
    main()
