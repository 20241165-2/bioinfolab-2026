import sys
 
STOPS = ["TAA", "TAG", "TGA"]
 
def find_orfs(seq, frame):
    orfs = []
    start = None
 
    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i + 3]
 
        if codon == "ATG" and start is None:
            start = i
        elif codon in STOPS and start is not None:
            orfs.append((start, i + 3))
            start = None
 
    return orfs
 
def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다. A/T/G/C 가 아닌 염기는 N 으로 바꾼다."""
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result = ""
    for base in seq:
        result = result + complement.get(base, "N")
    return result[::-1]
 
def to_original(s, e, strand, length):
    """find_orfs 가 준 위치(0부터, 끝 미포함)를 원래 서열 기준 1부터 시작하는 좌표(끝 포함)로 바꾼다.
    - 가닥이면 역상보 서열의 위치를 원래 서열 위치로 뒤집는다. 항상 시작 < 끝 이 되게 돌려준다."""
    if strand == "+":
        return s + 1, e
    else:
        return length - e + 1, length - s

seq = sys.argv[1].upper()
rc_seq = reverse_complement(seq)
length = len(seq)

# 정방향 틀 +1, +2, +3 과 역상보 틀 -1, -2, -3 을 같은 방식으로 검사한다.
# 좌표는 모두 원래 서열 기준(1부터, 끝 포함)이고, 가닥(+/-)을 함께 적는다.
for strand in ["+", "-"]:
    if strand == "+":
        target = seq
    else:
        target = rc_seq

    for frame in [0, 1, 2]:
        orfs = find_orfs(target, frame)
        print("틀 " + strand + str(frame + 1), ": ORF", len(orfs), "개")
        for s, e in orfs:
            start, end = to_original(s, e, strand, length)
            print("    " + str(start) + "-" + str(end), "(" + strand + ")", "길이", e - s)
            print("   ", target[s:e])
