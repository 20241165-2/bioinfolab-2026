#!/usr/bin/bash
# batchinfo.sh - 지정한 폴더 내 FASTA 파일 정보 출력

# 1. 인자 및 폴더 존재 여부 검사
if [ -z "$1" ] || [ ! -d "$1" ]; then
    echo "사용법: $0 <폴더경로>"
    echo "오류: 존재하지 않거나 올바르지 않은 폴더입니다."
    exit 1
fi

DIR="$1"

# 패턴과 일치하는 파일이 없으면 와일드카드 문자열을 남기지 않고 비움
shopt -s nullglob
FILES=("$DIR"/*.fasta)

# 2. FASTA 파일 존재 여부 검사
if [ ${#FILES[@]} -eq 0 ]; then
    echo "알림: '$DIR' 폴더 내에 FASTA 파일이 없습니다."
    exit 0
fi

# 3. 결과 출력
echo -e "file\tcount"
for F in "${FILES[@]}"; do
    FILENAME=$(basename "$F")
    COUNT=$(grep -c ">" "$F")
    echo -e "${FILENAME}\t${COUNT}"
done