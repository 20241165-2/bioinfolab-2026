"""GFF 파일에서 CDS 주석만 골라 길이 통계와 방향별 개수를 출력한다."""
import sys
from parse_gff import read_gff

if len(sys.argv) != 2:
    print("사용법: python3 gene_stats.py <GFF 파일>", file=sys.stderr)
    sys.exit(1)

features = read_gff(sys.argv[1])

# type 이 CDS 인 주석만 고르고 길이를 붙인다
cds_list = []
for f in features:
    if f["type"] == "CDS":
        f["length"] = f["end"] - f["start"] + 1
        cds_list.append(f)

if len(cds_list) == 0:
    print("CDS 주석이 없습니다.")
    sys.exit(0)

# 길이 통계
total = 0
min_len = cds_list[0]["length"]
max_len = cds_list[0]["length"]
for c in cds_list:
    total = total + c["length"]
    if c["length"] < min_len:
        min_len = c["length"]
    if c["length"] > max_len:
        max_len = c["length"]

# 방향별 개수
plus = 0
minus = 0
for c in cds_list:
    if c["strand"] == "+":
        plus = plus + 1
    elif c["strand"] == "-":
        minus = minus + 1

print("== CDS 통계 ==")
print(f"개수: {len(cds_list)}")
print(f"총 길이: {total} bp")
print(f"평균 길이: {total / len(cds_list):.1f} bp")
print(f"최소 길이: {min_len} bp")
print(f"최대 길이: {max_len} bp")
print(f"정방향(+): {plus}")
print(f"역방향(-): {minus}")

# 가장 긴 CDS 다섯 개
cds_list.sort(key=lambda c: c["length"], reverse=True)
print()
print("== 가장 긴 CDS 5개 ==")
for c in cds_list[:5]:
    print(f"{c['seqid']}\t{c['start']}\t{c['end']}\t{c['strand']}\t{c['length']}\t{c['attributes']}")
