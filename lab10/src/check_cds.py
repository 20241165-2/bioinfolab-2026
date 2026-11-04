"""rbcL GenBank 파일의 CDS 를 table=11 로 번역하여 /translation 과 비교한다.

사용법: python3 check_cds.py ../data
출력: 파일 이름, VERSION, ORGANISM, CDS 위치, 번역 일치 여부 (탭 구분)
"""
import sys
import os
from Bio import SeqIO

if len(sys.argv) != 2:
    print("사용법: python3 check_cds.py <데이터 폴더>", file=sys.stderr)
    sys.exit(1)

folder = sys.argv[1]

# rbcL_*.gb 파일 이름을 모아 정렬한다
names = []
for name in os.listdir(folder):
    if name.startswith("rbcL_") and name.endswith(".gb"):
        names.append(name)
names.sort()

print("파일\tVERSION\tORGANISM\tCDS위치\t번역일치")

for name in names:
    path = os.path.join(folder, name)
    for rec in SeqIO.parse(path, "genbank"):
        version = rec.id
        organism = rec.annotations.get("organism", "")
        for feature in rec.features:
            if feature.type != "CDS":
                continue
            location = str(feature.location)

            # CDS 서열을 꺼내고 codon_start 만큼 앞을 건너뛴다
            cds = feature.extract(rec.seq)
            codon_start = int(feature.qualifiers.get("codon_start", ["1"])[0])
            cds = cds[codon_start - 1:]
            # 부분 CDS 는 끝이 3의 배수가 아닐 수 있으므로 잘라 낸다
            cds = cds[:len(cds) - len(cds) % 3]

            protein = str(cds.translate(table=11, to_stop=True))
            given = feature.qualifiers.get("translation", [""])[0]

            if given == "":
                result = "translation없음"
            elif protein == given:
                result = "같음"
            else:
                result = "다름"
            print(f"{name}\t{version}\t{organism}\t{location}\t{result}")
