import sys
 
def read_gff(filename):
    features = []
 
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
 
            feature = {
                "seqid": cols[0],
                "type": cols[2],
                "start": int(cols[3]),
                "end": int(cols[4]),
                "strand": cols[6],
                "attributes": cols[8]
            }
            features.append(feature)
 
    return features

# GFF3 에서 값 안에 쓸 수 없는 글자는 %16진수 로 적는다 (예: 쉼표 → %2C)
ESCAPES = {"%3B": ";", "%3D": "=", "%26": "&", "%2C": ",", "%09": "\t", "%25": "%"}

def parse_attributes(text):
    """GFF3 9번째 열(이름=값;이름=값;...)을 {이름: 값} 딕셔너리로 바꾼다."""
    attrs = {}
    for item in text.split(";"):
        if "=" not in item:          # 빈 칸이나 = 없는 조각은 건너뛴다
            continue
        key, value = item.split("=", 1)   # 첫 번째 = 에서만 나눈다
        for code in ESCAPES:              # %2C 같은 표기를 원래 글자로 되돌린다 (%25 는 마지막)
            value = value.replace(code, ESCAPES[code])
        attrs[key] = value
    return attrs

features = read_gff(sys.argv[1])
print("주석 개수:", len(features))
print("첫 주석:", features[0])
