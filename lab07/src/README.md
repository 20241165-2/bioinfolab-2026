# fasta.py 에 들어 있는 함수 목록

1) read_fasta
-> FASTA 파일을 읽어 각 서열의 이름(헤더)와 염기서열을 짝지어 {이름: 서열} 딕셔너리 형태로 돌려준다.
예시: seq_dict = read_fasta("sample.fasta")

2) gc_content
-> 서열(문자열)의 GC 비율을 0과 1 사이의 실수(소수)로 게산해 돌려준다.
예시: gc_ratio = gc_content("ATGCGC")

3) write_fasta
-> {이름: 서열} 딕셔너리와 저장할 파일 경로를 받아 FASTA 파일로 저장한다.
예시: write_fasta({"seq1": "ATGC"}, "output.fasta")

4) reverse_complement
-> 서열을 받아, 짝이 맞는 상보적 염기(A<->T, C<->G)로 교환한 뒤 순서를 거꾸로 뒤집은 역상보 서열을 돌려준다.
예시: rev_seq = reverse_complement("ATGC")

5) length_stats
-> 서열들이 들어있는 딕셔너리를 받아, 서열의 총 개수, 가장 짧은/긴 서열의 길이, 평균 길이 등의 통계 정보를 딕셔너리로 만들어 돌려준다. 
예시: stats = length_stats(seq_dict)

# 추가하고 싶은 함수
-> 염기서열의 T와 U를 변환해주는 함수