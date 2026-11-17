"""길이가 L 인 서열에서 나올 수 있는 k-mer 의 개수를 계산하고 확인한다."""


def count_kmers(L, k):
    """길이 L 인 서열의 k-mer 개수(L - k + 1)를 돌려준다. k 가 L 보다 크면 0 이다."""
    if k > L:
        return 0
    return L - k + 1


def count_by_sliding(L, k):
    """공식을 쓰지 않고, 길이 L 인 서열에서 k-mer 를 하나씩 잘라 직접 센다."""
    seq = "A" * L
    count = 0
    start = 0
    while start + k <= len(seq):
        kmer = seq[start:start + k]
        if len(kmer) == k:
            count = count + 1
        start = start + 1
    return count


# (L, k, 손으로 센 개수)
tests = [
    (10, 5, 6),    # kmers.py 의 TATGGGGTGC 에서 5-mer 6개
    (10, 1, 10),   # 1-mer 는 염기 개수와 같다
    (10, 10, 1),   # k = L 이면 서열 전체 하나
    (10, 11, 0),   # k > L 이면 하나도 없다
    (7, 3, 5),
    (3, 5, 0),
    (1, 1, 1),
    (100, 21, 80),
]

all_ok = True
print("L\tk\t손계산\t직접세기\tcount_kmers\t결과")
for L, k, by_hand in tests:
    by_loop = count_by_sliding(L, k)
    by_func = count_kmers(L, k)
    if by_hand == by_loop and by_loop == by_func:
        result = "일치"
    else:
        result = "불일치"
        all_ok = False
    print(f"{L}\t{k}\t{by_hand}\t{by_loop}\t\t{by_func}\t\t{result}")

if all_ok:
    print("모든 조합에서 일치한다.")
else:
    print("일치하지 않는 조합이 있다.")
