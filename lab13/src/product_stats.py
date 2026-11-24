"""GFF 파일의 CDS 주석에서 product, hypothetical protein, gene 이름 개수를 세어 표로 저장한다.

사용법: python3 product_stats.py <GFF 파일> <출력 .md 파일>
예:     python3 product_stats.py ../doc/prokka_out/sample.gff ../doc/product_stats.md
"""
import sys
from parse_gff import read_gff, parse_attributes

if len(sys.argv) != 3:
    print("사용법: python3 product_stats.py <GFF 파일> <출력 .md 파일>", file=sys.stderr)
    sys.exit(1)

features = read_gff(sys.argv[1])

total = 0          # 전체 CDS
with_product = 0   # product 가 있는 CDS
hypothetical = 0   # product 가 hypothetical protein 인 CDS
with_gene = 0      # gene 이름이 있는 CDS

for f in features:
    if f["type"] != "CDS":
        continue
    total = total + 1
    attrs = parse_attributes(f["attributes"])

    product = attrs.get("product", "")
    if product != "":
        with_product = with_product + 1
    if product == "hypothetical protein":
        hypothetical = hypothetical + 1

    if attrs.get("gene", "") != "":
        with_gene = with_gene + 1

if total == 0:
    print("CDS 주석이 없습니다.", file=sys.stderr)
    sys.exit(1)

rows = [
    ["전체 CDS", total],
    ["product 정보가 있는 CDS", with_product],
    ["product 가 hypothetical protein 인 CDS", hypothetical],
    ["gene 이름이 붙은 CDS", with_gene],
]

lines = []
lines.append("| 항목 | 개수 | 전체 CDS 대비 비율 |")
lines.append("|------|-----:|------:|")
for name, count in rows:
    lines.append(f"| {name} | {count} | {count / total * 100:.1f}% |")

with open(sys.argv[2], "w") as out:
    out.write("# " + sys.argv[1] + " CDS product 요약\n\n")
    for line in lines:
        out.write(line + "\n")

for line in lines:
    print(line)
print("저장:", sys.argv[2])
