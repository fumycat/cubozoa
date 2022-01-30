#!/usr/bin/python3
import os
import sys
import re
import argparse
import platform
import string
import random
import subprocess
import datetime
from pathlib import Path

# Configuration
EDITOR = "vi"  # nano
TMP_DIR = "/dev/shm"  # /tmp
LOG_CHUNK_REGEX = "(?:\d\d:){3}[\s\S]*?(?=\n(?:\d\d:){3}|$)"
TIME_REGEX = "\d\d:\d\d:\d\d.\d\d\d\d\d\d"

logchunk = re.compile(LOG_CHUNK_REGEX)
timestr = re.compile(TIME_REGEX)
fromisoformat = datetime.time.fromisoformat
pool = string.ascii_letters + string.digits
if TMP_DIR == "/dev/shm" and platform.system() == "Darwin":
    TMP_DIR = "/tmp"

if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser(description="utility for filtering chronica logs")
    parser.add_argument("log_file", type=open)
    parser.add_argument("-c", action="append", help="show entries what contains ALL arguments")
    parser.add_argument("-y", action="append", help="show entries what contains ANY argument")
    parser.add_argument("-s", help="show entries after (HH:MM:SS.MMMMMM)")
    parser.add_argument("-e", help="show entries before (HH:MM:SS.MMMMMM)")
    # parser.add_argument("-m", help="filter by module (comma separated without space)")
    # parser.add_argument(
    #     "-l", help="filter by log level (comma separated without space)"
    # )
    args = parser.parse_args()
    # print(args)

    # In
    content = args.log_file.read()
    chunks = logchunk.findall(content)

    # Filters
    result = chunks
    if args.c:
        result = filter(lambda chunk: all(p in chunk for p in args.c), result)
    if args.y:
        result = filter(lambda chunk: any(p in chunk for p in args.y), result)
    if args.s:
        start_time = fromisoformat(args.s)
        result = filter(
            lambda x: fromisoformat(timestr.search(x)[0]) >= start_time, result
        )
    if args.e:
        end_time = fromisoformat(args.e)
        result = filter(
            lambda x: fromisoformat(timestr.search(x)[0]) <= end_time, result
        )
    # if args.l:
    #     # TODO
    #     levels = map(str.upper, args.l.split(","))
    #     result = result
    # if args.m:
    #     # TODO
    #     pass

    # Out
    result = list(result)

    if not result:
        sys.exit("Nothing found")

    result = "\n".join(result)

    tmp_file = Path(TMP_DIR) / "".join(random.choices(pool, k=7))

    with open(tmp_file, "w") as f:
        f.write(result)

    subprocess.call([EDITOR, tmp_file])
    os.remove(tmp_file)
