import sys

filename = sys.argv[1]   # 검사 없이 바로 받기

names = []
total = 0

with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            names.append(name)
        else:
            total = total + len(line)

print("파일:", filename)
print("서열 개수:", len(names))
print("서열 이름:")
for name in names:
    print(" " + name)
print("총 염기 수:", total)