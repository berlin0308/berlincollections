"""基地臺位址選擇"""
x = [0]*1000
y = [0]*1000
P = [0]*1000
value = [" "]*3
alist = [0]
allP = 0

value = input().split()
n = int(value[0])
p = int(value[1])
d = int(value[2])

for t in range(1,n+1):
  value = input().split()
  x[t] = int(value[0])
  y[t] = int(value[1])
  P[t] = int(value[2])
  alist.append(t)
  

"""print("\nInitiatial condition:",alist)
print(x)
print(y)
print(P)"""
for k in range(p):
    
    max = 0        
    for i in alist : # 決定誰先
      totalP = 0
      if i==0:
        continue
      for j in alist :
        if (x[i]-x[j])**2+(y[i]-y[j])**2 <= d**2:
          totalP += P[j]
          
      #print(totalP)
      if totalP > max :
        max = totalP
        maxi = i

    
    
    print("\nWe choose",maxi,"\n")
    P[maxi]=0
    
    for j in alist :
        
        #print("We check",j)
        
        if ((x[maxi]-x[j])**2+(y[maxi]-y[j])**2)<= d*d:
          P[j]=0
          #print("Now",j,"is removed")
        
   
    print("\nWe have",max,"this round")
    allP += max
    print("\nNow",int(allP),"people are included\n")
