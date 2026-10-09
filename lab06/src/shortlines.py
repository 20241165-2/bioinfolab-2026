#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 3:
    print("사용법: python3 shortlines.py <FASTA파일> <최소길이>")
    sys.exit(1)

filename = sys.argv[1]
minlen_str = sys.argv[2]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

if not minlen_str.isdigit():
    print("오류: 최소 길이는 숫자여야 합니다:", minlen_str)
    sys.exit(3)

minlen = int(minlen_str)

# 서열별 길이 계산
lengths = {}
name = None
with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            lengths[name] = 0
        else:
            lengths[name] = lengths[name] + len(line)

# 최소 길이보다 짧은 서열 세기
count = 0
for name in lengths:
    if lengths[name] < minlen:
        count = count + 1

print(count)