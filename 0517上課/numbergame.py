import random
min = 1
max = 99
ans = random.randint(min,max)
count = 0
while True:
  guess = int(input(f"請輸入{min}到{max}："))
  count += 1
  if ans == guess:
    break
  elif ans < guess:
    print(f"答錯了，現在總共猜了{count}次\n")
    max = guess - 1
  elif ans > guess:
    print(f"答錯了，現在總共猜了{count}次\n")
    min = guess + 1
print(f"你答對了！你總共猜了{count}次！")