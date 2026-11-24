"""Prokka GFF 두 개의 CDS 개수, 평균 CDS 길이, hypothetical protein 비율, 코딩 밀도를 비교하여 TSV 로 저장한다.

사용법: python3 annot_compare.py <GFF1> <GFF2> <이름1> <이름2> <출력 .tsv 파일>
예:     python3 annot_compare.py ../doc/prokka_raw_out/raw.gff ../doc/prokka_trim_out/trim.gff 원본 트리밍 ../doc/annot_compare.tsv

코딩 밀도 = CDS 가 덮는 염기 수 / 전체 조립 길이.
CDS 끼리 겹치는 부분은 한 번만 센다.
"""
import sys
from parse_gff import read_gff, parse_attributes


def contig_lengths(filename):
    """GFF 의 ##sequence-region 줄에서 {contig: 길이} 를 읽는다."""
    lengths = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("##sequence-region"):
                cols = line.split()
                lengths[cols[1]] = int(cols[3])
            elif line.startswith("##FASTA"):
                break
    return lengths


def cds_stats(filename):
    """GFF 하나의 CDS 통계를 딕셔너리로 돌려준다."""
    lengths = contig_lengths(filename)
    genome = 0
    for c in lengths:
        genome = genome + lengths[c]

    # contig 마다 염기 하나에 칸 하나씩 만들고, CDS 가 덮는 칸을 True 로 표시한다
    covered = {}
    for c in lengths:
        covered[c] = [False] * lengths[c]

    n_cds = 0
    total_len = 0
    hypo = 0
    for f in read_gff(filename):
        if f["type"] != "CDS":
            continue
        n_cds = n_cds + 1
        total_len = total_len + (f["end"] - f["start"] + 1)
        if parse_attributes(f["attributes"]).get("product") == "hypothetical protein":
            hypo = hypo + 1
        for i in range(f["start"] - 1, f["end"]):     # GFF 1부터 → 파이썬 0부터
            covered[f["seqid"]][i] = True

    coding = 0
    for c in covered:
        coding = coding + covered[c].count(True)

    return {
        "CDS 개수": str(n_cds),
        "평균 CDS 길이 (bp)": f"{total_len / n_cds:.1f}",
        "hypothetical protein": f"{hypo} ({hypo / n_cds * 100:.1f}%)",
        "코딩 밀도": f"{coding / genome * 100:.1f}% ({coding}/{genome} bp)",
    }


if len(sys.argv) != 6:
    print("사용법: python3 annot_compare.py <GFF1> <GFF2> <이름1> <이름2> <출력 .tsv 파일>", file=sys.stderr)
    sys.exit(1)

# 첫 번째 인자를 GFF 로 둔 이유: parse_gff.py 를 가져올 때 그 파일 맨 아래 코드가
# sys.argv[1] 을 GFF 로 열기 때문이다.
name1 = sys.argv[3]
name2 = sys.argv[4]
stats1 = cds_stats(sys.argv[1])
stats2 = cds_stats(sys.argv[2])

lines = ["항목\t" + name1 + "\t" + name2]
for key in stats1:
    lines.append(key + "\t" + stats1[key] + "\t" + stats2[key])

with open(sys.argv[5], "w") as out:
    for line in lines:
        out.write(line + "\n")

for line in lines:
    print(line)
print("저장:", sys.argv[5])
