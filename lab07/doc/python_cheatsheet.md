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

------------------------------------------------

## def 로 함수 만드는 모양
'''python
def 함수이름(매개변수1, 매개변수2):
    # 실행할 코드
    return 결과값

## print 와 return 의 차이를 한 줄로
- print: 결과를 화면에 출력
- return: 함수가 계산한 값을 호출한 곳으로 전달하여 변수에 저장하거나 다른 계산에 활용할 수 있게함

## from 모듈 import 함수
- 모듈 파일 전체를 가져오지 않고, 필요한 특정 함수만 골라서 가져올 때 사용

## if __name__ == "__main__": 을 언제 쓰는지
- 해당 파이썬 파일이 다른 파일에 모듈로 import 될 때는 실행되지 않고, 터미널 등에서 직접 실행될 때만 메인코드를 작동시키고자 할 때 사용

## "w" 와 "a" 의 차이, 그리고 bash의 어떤 기호와 같은지
- "w":덮어쓰기(>), 기존 내용이 있으면 삭제하고 새로 작성
- "a":이어쓰기(>>), 기존 파일의 맨 뒤에 새 내용을 덧붙여 씀

## 오늘 겪은 오류 두 가지
- TypeError: int로 변환하지 않아서 오류 발생
- ZeroDivisionError: ""로 빈 값을 실행시켜서 오류 발생