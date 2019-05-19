n = int(input("学生数量："))
max_chengji = 0
for i in range(1,n+1):
    chengji = float(input("成绩："))
    if max_chengji < chengji:
        max_chengji = chengji
print(max_chengji)
