infos = str(input())
values = infos.split(",")

a = int(values[0]) #demand if free
b = float(values[1]) #increased sales when another price increases
c1 = int(values[2]) #cost
c2 = int(values[3]) 
n = int(values[4]) #round

p1=[0]*(n+1)
p2=[0]*(n+1)

def bestp1(currentp2):
  p1 = (a+b*currentp2+c1)/2
  return p1

def bestp2(currentp1):
  p2 = (a+b*currentp1+c2)/2
  return p2

def display(k,p1,p2):
  print("\nRound",k)
  print("p1:",p1)
  print("p2:",p2)

#Retailer1 comes first
p1[0]=bestp1(0) #p2 is supposed to be 0 initially
p2[0]=bestp2(p1[0])
display(0,p1[0],p2[0])

for i in range(1,n+1):
  p1[i] = bestp1(p2[i-1])
  p2[i] = bestp2(p1[i])
  display(i,p1[i],p2[i])
  
print("%0.2f %0.2f" % (p1[n], p2[n]))







