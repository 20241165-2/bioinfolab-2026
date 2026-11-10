# parse_fastq.py 사용 설명서

## 1. 개요

`parse_fastq.py` 는 FASTQ 파일을 읽어 read 개수와 첫 번째 read 의 정보(이름, 서열, 길이)를 출력하는 스크립트이다.
외부 라이브러리 없이 파이썬 기본 문법만 사용한다.

- 위치: `lab11/src/parse_fastq.py`
- 입력: FASTQ 파일 1개
- 출력: 화면(표준 출력)에 요약 4줄

## 2. 사용법

```
$ cd lab11/src
$ python3 parse_fastq.py <FASTQ 파일>
```

| 인자 | 설명 |
|------|------|
| `<FASTQ 파일>` | 읽을 FASTQ 파일 경로 (`sys.argv[1]`) |

### 실행 예

```
$ python3 parse_fastq.py ../data/SRR1553607_1.fastq
read 개수: 203445
첫 read 이름: SRR1553607.1 1 length=101
첫 read 서열: GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
첫 read 길이: 101
```

`SRR1553607_2.fastq`(paired-end 의 두 번째 파일)도 같은 방법으로 실행하며, read 개수는 203445 개로 `_1` 파일과 같다.

## 3. FASTQ 형식

FASTQ 는 read 하나를 **4줄**로 저장한다.

```
@SRR1553607.1 1 length=101        ← 1줄: '@' + read 이름
GTTAGCGTTGTTGATCGCGACG...          ← 2줄: 염기 서열
+SRR1553607.1 1 length=101        ← 3줄: '+' (이름은 생략될 수 있음)
BB@FFFFFHHHHHJJJJJJJJJ...          ← 4줄: 품질 점수 (서열과 길이가 같다)
```

## 4. 코드 설명

### `read_fastq(filename)`

FASTQ 파일을 읽어 `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다.

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

| 반환값 위치 | 내용 |
|-------------|------|
| `reads[k][0]` | k 번째 read 의 이름 |
| `reads[k][1]` | k 번째 read 의 서열 |
| `reads[k][2]` | k 번째 read 의 품질 문자열 |

### 최상위 코드

```python
reads = read_fastq(sys.argv[1])
print("read 개수:", len(reads))
print("첫 read 이름:", reads[0][0])
print("첫 read 서열:", reads[0][1])
print("첫 read 길이:", len(reads[0][1]))
```

- read 개수 = 리스트 길이 = 파일 줄 수 ÷ 4 (813780 ÷ 4 = 203445)

## 5. 주의할 점

1. **인자를 주지 않으면 오류가 난다.**
   인자 개수를 확인하지 않으므로 `python3 parse_fastq.py` 만 실행하면 `IndexError: list index out of range` 가 난다.
2. **파일 전체를 메모리에 올린다.**
   `readlines()` 로 모든 줄을 한꺼번에 읽으므로 수 GB 크기의 FASTQ 에서는 메모리가 부족할 수 있다.
3. **압축 파일(`.fastq.gz`)은 읽지 못한다.** 먼저 `gunzip` 으로 풀어야 한다.
4. **형식 검사를 하지 않는다.**
   줄 수가 4의 배수가 아니거나 첫 줄이 `@` 로 시작하지 않아도 그대로 처리하거나 오류로 멈춘다.
5. **빈 파일이면** `reads[0]` 에서 `IndexError` 가 난다.

## 6. 데이터 파일

`lab11/data/SRR1553607_1.fastq`, `SRR1553607_2.fastq` 는 `.gitignore` 로 제외되어 커밋되지 않는다.
없으면 다시 내려받아야 한다.
