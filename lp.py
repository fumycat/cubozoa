#!/usr/bin/python3
import os
import sys
import re
import argparse
import platform
import string
import random
import subprocess
from pathlib import Path

# Configuration
EDITOR = "vi"  # nano
TMP_DIR = "/dev/shm"  # /tmp
LOG_CHUNK_REGEX = "(?:\d\d:){3}[\s\S]*?(?=\n(?:\d\d:){3}|$)"

logchunk = re.compile(LOG_CHUNK_REGEX)
pool = string.ascii_letters + string.digits
if TMP_DIR == "/dev/shm" and platform.system() == "Darwin":
    TMP_DIR = "/tmp"

if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser(description="utility for filtering chronica logs")
    parser.add_argument("log_file", type=open)
    parser.add_argument("-c", help="filter by containing string")
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
    # Contains
    if args.c:
        result = filter(lambda x: args.c in x, result)
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
