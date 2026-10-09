#!/usr/bin/bash
# fastainfo.sh — FASTA 파일의 요약 정보를 출력한다
if [ -z "$1" ] || [ ! -f "$1" ]; then
    echo "사용법: $0 <FASTA파일>"
    exit 1
fi

FILE="$1"

COUNT=$(grep -c ">" "$FILE")
NAMES=$(grep ">" "$FILE" | cut -d' ' -f1 | tr -d '>')
BASE_COUNT=$(grep -v ">" "$FILE" | tr -d '\n\r ' | wc -c)

echo "파일: $FILE"
echo "서열 개수: $COUNT"
echo "서열 이름:"
echo "$NAMES"
echo "총 염기수(대략): $BASE_COUNT"