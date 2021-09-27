info = str(input())
value = info.split(" ")
walls = int(value[0])
times = int(value[1])

wallist = [1]*walls
for a in range(times):
  string =str(input().strip())
  value = string.split(" ")
  i = int(value[0])
  f = int(value[1])
  col = int(value[2])
  for b in range(i,f+1):
    wallist[b]=col

print(wallist)
col2num = dict()

for c in range(1,10):
  for d in wallist :
    if d == c:
      if d not in col2num:
        col2num[d]=1
      else :
        col2num[d]+=1
      
print(col2num)
start = False
for color in range(1,10):
  if color in col2num and col2num[color]>0 :
    if start == False:
      start = True
    else :
      print(";",end="")
    print(col2num[color],color,end="")




