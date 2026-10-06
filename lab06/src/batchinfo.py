#!/usr/bin/env python3
import sys
import os
import glob

# 인자 검사
if len(sys.argv) < 2:
    print("사용법: python3 batchinfo.py <폴더>")
    sys.exit(1)

folder = sys.argv[1]

# 폴더 존재 검사
if not os.path.isdir(folder):
    print("오류: 폴더를 찾을 수 없습니다:", folder)
    sys.exit(2)

print("file\tcount")
for path in sorted(glob.glob(folder + "/*.fasta")):
    n = 0
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                n = n + 1
    print(path + "\t" + str(n))