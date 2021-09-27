"""報童問題"""

c = int(input()) #cost
r = int(input()) #price
N = int(input()) #possibilities of demand
q = int(input()) #purchase
p0 = float(input())
p1 = float(input())
p2 = float(input())
p3 = float(input())
p4 = float(input())
p5 = float(input())
p6 = float(input())
p7 = float(input())
p8 = float(input())

min = 0
expect = 0.0
for i in range(N+1):
  if i<=q :
     min=i
  else :
     min=q
     
  if min == 0 and i<=q :
     expect += (r*min-c*q)*p0
     print(expect)
  elif min == 1 and i<=q :
      expect += (r*min-c*q)*p1
      print(expect)
  elif min == 2 and i<=q :
     expect += (r*min-c*q)*p2
     print(expect)
  elif min == 3 and i<=q :
     expect += (r*min-c*q)*p3
     print(expect)
  elif min == 4 and i<=q :
     expect += (r*min-c*q)*p4
     print(expect)
  elif min == 5 and i<=q :
     expect += (r*min-c*q)*p5
     print(expect)
  elif min == 6 and i<=q :
     expect += (r*min-c*q)*p6
     print(expect)
  elif min == 7 and i<=q :
     expect += (r*min-c*q)*p7
     print(expect)
  elif min == 8 and i<=q :
     expect += (r*min-c*q)*p8
     print(expect)
  else :
         if i==0 :
           expect += (r*min-c*q)*p0
           print(expect)
         elif i==1 :
           expect += (r*min-c*q)*p1
           print(expect)
         elif i==2 :
           expect += (r*min-c*q)*p2
           print(expect)
         elif i==3 :
           expect += (r*min-c*q)*p3
           print(expect)
         elif i==4 :
           expect += (r*min-c*q)*p4
           print(expect)
         elif i==5 :
           expect += (r*min-c*q)*p5
           print(expect)
         elif i==6 :
           expect += (r*min-c*q)*p6
           print(expect)
         elif i==7 :
           expect += (r*min-c*q)*p7
           print(expect)
         elif i==8 :
           expect += (r*min-c*q)*p8
           print(expect)

    
print(expect)
print(int(expect))
