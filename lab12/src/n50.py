import sys
 
def read_fasta(filename):
    seqs = {}
    name = None
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = ""
            else:
                seqs[name] = seqs[name] + line
    return seqs
 
def n50(lengths):
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    half = total / 2
 
    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length
 
def write_lengths(lengths, filename):
    """contig 길이를 내림차순으로 정렬하여 한 줄에 하나씩 저장한다."""
    lengths = sorted(lengths, reverse=True)
    with open(filename, "w") as f:
        for length in lengths:
            f.write(str(length) + "\n")

if len(sys.argv) != 3:
    print("사용법: python3 n50.py contigs.fa contig_lengths.txt", file=sys.stderr)
    sys.exit(1)

seqs = read_fasta(sys.argv[1])
lengths = []
for name in seqs:
    lengths.append(len(seqs[name]))

print("contig 개수:", len(lengths))
print("전체 길이:", sum(lengths))
print("가장 긴 contig:", max(lengths))
print("N50:", n50(lengths))

write_lengths(lengths, sys.argv[2])
print("contig 길이 저장:", sys.argv[2])
