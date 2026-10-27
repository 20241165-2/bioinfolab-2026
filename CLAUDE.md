# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 이 저장소는

생물정보학실험 수업의 학생 실습 저장소이다. GitHub Codespaces 에서 작업한다.
소프트웨어 프로젝트가 아니므로 빌드 시스템, 패키지 목록, 테스트, 린터가 없다.
`labNN/` 폴더 하나가 한 주차의 실습이다.

설명, 주석, 커밋 메시지, 출력 문자열은 모두 한국어로 쓴다. 새로 만드는 것도 한국어로 맞춘다.

## 폴더 규칙

새 주차 폴더는 템플릿을 복사하여 만든다.

```
$ cp -r lab-template lab10
```

| 폴더 | 넣는 것 |
|------|---------|
| `data` | 내려받거나 만들어 낸 데이터 파일 (FASTA 등) |
| `doc` | 보고서, 결과 요약(`.md`, `.tsv`), 그림 |
| `src` | 학생이 직접 작성한 스크립트 (`.sh`, `.py`) |
| `resources/` | 강의자가 준 공용 연습 데이터(`resources/data/*.txt`, `seqs.fasta`)와 예제 스크립트 |

- 시퀀싱 데이터(`*.fastq`, `*.fq*`, `*.sra`), 조립·주석 결과 폴더(shovill, spades, prokka, flye), FastQC 보고서는 `.gitignore` 로 일부러 제외한다.
  필요하면 `wget` 으로 다시 내려받는다. 커밋하지 않는다.
- 한 주차 안에서 번호가 붙은 후속 스크립트가 생긴다(`countseq.py` → `countseq2.py`, 디버깅 실습 `bug1.sh` → `bug2.sh` …).
- 앞 주차 스크립트를 뒤 주차에서 다시 구현한다(lab05 셸 → lab06 파이썬 → lab07 모듈 사용).
- 예전 주차 폴더는 수업 진행 기록이다. 고치거나 합치지 않는다.

## 스크립트 실행

각 실습의 `src/` 에서 `python3` / `bash` 로 바로 실행한다. 경로는 `sys.argv` / `$1` 로 받는다.

```
$ cd lab07/src
$ python3 fasta.py ../data/seqs.fasta                  # 모듈 자체 확인 (길이/GC 출력, reverse_complement 검사)
$ python3 summary.py ../data/seqs.fasta ../doc/summary.tsv
$ python3 batchinfo.py ../data ../doc/batchinfo.tsv
```

lab07 스크립트들은 `from fasta import ...` 를 쓰므로 반드시 `lab07/src` 에서 실행한다(또는 `PYTHONPATH` 에 넣는다).
`fasta.py` 의 함수 목록(`read_fasta`, `gc_content`, `write_fasta`, `reverse_complement`, `length_stats`)은 `lab07/src/README.md` 에 있다.

`lab*/src/check_codespace.sh` 는 실습 폴더에서 `bash src/check_codespace.sh` 로 실행하며, 저장소·폴더·도구 확인 결과를 `doc/check_result.txt` 에 저장한다.
`.devcontainer/check.sh` 는 Codespace 를 열 때 설치된 도구를 보여 준다.

## 환경

`.devcontainer/` 에 설정이 네 개 있고, Codespace 를 만들 때 주차에 맞게 고른다.

| 주차 | 설정 | 들어 있는 것 |
|------|------|--------------|
| 02~07 | `1-basic` | 파이썬, 리눅스 기본 명령어 |
| conda 실습 | `2-conda` | micromamba 만 (패키지는 직접 설치) |
| 08~09, 12~14 | `3-seq` | seqkit, blast, mafft, iqtree, fastqc, fastp |
| 10~11 | `4-genome` | 위 + shovill, prokka |

- `$MYHOME` 은 작업 폴더 루트이며, 인자 없는 `cd` 는 그곳으로 돌아온다. 진짜 홈은 `cd ~` 이다.
- 필요한 도구가 없으면 직접 설치하지 않고 강의자에게 알린다. conda 실습 주차만 예외이다.

## 코드 스타일

수업 수준의 초보자 문법에 맞춘다.

- `sys.argv` 를 쓰는 단순한 최상위 스크립트, 명시적인 반복문, 문자열 연결 또는 f-string, 짧은 한국어 docstring.
- 인자 개수가 틀리면 사용법을 `stderr` 로 출력하고 `exit 1` 한다.
- 요청이 없으면 argparse, 클래스, 외부 라이브러리 등 수업에서 다루지 않은 것은 쓰지 않는다.

## FASTA 파일을 읽을 때 어떤 함수를 쓸 것인가
- `read_fasta`로 읽는다. 파싱 코드를 새로 만들지 않는다.

## 새 라이브러리를 쓰기 전에 어떻게 할 것인가
- 새 라이브러리(Biopython 등)는 쓰기 전에 먼저 물어본다. 설치도 하지 않는다.

## 하지 말아야 할 명령어
- 'pip install', 'apt', 'sudo' 같은 설치와 git push, git reset은 거절한다.

## 추가 규칙
- 요청한 부분만 고친다. 필요해보이는 부분은 제안한다.