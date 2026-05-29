#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import requests

TIMEOUT = 6
LOG_FILE = "m3u_filter.log"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (IPTV Checker)"
})


def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line + "\n")


def url_is_alive(url: str) -> bool:
    """
    Soft IPTV stream availability check.

    The script sends a GET request and tries to read the first byte
    from the response body.
    """
    try:
        response = session.get(url, stream=True, timeout=TIMEOUT)
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=1):
            if chunk:
                return True

        return False

    except Exception:
        return False


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage:\npython3 m3u_filter.py input.m3u output.m3u")
        return 1

    m3u_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(m3u_file, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.read().splitlines()

    log(f"START processing file: {m3u_file}")
    log(f"Total lines: {len(lines)}")

    checked = 0
    alive = 0
    output_lines = ["#EXTM3U"]

    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if not line.startswith("#EXTINF") or "**********" in line:
            index += 1
            continue

        if index + 1 >= len(lines):
            break

        url = lines[index + 1].strip()

        if not url.startswith(("http://", "https://")):
            log(f"SKIP non-http url: {url}")
            index += 2
            continue

        checked += 1

        if not url_is_alive(url):
            log(f"DEAD  {url}")
            index += 2
            continue

        alive += 1
        output_lines.append(line)
        output_lines.append(url)

        if checked % 10 == 0:
            print(f"Progress: checked={checked}, alive={alive}", end="\r")

        index += 2

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines) + "\n")

    log("FINISH")
    log(f"Checked URLs: {checked}")
    log(f"Alive URLs:   {alive}")
    log(f"Output file:  {output_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
