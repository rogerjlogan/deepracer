#!/usr/bin/env python3
import os
import mmap
from argparse import ArgumentTypeError


def valid_aws_log_file(file):
    if os.path.isfile(file):
        # using mmap to check file in place without overloading buffer by reading into memory
        with open(file, 'rb', 0) as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b'SIM_TRACE_LOG') != -1 and s.find(b'Reset') != -1:
                return file
    raise ArgumentTypeError(f"'{file}' is an invalid file. "
                            f"Should be an AWS Log file containing key words: 'SIM_TRACE_LOG' and 'Reset'")
