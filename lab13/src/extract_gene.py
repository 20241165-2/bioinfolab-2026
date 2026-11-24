"""GFF3 주석의 좌표로 contig 에서 유전자 서열을 잘라 FASTA 형식으로 출력한다.

사용법: python3 extract_gene.py <GFF 파일> <FASTA 파일> <유전자 이름 또는 ID>
예:     python3 extract_gene.py ../doc/prokka_out/sample.gff ../data/contigs.fa deoB
"""
import os
import sys

# lab07 의 fasta 모듈을 가져온다 (lab09 count_agent2.py 와 같은 방법)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta, reverse_complement

# 이 키들의 값 가운데 하나가 입력과 같으면 찾는 주석으로 본다
KEYS = ["ID", "Name", "gene", "locus_tag"]


def parse_attributes(text):
    """GFF 9번째 열(key=value;key=value)을 딕셔너리로 바꾼다."""
    attrs = {}
    for item in text.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            attrs[key] = value
    return attrs


def find_features(filename, query):
    """GFF 파일에서 이름이나 ID 가 query 와 같은 주석을 모두 찾아 리스트로 돌려준다."""
    found = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("##FASTA"):
                break
            if line.startswith("#") or line == "":
                continue

            cols = line.split("\t")
            if len(cols) < 9:
                continue

            attrs = parse_attributes(cols[8])
            for key in KEYS:
                if attrs.get(key) == query:
                    found.append({
                        "seqid": cols[0],
                        "type": cols[2],
                        "start": int(cols[3]),
                        "end": int(cols[4]),
                        "strand": cols[6],
                        "attrs": attrs,
                    })
                    break
    return found


if len(sys.argv) != 4:
    print("사용법: python3 extract_gene.py <GFF 파일> <FASTA 파일> <유전자 이름 또는 ID>", file=sys.stderr)
    sys.exit(1)

gff_file = sys.argv[1]
fasta_file = sys.argv[2]
query = sys.argv[3]

features = find_features(gff_file, query)
if len(features) == 0:
    print("'" + query + "' 에 해당하는 주석이 없습니다.", file=sys.stderr)
    sys.exit(1)

seqs = read_fasta(fasta_file)

for feat in features:
    seqid = feat["seqid"]
    start = feat["start"]
    end = feat["end"]
    strand = feat["strand"]

    if seqid not in seqs:
        print("FASTA 에 " + seqid + " 서열이 없습니다.", file=sys.stderr)
        sys.exit(1)

    # GFF3 좌표는 1부터 시작하고 끝을 포함한다.
    # 파이썬 슬라이스는 0부터 시작하고 끝을 포함하지 않으므로 [start-1:end] 로 자른다.
    sub = seqs[seqid][start - 1:end]

    # 역방향(-) 주석은 역상보 서열로 바꿔야 5'→3' 유전자 서열이 된다.
    if strand == "-":
        sub = reverse_complement(sub)

    # 머리줄: >ID 이름 seqid:start-end(strand)
    header = ">" + feat["attrs"].get("ID", query)
    if "Name" in feat["attrs"]:
        header = header + " " + feat["attrs"]["Name"]
    header = header + " " + seqid + ":" + str(start) + "-" + str(end) + "(" + strand + ")"
    print(header)

    # 한 줄에 60 염기씩 출력한다
    for i in range(0, len(sub), 60):
        print(sub[i:i + 60])
