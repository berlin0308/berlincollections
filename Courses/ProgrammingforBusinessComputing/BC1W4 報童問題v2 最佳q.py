"""報童問題"""
"""advance:找出最佳訂貨量q*使預期利潤最大化"""

c = int(input()) #cost
r = int(input()) #price
N = int(input()) #possibilities of demand
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
max = 0.0
bestq = 0
expect = 0.0
for q in range(N+1):
    expect = 0.0
    for i in range(N+1):
      if i<=q :
        min=i
      else :
        min=q
        
      if min == 0 and i<=q :
        expect += (r*min-c*q)*p0
        
      elif min == 1 and i<=q :
          expect += (r*min-c*q)*p1
          
      elif min == 2 and i<=q :
        expect += (r*min-c*q)*p2
        
      elif min == 3 and i<=q :
        expect += (r*min-c*q)*p3
        
      elif min == 4 and i<=q :
        expect += (r*min-c*q)*p4
        
      elif min == 5 and i<=q :
        expect += (r*min-c*q)*p5
        
      elif min == 6 and i<=q :
        expect += (r*min-c*q)*p6
       
      elif min == 7 and i<=q :
        expect += (r*min-c*q)*p7
        
      elif min == 8 and i<=q :
        expect += (r*min-c*q)*p8
        
      else :
            if i==0 :
              expect += (r*min-c*q)*p0
             
            elif i==1 :
              expect += (r*min-c*q)*p1
            
            elif i==2 :
              expect += (r*min-c*q)*p2
             
            elif i==3 :
              expect += (r*min-c*q)*p3
            
            elif i==4 :
              expect += (r*min-c*q)*p4
            
            elif i==5 :
              expect += (r*min-c*q)*p5
             
            elif i==6 :
              expect += (r*min-c*q)*p6
           
            elif i==7 :
              expect += (r*min-c*q)*p7
              
            elif i==8 :
              expect += (r*min-c*q)*p8
    print(expect)
    if expect > max :
      max = expect
      bestq = q        

print(bestq,int(max))

