"""paired-end FASTQ 두 파일의 read 개수와 이름 짝을 확인한다.

사용법: python3 check_paired.py <파일_1.fastq> <파일_2.fastq>
"""

import sys


def base_name(header):
    """헤더 줄에서 read 이름(첫 단어)만 꺼낸다. '@' 는 뺀다."""
    return header.rstrip().split()[0][1:]


def is_pair(name1, name2):
    """두 이름이 짝인지 판단한다.

    1) 이름이 완전히 같으면 짝이다. (예: SRR1553607.1 / SRR1553607.1)
    2) 마지막 글자가 각각 1, 2 이고 그 앞이 '/' 또는 '.' 이며
       나머지 앞부분이 같으면 짝이다. (예: read7/1 / read7/2)
    """
    if name1 == name2:
        return True
    if len(name1) < 2 or len(name2) < 2:
        return False
    if name1[-1] != "1" or name2[-1] != "2":
        return False
    if name1[-2] not in "/." or name2[-2] not in "/.":
        return False
    return name1[:-2] == name2[:-2]


if len(sys.argv) != 3:
    print("사용법: python3 check_paired.py <파일_1.fastq> <파일_2.fastq>", file=sys.stderr)
    sys.exit(1)

file1 = open(sys.argv[1])
file2 = open(sys.argv[2])

count1 = 0
count2 = 0
bad = 0
max_show = 5

while True:
    header1 = file1.readline()
    header2 = file2.readline()

    # 한 read 의 나머지 세 줄(서열, +, 품질)은 건너뛴다
    for i in range(3):
        file1.readline()
        file2.readline()

    if header1 == "" and header2 == "":
        break
    if header1 != "":
        count1 = count1 + 1
    if header2 != "":
        count2 = count2 + 1
    if header1 == "" or header2 == "":
        continue  # 한쪽 파일만 끝났으면 개수만 센다

    name1 = base_name(header1)
    name2 = base_name(header2)
    if not is_pair(name1, name2):
        bad = bad + 1
        if bad <= max_show:
            print(f"짝이 안 맞음 ({count1}번째 read): {name1} / {name2}")

file1.close()
file2.close()

print(f"파일 1 read 개수: {count1}")
print(f"파일 2 read 개수: {count2}")

if count1 == count2:
    print("read 개수: 같음")
else:
    print("read 개수: 다름")

print(f"짝이 안 맞는 read 수: {bad}")

if count1 == count2 and bad == 0:
    print("결과: 두 파일은 올바른 paired-end 짝이다")
else:
    print("결과: 두 파일의 짝이 맞지 않는다")
    sys.exit(1)
