#!/bin/bash

# 인자 두 개 다 있는지 검사
if [ $# -lt 2 ]; then
    echo "사용법: shortlines.sh <FASTA파일> <최소길이>"
    exit 1
fi

FILENAME=$1
MINLEN=$2

# 파일 존재 검사
if [ ! -f "$FILENAME" ]; then
    echo "오류: 파일을 찾을 수 없습니다: $FILENAME"
    exit 2
fi

# 두 번째 인자가 숫자인지 검사
if ! [[ "$MINLEN" =~ ^[0-9]+$ ]]; then
    echo "오류: 최소 길이는 숫자여야 합니다: $MINLEN"
    exit 3
fi

# 짧은 서열 줄 세기
COUNT=0
while IFS= read -r LINE; do
    if [[ "$LINE" == ">"* ]]; then
        continue
    fi
    if [ ${#LINE} -lt $MINLEN ]; then
        COUNT=$((COUNT + 1))
    fi
done < "$FILENAME"

echo $COUNT