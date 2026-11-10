"""FASTQ 파일의 각 read 마다 GC 비율과 평균 품질을 계산하고,
GC 비율이 가장 높은 read 10개와 가장 낮은 read 10개의 평균 품질을 전체 평균과 비교한다."""
import sys

if len(sys.argv) != 2:
    print("사용법: python3 gc_content.py <FASTQ 파일>", file=sys.stderr)
    sys.exit(1)

N = 10  # 고를 read 개수


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 목록을 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def gc_ratio(seq):
    """서열의 GC 비율(%)을 돌려준다. N 은 분모에서 뺀다. A/T/G/C 가 없으면 -1."""
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    atgc = gc + seq.count("A") + seq.count("T")
    if atgc == 0:
        return -1
    return gc / atgc * 100


def mean_quality(qual):
    """품질 문자열의 평균 Phred 점수(Phred+33)를 돌려준다."""
    total = 0
    for ch in qual:
        total = total + (ord(ch) - 33)
    return total / len(qual)


def average_quality(rows):
    """(GC, 이름, 평균품질) 목록에서 평균품질의 평균을 돌려준다."""
    total = 0
    for gc, name, q in rows:
        total = total + q
    return total / len(rows)


def print_rows(title, rows):
    """고른 read 목록을 표로 출력한다."""
    print(title)
    print("read\tGC(%)\t평균품질")
    for gc, name, q in rows:
        print(f"{name}\t{gc:.2f}\t{q:.2f}")
    print()


reads = read_fastq(sys.argv[1])

# read 마다 (GC 비율, 이름, 평균 품질) 를 만든다.
# 이름을 두 번째에 두어 GC 가 같을 때 품질이 아니라 이름 순서로 정렬되게 한다.
results = []
skipped = 0
for name, seq, qual in reads:
    gc = gc_ratio(seq)
    if gc < 0:
        skipped = skipped + 1
        continue
    short_name = name.split()[0]  # "SRR1553607.1 1 length=101" → "SRR1553607.1"
    results.append((gc, short_name, mean_quality(qual)))

results.sort()
low = results[:N]
high = results[-N:]
high.reverse()

all_q = average_quality(results)
low_q = average_quality(low)
high_q = average_quality(high)

print("read 개수:", len(results))
if skipped > 0:
    print("A/T/G/C 가 없어 뺀 read 수:", skipped)
print()
print_rows(f"[GC 비율이 가장 높은 read {N}개]", high)
print_rows(f"[GC 비율이 가장 낮은 read {N}개]", low)

print("[평균 품질 비교]")
print("그룹\t평균품질\t전체와의 차이")
print(f"전체\t{all_q:.2f}\t0.00")
print(f"GC 높음\t{high_q:.2f}\t{high_q - all_q:+.2f}")
print(f"GC 낮음\t{low_q:.2f}\t{low_q - all_q:+.2f}")
