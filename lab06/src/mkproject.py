#!/usr/bin/env python3
import sys
import os

# 인자 검사
if len(sys.argv) < 2:
    print("사용법: python3 mkproject.py <프로젝트이름>")
    sys.exit(1)

project = sys.argv[1]

# 같은 이름의 폴더가 이미 있는지 검사
if os.path.isdir(project):
    print("오류: 이미 존재하는 폴더입니다:", project)
    sys.exit(2)

# 폴더 만들기
os.makedirs(project + "/data")
os.makedirs(project + "/doc")
os.makedirs(project + "/src")

print("프로젝트 폴더를 만들었습니다:", project)