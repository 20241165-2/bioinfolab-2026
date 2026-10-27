"""FASTA 파일을 받아 서열 개수를 출력한다."""
import os
import sys

# lab07/src 의 fasta.py 모듈을 불러온다
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta

if len(sys.argv) != 2:
    print(f"사용법: python3 {sys.argv[0]} <FASTA 파일>", file=sys.stderr)
    sys.exit(1)

seqs = read_fasta(sys.argv[1])
print(len(seqs))
