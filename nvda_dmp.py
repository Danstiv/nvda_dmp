"""A utility to calculate text insersions using Diff Match Patch.
Copyright 2020 Bill Dengler

licensed under the Apache licence, Version 2.0 (the "licence") with specific authorization to be distributed with NVDA;
you may not use this file except in compliance with the licence.
You may obtain a copy of the licence at

    http://www.apache.org/licences/licence-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the licence is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the licence for the specific language governing permissions and
limitations under the licence."""

import struct
import sys

from fast_diff_match_patch import diff

import time
init_time = 1707572604.8901055
def my_log(event):
	with open('d:/temp/log.log', 'ab') as f:
		f.write(f'{round(time.time()-init_time, 3)}\n{event}\n'.encode())

def main():
    goodLineEndings = (b"\n", b"\r")
    while True:
        my_log('reading text length')
        oldLen, newLen = struct.unpack("=II", sys.stdin.buffer.read(8))
        my_log(f'read length, old: {oldLen}, new: {newLen}')
        if not oldLen and not newLen:
            my_log('read zeros, terminating dmp')
            break  # sentinal value
        my_log('Reading old text')
        oldText = sys.stdin.buffer.read(oldLen)
        my_log('Reading new text')
        newText = sys.stdin.buffer.read(newLen)
        res = b""
        my_log('Calculating diff')
        for op, text in diff(oldText, newText, counts_only=False):
            if op == "+":
                res += text
                if not text.endswith(goodLineEndings):
                    res += b"\n"
        my_log('Writing diff size')
        sys.stdout.buffer.write(struct.pack("=I", len(res)))
        my_log('Writing diff')
        sys.stdout.buffer.write(res)
        sys.stdin.flush()
        sys.stdout.flush()


if __name__ == "__main__":
    main()
