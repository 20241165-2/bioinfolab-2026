#!/usr/bin/bash
# [조건 4] 스크립트 기능 설명 주석
# mkproject2.sh - 프로젝트 이름을 인자로 받아 하위에 data, doc, src 폴더 구조를 만드는 안전한 스크립트

# [조건 1] 인자가 없으면 사용법을 출력하고 exit 1로 끝낸다
if [ -z "$1" ]; then
    echo "사용법: $0 <프로젝트이름>"
    echo " 주어진 이름으로 프로젝트 표준 폴더(data, doc, src)를 생성합니다."
    exit 1
fi

TARGET="$1"

# [조건 2] 같은 이름의 폴더가 이미 있으면 덮어쓰지 않고 오류 메시지를 낸 뒤 끝낸다
if [ -d "$TARGET" ]; then
    echo "오류: '$TARGET' 폴더가 이미 존재합니다."
    exit 1
fi

# 폴더 구조 생성 (변수를 따옴표로 감싸 공백 문제 방지)
mkdir -p "$TARGET/data" "$TARGET/doc" "$TARGET/src"

# [조건 3] 정상적으로 끝나면 만들어진 구조를 보여 준다
echo "'$TARGET' 프로젝트 구조가 성공적으로 만들어졌습니다:"
ls -la "$TARGET"