# M3U Playlist Filter

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A simple Python utility that checks IPTV stream URLs from an M3U playlist and creates a new M3U playlist containing only available streams.

## Features

- Reads standard M3U playlists
- Checks HTTP and HTTPS stream availability
- Filters out dead or inaccessible streams
- Preserves original `#EXTINF` metadata
- Generates a clean output `.m3u` playlist
- Writes processing logs to a local log file
- Simple CLI usage
- Minimal dependencies

## Requirements

- Python 3.7+
- requests

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests
```

## Usage

```bash
python3 m3u_filter.py input.m3u output.m3u
```

Example:

```bash
python3 m3u_filter.py examples/sample.m3u examples/sample_alive.m3u
```

## Input Format

The script expects a standard M3U playlist:

```m3u
#EXTM3U
#EXTINF:-1 tvg-name="Channel 1" group-title="TV",Channel 1
http://example.com/live/channel1
#EXTINF:-1 tvg-name="Channel 2" group-title="TV",Channel 2
http://example.com/live/channel2
```

## Output Format

The output file keeps only working streams:

```m3u
#EXTM3U
#EXTINF:-1 tvg-name="Channel 1" group-title="TV",Channel 1
http://example.com/live/channel1
```

## How It Works

For each stream in the source playlist, the script:

1. Finds a `#EXTINF` metadata line.
2. Reads the next line as the stream URL.
3. Sends an HTTP GET request with streaming enabled.
4. Attempts to read the first byte from the response.
5. Adds the stream to the output playlist only if it responds successfully.

## Log File

The script creates a log file in the current working directory:

```text
m3u_filter.log
```

Example log output:

```text
[2026-05-29 12:00:01] START processing file: channels.m3u
[2026-05-29 12:00:05] DEAD http://example.com/broken
[2026-05-29 12:00:20] FINISH
[2026-05-29 12:00:20] Checked URLs: 120
[2026-05-29 12:00:20] Alive URLs: 85
```

## Notes

- Some IPTV providers may block automated checks or require specific headers.
- A successful check only means that the stream responded at the time of testing.
- The script currently supports HTTP and HTTPS URLs.
- Very slow streams may be marked as unavailable if they exceed the timeout.

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── python-check.yml
├── examples/
│   ├── sample.m3u
│   └── sample_alive.m3u
├── .gitignore
├── LICENSE
├── README.md
├── m3u_filter.py
└── requirements.txt
```

## License

This project is licensed under the MIT License.
