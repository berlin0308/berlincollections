#該怎麼找錢

"""如果你在一家零售店幫消費的客人結帳，你可能需要快速地挑出合適且數量正確的鈔票與零錢。假設客人的消費金額 aa 一定是 1 到 1000 之間的整數，而你有無限量的 500、100、50、10、5、1 這些面額的鈔票和零錢 """

a=int(input())
w=str((1000-a)//500)
a=(1000-a)%500
x=str(a//100)
a=a%100
y=str(a//50)
a=a%50
z=str(a//10)
a=a%10
r=str(a//5)
a=str(a%5)

head = False

if w!="0":
  print("500, "+w,end='')
  head = True

if x!="0":
  if head == True :
     print("; ",end='')
  print("100, "+x,end='')
  head = True

if y!="0":
  if head == True :
     print("; ",end='')
  print("50, "+y,end='')
  head = True

if z!="0":
  if head == True :
     print("; ",end='')
  print("10, "+z,end='')
  head = True

if r!="0":
  if head == True :
     print("; ",end='')
  print("5, "+r,end='')
  head = True

if a!="0":
  if head == True :
     print("; ",end='')
  print("1, "+a,end='')
  head = True