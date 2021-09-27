class grade:
  
  def __init__(self, subTime, problem, status):
      self.subTime = subTime
      self.problem = problem
      self.status = status
  
  def count(self):
      if self.status=='Accepted':
        return 0
      if self.status=='Compile Error':
        return 1
      if self.status=='Runtime Error':
        return 2
      if self.status=='Time Limit Exceed':
        return 3
      if self.status=='Wrong Answer':
        return 4

# read input data and change str to datetime
timeInverval = input().split(' ')
import datetime
start = datetime.datetime.strptime(timeInverval[0], '%H:%M:%S')
end = datetime.datetime.strptime(timeInverval[1], '%H:%M:%S')

# initialize
midtermDict = dict()
      
# read csv file
import csv
midtermFile = 'BC-midterm2csv.csv'
fh1 = open(midtermFile, 'r', newline = '')
reader1 = csv.DictReader(fh1)
for row in reader1:
    thetime = datetime.datetime.strptime(row['SubmissionTime'], '%H:%M:%S')
    g = grade(thetime, int(row['Problem']), str(row['Status']))
    if g.problem not in midtermDict:
        midtermDict[g.problem] = list()
    if start <= g.subTime <= end:
        num=g.count()        
        midtermDict[g.problem].append(num)

fh1.close()

print("Problem     A C R T W")
# print the output
for i in range(1, len(midtermDict) + 1):
  Accepted=0
  CompileError=0
  RuntimeError=0
  TimeLimitExceed=0
  WrongAnswer=0
  for j in range(0,len(midtermDict[i])):
    
    if midtermDict[i][j]==0:
      Accepted+=1
    if midtermDict[i][j]==1:
      CompileError+=1
    if midtermDict[i][j]==2:
      RuntimeError+=1
    if midtermDict[i][j]==3:
      TimeLimitExceed+=1
    if midtermDict[i][j]==4:
      WrongAnswer+=1
    
  print("Problem",i,":",Accepted,CompileError,RuntimeError,TimeLimitExceed,WrongAnswer)

print('\n')
"""To be consistent with the format"""
for i in range(1, len(midtermDict) + 1):
  Accepted=0
  CompileError=0
  RuntimeError=0
  TimeLimitExceed=0
  WrongAnswer=0
  for j in range(0,len(midtermDict[i])):
    
    if midtermDict[i][j]==0:
      Accepted+=1
    if midtermDict[i][j]==1:
      CompileError+=1
    if midtermDict[i][j]==2:
      RuntimeError+=1
    if midtermDict[i][j]==3:
      TimeLimitExceed+=1
    if midtermDict[i][j]==4:
      WrongAnswer+=1
    
  print(Accepted,CompileError,RuntimeError,TimeLimitExceed,WrongAnswer,end=";")
