# qual_summary.py 사용 설명서

## 1. 개요

`qual_summary.py` 는 FASTQ 파일을 읽어 **모든 read 의 평균 품질 점수(Phred)** 를 계산해 한 줄로 출력하는 스크립트이다.
외부 라이브러리 없이 파이썬 기본 문법만 사용한다.

- 위치: `lab11/src/qual_summary.py`
- 입력: FASTQ 파일 1개 (Phred+33 인코딩)
- 출력: 화면(표준 출력)에 `전체 read 평균 품질: <값>` 1줄

## 2. 사용법

```
$ cd lab11/src
$ python3 qual_summary.py <FASTQ 파일>
```

| 인자 | 설명 |
|------|------|
| `<FASTQ 파일>` | 읽을 FASTQ 파일 경로 (`sys.argv[1]`) |

### 실행 예

```
$ python3 qual_summary.py ../data/SRR1553607_1.fastq
전체 read 평균 품질: 33.4497222958299

$ python3 qual_summary.py ../data/SRR1553607_2.fastq
전체 read 평균 품질: 30.830840894308746
```

두 파일 모두 read 는 203445 개, 길이는 모두 101 bp 이다.
paired-end 의 두 번째 read(`_2`)가 첫 번째 read(`_1`)보다 평균 품질이 약 2.6 낮다.
일반적으로 Illumina 시퀀싱에서 read 2 의 품질이 더 낮게 나온다.
실행 시간은 1~2 초 정도이다.

## 3. 품질 점수(Phred) 읽는 법

FASTQ 의 4번째 줄은 염기 하나마다 품질 문자 하나를 적는다.
문자의 ASCII 코드에서 33 을 빼면 Phred 품질 점수 Q 가 된다(Phred+33).

```
Q = ord(문자) - 33
```

| 문자 | ASCII | Q | 오류 확률 (10^(-Q/10)) |
|------|-------|---|------------------------|
| `!` | 33 | 0 | 1 |
| `+` | 43 | 10 | 1/10 |
| `5` | 53 | 20 | 1/100 |
| `?` | 63 | 30 | 1/1,000 |
| `I` | 73 | 40 | 1/10,000 |
| `J` | 74 | 41 | 약 1/12,600 |

- Q30 이상이면 품질이 좋다고 본다(염기 1000 개 중 오류 1 개).
- 예: 첫 read 품질 줄 `BB@FFFFFHHHHHJJJJ...` 에서 `B` = 66 − 33 = **33**, `J` = 74 − 33 = **41**.

## 4. 코드 설명

### `read_fastq(filename)`

FASTQ 파일을 읽어 `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다. (`parse_fastq.py` 와 같은 함수)

```python
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()          # 파일 전체를 줄 단위 리스트로 읽음
    for i in range(0, len(lines), 4):  # 4줄씩 건너뛰며 반복
        name = lines[i].rstrip()[1:]   # 1줄: 줄바꿈 제거 후 맨 앞 '@' 제거
        seq = lines[i + 1].rstrip()    # 2줄: 서열
        qual = lines[i + 3].rstrip()   # 4줄: 품질 (3줄 '+' 는 건너뜀)
        records.append((name, seq, qual))
    return records
```

### `mean_quality(qual)`

품질 문자열 하나를 받아 **그 read 의 평균 Phred 점수**를 돌려준다.

```python
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)    # 문자 → Phred 점수
    return sum(scores) / len(scores)   # 점수 평균
```

예: `mean_quality("II5")` → (40 + 40 + 20) / 3 = 33.33...

### 최상위 코드

```python
reads = read_fastq(sys.argv[1])

total = 0
for name, seq, qual in reads:
    q = mean_quality(qual)       # read 하나의 평균 품질
    total = total + q            # 모두 더함

print("전체 read 평균 품질:", total / len(reads))
```

계산 순서:

1. read 마다 평균 품질을 구한다.
2. 그 값을 모두 더한다.
3. read 개수로 나눈다 → **read 평균 품질들의 평균**.

## 5. 주의할 점

1. **인자를 주지 않으면 오류가 난다.**
   인자 개수를 확인하지 않으므로 `python3 qual_summary.py` 만 실행하면 `IndexError: list index out of range` 가 난다.
2. **"read 평균의 평균" 이다.**
   read 길이가 모두 같으면(이 데이터는 모두 101 bp) 전체 염기의 평균 품질과 같다.
   trimming 등으로 길이가 달라지면 짧은 read 와 긴 read 가 같은 비중으로 계산되어 전체 염기 평균과 달라진다.
3. **Phred+33 만 가정한다.** 아주 오래된 Illumina(1.3~1.7) 의 Phred+64 파일은 점수가 31 높게 나온다.
4. **파일 전체를 메모리에 올린다.**
   `readlines()` 로 모든 줄을 한꺼번에 읽으므로 수 GB 크기의 FASTQ 에서는 메모리가 부족할 수 있다.
5. **압축 파일(`.fastq.gz`)은 읽지 못한다.** 먼저 `gunzip` 으로 풀어야 한다.
6. **빈 파일이면** `len(reads)` 가 0 이라 `ZeroDivisionError` 가 난다.
   품질 줄이 빈 read 가 있어도 `mean_quality` 에서 같은 오류가 난다.
7. **소수점이 길게 출력된다.** 보기 좋게 하려면 `round(total / len(reads), 2)` 처럼 바꿀 수 있다.

## 6. 데이터 파일

`lab11/data/SRR1553607_1.fastq`, `SRR1553607_2.fastq` 는 `.gitignore` 로 제외되어 커밋되지 않는다.
없으면 다시 내려받아야 한다.
