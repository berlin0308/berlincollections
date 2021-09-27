import matplotlib.pyplot as py

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

def printp(k,p1,p2):
  print("\nRound",k)
  print("p1:",p1)
  print("p2:",p2)

def showline(x1,y1,x2,y2,color):
  if color == "blue":
    py.plot([x1,x2],[y1,y2],"b")
  if color == "red":
    py.plot([x1,x2],[y1,y2],"r")
  if color == "--":
    py.plot([x1,x2],[y1,y2],"k--")
  if color == "black":
    py.plot([x1,x2],[y1,y2],"k")

#Retailer1 comes first
p1[0]=bestp1(0) #p2 is supposed to be 0 initially
p2[0]=bestp2(p1[0])
printp(0,p1[0],p2[0])

for i in range(1,n+1):
  p1[i] = bestp1(p2[i-1])
  p2[i] = bestp2(p1[i])
  printp(i,p1[i],p2[i])
  py.plot([p1[i]],[p2[i-1]],"bo")
  py.plot([p1[i]],[p2[i]],"ro")
  
#print("%0.2f %0.2f" % (p1[n], p2[n]))

#showline(-10,0,max((a-c1)/b,(a-c2)/b)*1.5,0,"--")
#showline(0,-10,0,max(bestp1(0),bestp2(0))*1.5,"--")
#showline(0,bestp1(0),(a-c1)/b,0,"blue")
#showline(0,bestp2(0),(a-c2)/b,0,"red")

showline(p1[1],p2[0],p1[1],p2[1],"black")
for i in range(2,n+1):
  #showline(p1[i-1],p2[i-1],p1[i],p2[i-1],"red")
  #showline(p1[i],p2[i-1],p1[i],p2[i],"blue")
  showline(p1[i-1],p2[i-2],p1[i],p2[i-1],"blue")
  showline(p1[i-1],p2[i-1],p1[i],p2[i],"red")
  showline(p1[i-1],p2[i-1],p1[i],p2[i-1],"black")
  showline(p1[i],p2[i-1],p1[i],p2[i],"black")
  
m1 = (p2[n-1]-p2[0])/(p1[n]-p1[1])
s1 = (p1[n]-p1[1])/5
showline(p1[1]-s1,p2[0]-m1*s1,p1[n]+s1,p2[n]+m1*s1,"blue")
  
m2 = (p2[n]-p2[0])/(p1[n]-p1[0])
s2 = (p1[n]-p1[1])/5
showline(p1[0]-s2,p2[0]-m2*s2,p1[n]+s2,p2[n]+m2*s2,"red")

py.show()




