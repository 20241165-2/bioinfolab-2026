import sys
import os
from fasta import read_fasta, gc_content, length_stats

folder = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, "w") as out:
    out.write("filename\tcount\ttotal\tmean_gc\n")
    for fname in os.listdir(folder):
        if fname.endswith(".fasta"):
            path = os.path.join(folder, fname)
            seqs = read_fasta(path)
            stats = length_stats(seqs)
            gc_values = [gc_content(seqs[name]) for name in seqs]
            mean_gc = round(sum(gc_values) / len(gc_values), 3)
            out.write(f"{fname}\t{stats['count']}\t{stats['total']}\t{mean_gc}\n")

print("완료!")