# 트리밍 전과 후 조립 결과의 Prokka 주석 비교

## 실행 조건

| 조건 | 조립 결과 (lab12) | Prokka 출력 |
|------|------------------|-------------|
| 원본 | `lab12/doc/shovill_out/contigs.fa` | `doc/prokka_raw_out/` |
| 트리밍 (`fastp -q 20 -l 50`) | `lab12/doc/shovill_trim_out/contigs.fa` | `doc/prokka_trim_out/` |

```
$ cd lab13
$ prokka --outdir doc/prokka_raw_out  --prefix raw  --cpus 4 ../lab12/doc/shovill_out/contigs.fa
$ prokka --outdir doc/prokka_trim_out --prefix trim --cpus 4 ../lab12/doc/shovill_trim_out/contigs.fa
$ cd src
$ python3 annot_compare.py ../doc/prokka_raw_out/raw.gff ../doc/prokka_trim_out/trim.gff 원본 트리밍 ../doc/annot_compare.tsv
```

- contig 개수와 N50 은 lab12 `doc/trim_compare.md` 에 적어 둔 값을 재사용하였다.
  (`lab12/src/n50.py` 로 다시 실행해도 같은 값이 나왔다.)
- 원본 쪽 조립은 이번 주 `data/contigs.fa` 와 같은 파일이다.

## 결과

| 항목 | 원본 | 트리밍 |
|------|-----:|-------:|
| contig 개수 | 12 | 12 |
| N50 (bp) | 58,878 | 58,878 |
| 전체 길이 (bp) | 180,912 | 180,912 |
| CDS 개수 | 149 | 149 |
| 평균 CDS 길이 (bp) | 1,008.4 | 1,008.4 |
| hypothetical protein | 60 (40.3%) | 60 (40.3%) |
| 코딩 밀도 | 82.9% | 82.9% |

- 코딩 밀도 = CDS 가 덮는 염기 수 / 전체 조립 길이. CDS 끼리 겹치는 부분은 한 번만 세었다 (150,060 / 180,912 bp).
  겹침을 무시하고 CDS 길이를 그냥 더하면 150,246 bp (83.0%) 로, 겹치는 부분은 186 bp 이다.
- tRNA 는 두 결과 모두 2개, rRNA 는 0개이다.

## 숫자는 같지만 완전히 같지는 않다

1. **염기 3개가 다르다.** 두 조립의 contig 서열을 한 글자씩 비교하면 3곳이 다르다.

   | contig | 위치 | 원본 | 트리밍 | 들어 있는 CDS |
   |--------|-----:|:----:|:------:|---------------|
   | contig00001 | 13,703 | C | T | hypothetical protein (13,525-14,763, −) |
   | contig00003 | 21 | C | A | DnaA (8-1,342, +) |
   | contig00003 | 22 | T | G | DnaA (8-1,342, +) |

   그래서 이 두 CDS 의 단백질 서열이 조금 다르다. 길이와 product 는 같아서 위 표의 숫자에는 드러나지 않는다.
   shovill 의 마지막 단계(Pilon 오류 교정)가 입력 리드에 따라 고친 곳이 조금 달라서 생긴 차이로 보인다.

2. **contig00004 의 방향이 반대이다.** 트리밍 쪽 contig00004 는 원본의 역상보 서열이다.
   그래서 같은 유전자 세 개(ipdC, hypothetical protein, ptsG)가 좌표와 가닥만 뒤집혀 나온다.
   어셈블러는 contig 를 어느 방향으로 써도 되므로 생물학적으로는 같은 결과이다.

## 해석

이 데이터에서는 트리밍이 주석 결과를 바꾸지 않았다.
lab12 에서 본 것처럼 fastp `-q 20 -l 50` 은 리드를 하나도 버리지 않았고 염기도 96개만 잘랐다.
그래서 조립이 거의 같았고, 주석도 유전자 수, 길이, 기능 이름이 모두 같았다.
남은 차이(염기 3개, contig 하나의 방향)는 조립 품질의 차이가 아니라 오류 교정과 출력 방향의 사소한 차이이다.
