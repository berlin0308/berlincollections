ID = "A123456789"
firstcode = ord(ID[0])-55
"""A==65->10 B,C..."""
ID = str(firstcode)+ID[1:]
print("revised ID:",ID)

wlist = [1,9,8,7,6,5,4,3,2,1,1]
sum = 0
for i in range(11):
  sum += int(ID[i])*wlist[i]

print("The sum is",sum)
print("The remainder is",sum%10)

if sum%10 == 0:
  print("valid ID")
else:
  print("invalid")