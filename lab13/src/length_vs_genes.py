"""contig 길이와 유전자 개수를 한 표로 모으고, 둘 사이의 상관계수를 계산한다.

사용법: python3 length_vs_genes.py <contigs FASTA> <contig_genes.tsv> <출력 .tsv 파일>
예:     python3 length_vs_genes.py ../data/contigs.fa ../doc/contig_genes.tsv ../doc/length_vs_genes.tsv

contig_genes.tsv 는 contig_genes.py 가 만든 파일이다 (첫 열 contig, 마지막 열 합계).
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta


def pearson(xs, ys):
    """두 수 목록의 피어슨 상관계수를 돌려준다."""
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxy = 0
    sxx = 0
    syy = 0
    for i in range(n):
        dx = xs[i] - mean_x
        dy = ys[i] - mean_y
        sxy = sxy + dx * dy
        sxx = sxx + dx * dx
        syy = syy + dy * dy
    return sxy / (sxx * syy) ** 0.5


if len(sys.argv) != 4:
    print("사용법: python3 length_vs_genes.py <contigs FASTA> <contig_genes.tsv> <출력 .tsv 파일>", file=sys.stderr)
    sys.exit(1)

# 1. 길이는 FASTA 서열에서 직접 잰다
seqs = read_fasta(sys.argv[1])

# 2. 유전자 개수는 contig_genes.tsv 의 마지막 열(합계)에서 읽는다
genes = {}
with open(sys.argv[2]) as f:
    f.readline()                       # 머리줄 건너뛰기
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if cols[0] == "전체":
            continue
        genes[cols[0]] = int(cols[-1])

# 3. 표 만들기: contig, 길이, 유전자 수, 1 kb 당 유전자 수
lengths = []
counts = []
lines = ["contig\t길이\t유전자수\t유전자/kb"]
for name in seqs:
    length = len(seqs[name])
    n = genes.get(name, 0)
    lengths.append(length)
    counts.append(n)
    lines.append(f"{name}\t{length}\t{n}\t{n / length * 1000:.2f}")

total_len = sum(lengths)
total_genes = sum(counts)
lines.append(f"전체\t{total_len}\t{total_genes}\t{total_genes / total_len * 1000:.2f}")

with open(sys.argv[3], "w") as out:
    for line in lines:
        out.write(line + "\n")

for line in lines:
    print(line)
print()

# 4. 상관계수: 전체 contig, 그리고 1 kb 이상 contig 만
print(f"피어슨 상관계수 (contig {len(lengths)}개): {pearson(lengths, counts):.3f}")

long_len = []
long_cnt = []
for i in range(len(lengths)):
    if lengths[i] >= 1000:
        long_len.append(lengths[i])
        long_cnt.append(counts[i])
print(f"피어슨 상관계수 (1 kb 이상 contig {len(long_len)}개): {pearson(long_len, long_cnt):.3f}")
print("저장:", sys.argv[3])
