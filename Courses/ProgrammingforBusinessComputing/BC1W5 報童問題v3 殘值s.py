"""報童問題 v3"""
"""新增殘值s設定，多進貨沒賣出的可以回收換錢"""


c = int(input())
r = int(input())
N = int(input())
s = int(input())
p = []  #p = [0.0]*1000
max = 0.0
maxq = 0

for i in range(0,N+1):
  p.append(float(input()))
  
#for i in range(0,N+1):
#  p[i] = float(input())

for q in range(0,N+1):
  expect = 0.0
  for D in range(0,N+1):
    if D <= q :
      expect += (r*D-q*c+(q-D)*s)*p[D]
    else :
      expect += (r*q-q*c)*p[D]
  print(expect)
  if expect > max :
    max = expect
    maxq = q

print(maxq,int(max))

