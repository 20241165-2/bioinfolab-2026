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
 
seq = sys.argv[1].upper()
rc_seq = reverse_complement(seq)
 
# 정방향 틀 +1, +2, +3
for frame in [0, 1, 2]:
    orfs = find_orfs(seq, frame)
    print("틀 +" + str(frame + 1), ":", orfs)
    for s, e in orfs:
        print("   ", seq[s:e], "길이", e - s)
 
# 역상보 틀 -1, -2, -3 (위치는 역상보 서열 기준)
for frame in [0, 1, 2]:
    orfs = find_orfs(rc_seq, frame)
    print("틀 -" + str(frame + 1), ":", orfs)
    for s, e in orfs:
        print("   ", rc_seq[s:e], "길이", e - s)
