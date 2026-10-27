# lab07 요약 — 파이썬 함수와 모듈로 FASTA 다루기

lab07에서는 **함수(`def`)를 만들고**, 자주 쓰는 함수를 **모듈(`fasta.py`)로 모은 뒤**, 다른 스크립트에서 `import`해 FASTA 파일을 읽고, 거르고, 요약했다.

## 폴더 구성

| 폴더 | 내용 |
|------|------|
| `src/` | 파이썬 스크립트, 모듈 `fasta.py`, 함수 설명 `README.md` |
| `data/` | 연습용 FASTA (`seqs.fasta`, `seqs2.fasta`, `lower.fasta`, `noheader.fasta`) |
| `doc/` | 결과 파일(`summary.tsv`, `batchinfo.tsv`, `long.fasta`)과 `python_cheatsheet.md` |

## 1. 함수 기초

- `fgc.py`: `gc_content(seq)`를 직접 정의하고 호출해 GC 비율을 계산한다.
- `fseqlen.py`: **print와 return의 차이**를 확인한다.
  - `length_print()`는 화면에 출력만 하므로 변수에 담으면 `None`이 된다.
  - `length_return()`은 값을 돌려주므로 변수에 저장하거나 다른 계산에 쓸 수 있다.

```python
def 함수이름(매개변수):
    # 실행할 코드
    return 결과값
```

## 2. 모듈 `fasta.py`

| 함수 | 하는 일 |
|------|---------|
| `read_fasta(filename)` | FASTA를 읽어 `{이름: 서열}` 딕셔너리로 반환. 헤더의 첫 단어만 이름으로 쓰고, 서열은 대문자로 바꾼다. 헤더 없는 줄은 무시 |
| `gc_content(seq)` | GC 비율(0~1)을 반환. 빈 서열이면 `0.0` (ZeroDivisionError 방지) |
| `write_fasta(seqs, filename)` | 딕셔너리를 FASTA 파일로 저장 |
| `reverse_complement(seq)` | A↔T, C↔G로 바꾼 뒤 뒤집은 역상보 서열 반환 |
| `length_stats(seqs)` | 개수·총 길이·평균·최소·최대 길이를 딕셔너리로 반환 |

- `if __name__ == "__main__":` 블록은 파일을 **직접 실행할 때만** 동작한다. 여기서 각 서열의 길이·GC를 출력하고, `assert`로 역상보를 두 번 하면 원래 서열이 되는지 시험한다.
- `README.md`에 함수 목록을 정리했고, 추가하고 싶은 함수로 **T↔U 변환 함수**를 적었다.

## 3. 모듈을 import해서 쓰는 스크립트

모두 `from fasta import ...`로 필요한 함수만 가져오고, `sys.argv`로 인자를 받는다.

| 스크립트 | 사용법 | 하는 일 |
|----------|--------|---------|
| `countseq2.py` | `python countseq2.py in.fasta` | 서열 개수 출력 |
| `seqlen2.py` | `python seqlen2.py in.fasta` | 서열별 이름과 길이 출력 |
| `stats.py` | `python stats.py in.fasta` | `length_stats` 결과(개수, 전체/평균/최소/최대 길이) 출력 |
| `filter_fasta.py` | `python filter_fasta.py in.fasta 20 out.fasta` | 최소 길이 이상인 서열만 새 FASTA로 저장 (`int()` 변환 필요) |
| `summary.py` | `python summary.py in.fasta out.tsv` | 서열별 `name / length / gc`를 TSV로 저장 |
| `batchinfo.py` | `python batchinfo.py ../data out.tsv` | 폴더 안 모든 `.fasta`에 대해 `filename / count / total / mean_gc`를 TSV로 저장 (`os.listdir`, `os.path.join`) |

`filter.py`는 모듈화 이전 버전으로, 길이 20~40, GC 0.4~0.6, N 5개 미만 조건을 한 번에 거는 필터 예제다.

## 4. 결과 예시

`doc/summary.tsv`

| name | length | gc |
|------|--------|----|
| gene1 | 30 | 0.5 |
| gene2 | 15 | 0.4667 |
| gene3 | 22 | 0.5455 |

`doc/batchinfo.tsv`

| filename | count | total | mean_gc |
|----------|-------|-------|---------|
| noheader.fasta | 1 | 8 | 0.5 |
| seqs2.fasta | 2 | 16 | 0.25 |
| seqs.fasta | 3 | 67 | 0.504 |
| lower.fasta | 2 | 20 | 0.65 |

- `lower.fasta`: 소문자 서열도 `read_fasta`가 대문자로 바꾸므로 GC가 정상 계산된다.
- `noheader.fasta`: 헤더 앞의 서열 줄은 버려지고 `gene1` 하나만 읽힌다.
- `long.fasta`: `filter_fasta.py`로 길이 기준을 넘긴 gene1, gene3만 저장한 결과다.

## 5. 정리한 개념 (`python_cheatsheet.md`)

- **bash ↔ python 대응**: `echo`↔`print`, `${#SEQ}`↔`len(seq)`, `$1`↔`sys.argv[1]`, `$#`↔`len(sys.argv)-1`, `exit 1`↔`sys.exit(1)`
- bash는 정수만 다루지만 파이썬은 소수 계산과 `round()`가 가능하다.
- `from 모듈 import 함수`: 필요한 함수만 골라 가져온다.
- 파일 열기 모드: `"w"`는 덮어쓰기(bash `>`), `"a"`는 이어쓰기(bash `>>`)
- 겪은 오류
  - `TypeError`: 인자를 `int()`로 바꾸지 않음
  - `ZeroDivisionError`: 빈 서열로 GC 계산 → `gc_content`에 길이 0 검사 추가

## 기타

- `check_codespace.sh`: Codespace 환경(저장소, 폴더 구조, 도구 설치 여부)을 점검해 `doc/check_result.txt`로 저장하는 확인 스크립트
