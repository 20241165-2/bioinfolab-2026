"""FASTQ 파일을 읽어 위치(염기 번호)별 평균 품질 점수를 출력한다."""
import sys

if len(sys.argv) != 2:
    print("사용법: python3 qual_by_position.py <FASTQ 파일>", file=sys.stderr)
    sys.exit(1)


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 목록을 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


reads = read_fastq(sys.argv[1])

# 위치마다 품질 점수 합계와 염기 개수를 모은다.
# read 길이가 서로 다를 수 있으므로(트리밍 후) 목록을 필요한 만큼 늘린다.
totals = []
counts = []
for name, seq, qual in reads:
    for i in range(len(qual)):
        if i >= len(totals):
            totals.append(0)
            counts.append(0)
        totals[i] = totals[i] + (ord(qual[i]) - 33)
        counts[i] = counts[i] + 1

# 위치별 평균 = 그 위치 품질 점수 합계 / 그 위치에 염기가 있는 read 수
# (FastQC 의 Per base sequence quality 에서 Mean 과 같은 계산)
print("위치\t평균품질")
for i in range(len(totals)):
    mean = totals[i] / counts[i]
    print(f"{i + 1}\t{mean}")
