# qual_by_position.py 사용법

FASTQ 파일의 모든 read 에서 같은 위치(1번째 염기, 2번째 염기, …)의 품질 점수를 모아
위치별 평균을 계산하고, 위치와 평균 품질을 탭으로 구분하여 출력한다.

## 실행

```
$ cd lab11/src
$ python3 qual_by_position.py <FASTQ 파일>
```

| 인자 | 설명 |
|------|------|
| `<FASTQ 파일>` | 읽을 FASTQ 파일 경로 (Phred+33) |

인자 개수가 틀리면 사용법을 출력하고 종료한다.

결과를 파일로 저장하려면 `>` 를 쓴다.

```
$ python3 qual_by_position.py ../data/SRR1553607_1.fastq > result.tsv
```

## 출력 예

```
$ python3 qual_by_position.py ../data/SRR1553607_1.fastq
위치	평균품질	read수
1	32.04	203445
2	32.17	203445
...
101	28.25	203445
```

| 열 | 내용 |
|----|------|
| `위치` | 염기 위치 (1 부터) |
| `평균품질` | 그 위치 품질 점수의 평균 (소수 둘째 자리) |
| `read수` | 그 위치에 염기가 있는 read 개수 |
