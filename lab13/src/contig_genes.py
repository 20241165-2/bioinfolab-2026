"""GFF 파일의 첫 번째 열(seqid)을 기준으로 contig 마다 유전자(CDS, tRNA 등)가 몇 개인지 세어 TSV 로 저장한다.

사용법: python3 contig_genes.py <GFF 파일> <출력 .tsv 파일>
예:     python3 contig_genes.py ../doc/prokka_out/sample.gff ../doc/contig_genes.tsv
"""
import sys
from parse_gff import read_gff

if len(sys.argv) != 3:
    print("사용법: python3 contig_genes.py <GFF 파일> <출력 .tsv 파일>", file=sys.stderr)
    sys.exit(1)

gff_file = sys.argv[1]

# 1. ##sequence-region 줄에서 contig 이름과 길이를 순서대로 읽는다.
#    유전자가 하나도 없는 contig 도 표에 0 으로 넣기 위해서이다.
contigs = []
lengths = {}
with open(gff_file) as f:
    for line in f:
        if line.startswith("##sequence-region"):
            cols = line.split()
            contigs.append(cols[1])
            lengths[cols[1]] = int(cols[3])
        elif line.startswith("##FASTA"):
            break

# 2. 주석을 contig 별, 종류(type)별로 센다. counts[contig][type] = 개수
features = read_gff(gff_file)
counts = {}
types = []
for c in contigs:
    counts[c] = {}

for feat in features:
    seqid = feat["seqid"]
    t = feat["type"]
    if seqid not in counts:          # sequence-region 에 없던 contig
        contigs.append(seqid)
        lengths[seqid] = 0
        counts[seqid] = {}
    if t not in types:
        types.append(t)
    counts[seqid][t] = counts[seqid].get(t, 0) + 1

# 3. 표를 만든다: contig, 길이, 종류별 개수, 합계
header = ["contig", "길이"] + types + ["합계"]
lines = ["\t".join(header)]
total_by_type = {}
for c in contigs:
    row = [c, str(lengths[c])]
    row_sum = 0
    for t in types:
        n = counts[c].get(t, 0)
        row.append(str(n))
        row_sum = row_sum + n
        total_by_type[t] = total_by_type.get(t, 0) + n
    row.append(str(row_sum))
    lines.append("\t".join(row))

total_len = 0
for c in contigs:
    total_len = total_len + lengths[c]
last = ["전체", str(total_len)]
grand = 0
for t in types:
    last.append(str(total_by_type.get(t, 0)))
    grand = grand + total_by_type.get(t, 0)
last.append(str(grand))
lines.append("\t".join(last))

with open(sys.argv[2], "w") as out:
    for line in lines:
        out.write(line + "\n")

for line in lines:
    print(line)
print("저장:", sys.argv[2])
