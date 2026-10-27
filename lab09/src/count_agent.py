import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <fasta_file>", file=sys.stderr)
    sys.exit(1)

count = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith(">"):
            count += 1

print(count)
