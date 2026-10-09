# Bash & Python 치트시트

## 화면 출력
- bash: `echo "hello"`
- python: `print("hello")`

## 변수
- bash: `NAME=gene1` / `echo $NAME`
- python: `name = "gene1"` / `print(name)`

## 문자열 길이
- bash: `${#SEQ}`
- python: `len(seq)`

## 특정 글자 개수
- bash: `grep -o G | wc -l`
- python: `seq.count("G")`

## 파일 한 줄씩 읽기
- bash: `while read LINE; do ... done < file`
- python: `for line in f:`

## 조건문
- bash: `if [ -f "$FILE" ]; then`
- python: `if os.path.isfile(file):`

## 반복문
- bash: `for F in *.fasta; do`
- python: `for path in glob.glob("*.fasta"):`

## 첫 번째 인자
- bash: `$1`
- python: `sys.argv[1]`

## 인자 개수
- bash: `$#`
- python: `len(sys.argv) - 1`

## 실패로 끝내기
- bash: `exit 1`
- python: `sys.exit(1)`

## 파일 이동/복사
- bash: `mv`, `cp`
- python: 옮길 필요 없음 — 터미널에서 bash로 하는 것이 더 간단

## 파이프
- bash: `grep ">" file | wc -l`
- python: 옮길 필요 없음 — 파일을 직접 읽어 처리하는 것이 파이썬 방식

## 소수 계산
- bash: 불가능 — 정수만 다룰 수 있음
- python: `gc / len(seq)`, `round()` 로 해결