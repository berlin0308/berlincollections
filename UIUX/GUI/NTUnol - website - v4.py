import requests
from bs4 import BeautifulSoup
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import smtplib

""" 
v1 : 
1. 成功crawl到台大課程網的通識課資料 獲得一共有多少筆資料dataNum
2. 利用得到的dataNum修改網址 使全部課程資訊都在同一頁
3. 再一次crawl 用函式storeCourseInfo抽取關於課程的資訊(未存)

v2 :
4. 補上班次
5. recordSessions會在storeCourseInfo被呼叫 處理多個時段 和多個節數的問題
6. CourseDict以流水號為key 包括所有課程資訊的list為value
7. MonList到SunList 的第i項即為第i節課所有課程的流水號的list

v3 :
8. 修復2021/8/5 課程網201->285堂課的bug(未註記A幾的field為0)
9. ValidSessList[i][j]=True 代表星期i+1的第j節課有空
10.重複的流水號CourseDict只算一次(285筆收錄245筆
11.從第一項True的課開始看 利用CourseDict看這堂課所有的時段 若所有的時段都有空 將之存到ValidCourseList
12.判斷出所有不包括Sat Sun的課是否valid

v4 :
13.用showValidCourseResult展示結果並寄信
"""

myaccount = 'berlinchen0308@gmail.com'
ntuaccount = 'b09611007@ntu.edu.tw'
urlPiece = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=&allproced=&op=stu&classarea=a&coursename=&teachername=&startrec=0&current_sem=110-1&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&page_cnt="
origurl = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=&allproced=&op=stu&classarea=a&coursename=&teachername=&startrec=0&current_sem=110-1&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&page_cnt=5"
cookie = "_ga=GA1.3.1203695655.1624103286; _gcl_au=1.1.261291191.1627552169; ASPSESSIONIDASBSQATC=DAOCBALAHMHPLJJBLPKDBAGJ; BIGipServernol_http=760652042.20480.0000; PHPSESSID=e2smm2609d497bttfqkn9hrra3; NOLlang=CH; user=YjA5NjExMDA3OiYjeDk2NzM7JiN4NjdjZjsmI3g5NzE2OzpzdHVkZW50OqZQvsc%3D; TS0117f60b=01048815221941082362c5dd059232df6e89a614a5ef9d6e469b87b45d406e76dd8f440bf1ac7a5e008b607ef3498fc936da4a1de64818febb00bb61a817c90c4cf9c1598637ddc9a78af3b40a96f8a8901e3eb4b5a8552da72a83369e009ba56aeac1e36ba2e249487a46555d2572b5a643ab2b21d44468f3b587484c431eb09b9e870eda; TSf86f2d17027=08eee1de4aab2000514fa6ff8dd1821335a3fbe0d3175a90123bd214adb49b1f41cbc5ddf0e5654008e2a7036e1130009d70487ae08a35775cbe3a2ad8a3e2feeba716b67ed51cf17dbada7b4b5ecf19cd74056810f76413aafb82840dcc485c"

CourseDict = dict()  #CourseDict[serialNum] = [courseNum,classNum,courseName,credit,identifier,period,prof,regisAppr,sesstring,addsesstring,moresesstring,classroom,studentNum,field,courseLink]

MonList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
TueList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
WedList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
ThuList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
FriList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
SatList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
SunList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

ValidCourseList = []

                #  0    1    2    3    4    5    6    7    8    9    10   11   12   13   14
ValidSessList1 = [[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]   #Mon
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]   #Tue
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]]

                #     0    1    2    3    4    5    6    7    8    9    10   11   12   13   14
theValidSessList = [[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]    #Mon
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]    #Tue
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]    #Wed
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]    #Thu
                 ,[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]]   #Fri

"""輸入信件主旨 內容 (收件者 副本 預設為gmail帳號) (寄件者為gmail帳號)"""
def SendMail(subject,content,receive = myaccount,cc = myaccount ):
    mypassword = 'blackie0308'
    print('start to send mail...')
    sender = myaccount #step1:setup sender gmail,ex:"Fene1977@superrito.com"
    password = mypassword #step2:setup password
    recipient = receive #step3:setup recipients mail
    
    #多個收件人 e.g."Hinte1969@jourrapide.com,Fene1977@rhyta.com,Fene1977@teleworm.us"
    
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = recipient
    outer["Cc"]= cc
    outer['From'] = sender
    
    outer.attach(MIMEText(content))
    mailBody = outer.as_string()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s: #send webservice to gmail smtp socket
            s.ehlo()
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender, recipient,mailBody)
            s.close()
        print("mail sent!")
        print("\nCheck:\nSender Account Check:",sender)
        print("Recipient Account Check:",recipient)
        print("\nSubject:",subject)
        print("\nContent:",content)
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

def showValidCourseResult(serialNum):
    print("\n課程名稱:",CourseDict[serialNum][2])
    print("授課老師:",CourseDict[serialNum][6])
    print("課號及班次:",CourseDict[serialNum][0],CourseDict[serialNum][1])
    print("課程識別碼:",CourseDict[serialNum][4])
    print("流水號:",serialNum)
    print("時間:",CourseDict[serialNum][8],CourseDict[serialNum][9],CourseDict[serialNum][10])
    print("教室:",CourseDict[serialNum][11])
    print("學分:",CourseDict[serialNum][3])
    print("全/半年:",CourseDict[serialNum][5])
    print("加選方式:",CourseDict[serialNum][7])
    print("人數上限:",CourseDict[serialNum][12])
    print("領域:",str('A'+str(CourseDict[serialNum][13])))
    print("課程資訊:",CourseDict[serialNum][14])
    
    subject = "Pymail: Valid Courses"
     
    content = "\n\n課程名稱: "+str(CourseDict[serialNum][2])+"\n授課老師: "+CourseDict[serialNum][6]+"\n課號及班次: "+str(CourseDict[serialNum][0])+' '+str(CourseDict[serialNum][1])+"\n課程識別碼: "+str(CourseDict[serialNum][4])+"\n流水號: "+str(serialNum)+"\n時間: "+str(CourseDict[serialNum][8])+' '+str(CourseDict[serialNum][9])+' '+str(CourseDict[serialNum][10])+"\n教室: "+CourseDict[serialNum][11]+"\n學分: "+str(CourseDict[serialNum][3])+"\n全/半年: "+CourseDict[serialNum][5]+"\n加選方式:"+str(CourseDict[serialNum][7])+"\n人數上限: "+str(CourseDict[serialNum][12])+"\n領域: "+str('A'+str(CourseDict[serialNum][13]))+"\n課程資訊: "+CourseDict[serialNum][14]
    SendMail(subject,content,ntuaccount)
    
def sess2Num(sess):
    if sess == 'A':
        return 11
    if sess == 'B':
        return 12
    if sess == 'C':
        return 13
    if sess == 'D':
        return 14
    if int(sess) >= 0 and int(sess) <= 10:
        return int(sess)
        
def add2MonList(timeString,serialNum):
    MonList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        MonList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nMon 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            MonList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nMon 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass

def add2TueList(timeString,serialNum):
    TueList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        TueList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nTue 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            TueList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nTue 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass
     
def add2WedList(timeString,serialNum):
    WedList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        WedList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nWed 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            WedList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nWed 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass
        
def add2ThuList(timeString,serialNum):
    ThuList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        ThuList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nThu 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            ThuList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nThu 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass
        
def add2FriList(timeString,serialNum):
    FriList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        FriList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nFri 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            FriList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nFri 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass
        
def add2SatList(timeString,serialNum):
    SatList[sess2Num(str(timeString).split(',')[0][1:].strip('(請洽系所辦) '))].append(serialNum)
    CourseDict[serialNum][8] = timeString.strip('(請洽系所辦) ')
    try:
        SatList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nSat 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        for i in range(2,10):
            try:
                SatList[sess2Num(str(timeString.split(',')[i]))].append(serialNum)
                #print('\n\n\n\nSat sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),"to",sess2Num(str(timeString.split(',')[i])),'\n\n\n\n')
            except:
                pass
    except:
        pass
              
def add2SunList(timeString,serialNum):
    SunList[sess2Num(str(timeString).split(',')[0][1:])].append(serialNum)
    try:
        SunList[sess2Num(str(timeString.split(',')[1]))].append(serialNum)
        #print('\n\n\n\n\n\n\nSun 2 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),'\n\n\n\n\n\n\n')
        try:
            SunList[sess2Num(str(timeString.split(',')[2]))].append(serialNum)
            #print('\n\n\n\nSun 3 sessions:',serialNum,sess2Num(str(timeString).split(',')[0][1:]),sess2Num(str(timeString.split(',')[1])),sess2Num(str(timeString.split(',')[2])),'\n\n\n\n')
        except:
            pass
    except:
        pass
        
            
def crawler(url,cookie):
    try:
        r = requests.get(url, headers = {"cookie": cookie
        ,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3"})
        #print("check encoding",r.encoding)
        #print("check headers:\n",r.request.headers)
        #print("check status",r.status_code)
        return r
        if r.encoding == "utf-8" and r.status_code == 200:
          print("\nSuccess!!!")
        else :
          print("\nFailed...")

    except:
        print("沒抓到網頁")
  
def storeCourseInfo(string,link):
    #print(string)
    courseLink = link
    infoList = re.split('</td><td>',string)
    serialNum = int(infoList[0].strip(' ')[-5:]) #流水號
    courseNum = str(infoList[2].strip(' ')) #課號
    classNum = str(infoList[3].strip(' ').strip('\xa0')) #班次
    try:
        courseName = str(infoList[4].split('" target="_blank">')[1].strip('</a>')) #課程名稱
    except:
        courseName = str(infoList[4].split('<')[0].strip(' '))
    credit = float(infoList[6].strip(' ')) #學分數
    identifier = str(infoList[7].strip(' ')) #課程識別碼
    period = str(infoList[8].strip(' ')) #全 半年
    prof = str(infoList[9].split('_new">')[1].strip('</a>')) #授課教師
    field = '0'
    try:
        regisAppr = int(infoList[10].strip(' ').strip('\xa0')) #加選方式
    except:
        regisAppr = 0
    addsesstring = '' #第二個時間
    moresesstring = '' #第三個時間
    if str(infoList[11].split('<a')[0][0]) == "第" :
        sesstring = str(infoList[11].split('<a')[0].split('週<br/>')[1])
        #print('\n\n\n\n\n\n\nUnusual session',sesstring,'\n\n\n\n\n\n\n') #特例:第1,2,3,4,5,6,7,8,9   週<br/>三3,4<a href=http://map.ntu.edu.tw/index.htm?layer=build&uid=AT1020   target=_new >(新501)</a>
    else:
        sesstring = str(infoList[11].split('<a')[0].strip(' ')) #時間  .strip(' <img align="ABSMIDDLE" height="18" src="images/chg.gif" width="32"/>')
        if sesstring.strip(' ')[-7:] == "(請洽系所辦)":
            sesstring = sesstring.strip(' ').strip("(請洽系所辦)")
            classroom = "請洽系所辦"
        try:
            addsesstring = str(infoList[11].split('<a')[1].split('</a>')[1].strip('<img align="ABSMIDDLE" height="18" src="images/chg.gif" width="32"/>').strip(' ')) #第二個時間
            if addsesstring.strip(' \n') != '':
                #print("\n\n\n\n\n\n\nTwo sessions:",sesstring,addsesstring,'\n\n\n\n\n\n\n')
                try:
                    moresesstring = str(infoList[11].split('<a')[2].split('</a>')[1]) #第三個時間
                    if moresesstring.strip(' \n') != '':
                        #print("\n\n\n\n\n\n\nThree sessions:",sesstring,addsesstring,moresesstring,'\n\n\n\n\n\n\n')
                        pass
                except:
                    #print("\n\n\n\n\n\n\nThree:",sesstring,addsesstring,moresesstring,'\n\n\n\n\n\n\n')
                    pass
        except:
            addsesstring = ''
    try:
        classroom = str(infoList[11].split('>(')[1].split(')</a>')[0]) #教室
    except:
        classroom = "請洽系所辦"
        sesstring = sesstring.strip('(請洽系所辦)')
        
    studentNum = int(infoList[12].split('(含開放')[0].split('</td><td')[0])
    try:
        field = infoList[12].split('A')[1].split('領域')[0].strip('*。') #.strip('<a href="https://ceiba.ntu.edu.tw/question.php?lang=big5&amp;course_id=H01 10400&amp;class=01&amp;semester=110-1" target="_new">本課程英文化程度說明</a>')
        try:
            field = int(field[:2])
        except:
            field = int(field[0])
        try:
            field = str( str(field) + infoList[12].split('A')[2].split('領域')[0] )
            field = int(field[:2])
            if field//10 == field%10 :
                field = field%10          
        except:
            field = '0'
    except:
        #print('\n\n\n\n\n\n\nUnusual field',"!!!!!",'\n\n\n\n\n\n\n')
        #print(infoList[12])
        pass
    # print('\n0',infoList[0],'\n1',infoList[1],'\n2',infoList[2],'\n3',infoList[3],'\n4',infoList[4],'\n5',infoList[5],'\n6',infoList[6]
    # ,'\n7',infoList[7],'\n8',infoList[8],'\n9',infoList[9],'\n10',infoList[10],'\n11',infoList[11],'\n12',infoList[12],'\n13',infoList[13])
    # print('\n\n流水號:',serialNum,'\n課號:',courseNum,'\n班次:',classNum,'\n課程名稱:',courseName,'\n學分數:',credit,'\n課程識別碼:',identifier
    # ,'\n全/半年:',period,'\n授課教師:',prof,'\n加選方式:',regisAppr,'\n時間:',sesstring,'\n第二時間:',addsesstring,'\n第三時間:',moresesstring
    # ,'\n教室:',classroom,'\n人數:',studentNum,'\n領域: A',field,'\n課程連結:',courseLink)
    
    # if serialNum in CourseDict.keys():
        # print("\n\n\n\n\n\nhelp!!!",serialNum,"\n\n\n\n\n\n") 
    """重複的流水號"""
    if serialNum not in CourseDict :
        CourseDict[serialNum] = [courseNum,classNum,courseName,credit,identifier,period,prof,regisAppr,sesstring,addsesstring,moresesstring,classroom,studentNum,field,courseLink]
    # print("Append dict:",serialNum,CourseDict[serialNum],'\n')
    
    recordSessions(sesstring,addsesstring,moresesstring,serialNum)
    
def recordSessions(time1,time2,time3,serialNum):
    timeList = [time1,time2,time3]
    for time in timeList :
        if time == '':
            break
        if time[0] == '一' :
            add2MonList(time,serialNum)
        if time[0] == '二' :
            add2TueList(time,serialNum)
        if time[0] == '三' :
            add2WedList(time,serialNum)
        if time[0] == '四' :
            add2ThuList(time,serialNum)
        if time[0] == '五' :
            add2FriList(time,serialNum)
        if time[0] == '六' :
            add2SatList(time,serialNum)
        if time[0] == '日' :
            add2SunList(time,serialNum)
    
def collectResult(theValidSessList)
    origReq = crawler(origurl,cookie)
    origReq.encoding = 'big5'
    print("Successfully crawl the orig url")

    origsoup = BeautifulSoup(origReq.text,"html.parser")
    #print("\nStore orig html as origsoup, datatype:",type(origsoup),'\n')
    #print(origsoup.prettify())

    """數總共有幾筆資料"""
    someStrings = origsoup.find_all("td",attrs={"align":'left'})
    for eachString in someStrings:
        if eachString.get_text()[:4]== "共查詢到"  and  eachString.get_text()[-3:]== "筆課程" :
            dataNum = int(eachString.get_text().split(' ')[1])
            print("There are",dataNum,"courses\n")
            
    newurl = urlPiece + str(dataNum+2)
    newReq = crawler(newurl,cookie)
    newReq.encoding = 'big5'
    print("Successfully crawl the new url")

    soup = BeautifulSoup(newReq.text,"html.parser")
    #print("\nStore new html as soup, datatype:",type(soup),'\n')
    #print(soup.prettify()) 

    startFlag = False
    courseInfos = soup.find_all("tr",attrs = {"align":"center"})
    for courseInfo in courseInfos :
        infoString = courseInfo.get_text()

        if startFlag == True :
            index1 = str(courseInfo).find('href="')
            index2 = str(courseInfo).find('" target')
            linkstr = "https://nol.ntu.edu.tw/nol/coursesearch/" + str(courseInfo)[index1:index2].strip('href="').strip(' ')
            try:
                linkstr = linkstr.split(' ')[0] + "%20" + linkstr.split(' ')[1]
            except:
                #print("\n\nException\n\n")
                pass
            segments = linkstr.split('&')
            try:
                linkstr = segments[0] + '&' + segments[1][4:] + '&' + segments[2][4:] + '&' + segments[3][4:] + '&' + segments[4][4:]+ '&' + segments[5][4:]
            except:
                linkstr = ''
            #print(index1,index2)
            #print(linkstr)
            #print(infoString,courseInfo)
            storeCourseInfo(str(courseInfo),linkstr)
        if infoString.strip(' \n\t') == "流水號授課對象課號班次課程名稱查看課程大綱，請點選課程名稱簡介影片學分課程識別碼全/半年授課教師加選方式時間教室總人數選課限制條件備註課程網頁本學期我預計要選的課程":
            print("Start collecting data\n")
            startFlag = True

    #print(CourseDict)
    print("\nThe CourseDict appends",len(CourseDict.keys()),"courses\n")

    # print(MonList)
    # print(TueList)
    # print(WedList)
    # print(ThuList)
    # print(FriList)
    # print(SatList)
    # print(SunList)

    WeekdayList = [MonList,TueList,WedList,ThuList,FriList]

    for weekday in range(0,5):
        for sess in range(0,14):
            #print(sess)
            if theValidSessList[weekday][sess] == True :  #Mon 的第sess堂課有空
                for aclass in WeekdayList[weekday][sess]:
                    #print(type(aclass),aclass)
                    time1 = CourseDict[aclass][8]
                    time2 = CourseDict[aclass][9]
                    time3 = CourseDict[aclass][10]
                    #print("time1:",time1,"time2:",time2,"time3:",time3)
                    times = [time1,time2,time3]
                    countValid = 0
                    for time in times:
                        try:
                            if time == '':
                                countValid += 1
                                #print("countValid++(void)",countValid)
                            if time[0] == '一' :
                                #print(int(time[1:].split(',')[0]))
                                count = 0
                                for segment in range(0,len(time[1:].split(','))) :
                                    if theValidSessList[0][sess2Num(time[1:].split(',')[segment])] == True :
                                        count += 1
                                        #print("valid")
                                    if theValidSessList[0][sess2Num(time[1:].split(',')[segment])] == False :
                                        pass
                                        #print("Not valid")  
                                if count == len(time[1:].split(',')):
                                    countValid += 1
                                    #print("countValid++",countValid)
                                # else :
                                    # print("It's not valid!")
                                      
                            if time[0] == '二' :
                                #print(int(time[1:].split(',')[0]))
                                count = 0
                                for segment in range(0,len(time[1:].split(','))) :
                                    if theValidSessList[1][int(time[1:].split(',')[segment])] == True :
                                        count += 1
                                        #print("valid")
                                    if theValidSessList[1][int(time[1:].split(',')[segment])] == False :
                                        pass
                                        #print("Not valid")  
                                if count == len(time[1:].split(',')):
                                    countValid += 1
                                    #print("countValid++",countValid)
                                # else :
                                    # print("It's not valid!")
                                    
                            if time[0] == '三' :
                                #print(int(time[1:].split(',')[0]))
                                count = 0
                                for segment in range(0,len(time[1:].split(','))) :
                                    if theValidSessList[2][sess2Num(time[1:].split(',')[segment])] == True :
                                        count += 1
                                        #print("valid")
                                    if theValidSessList[2][sess2Num(time[1:].split(',')[segment])] == False :
                                        pass
                                        #print("Not valid")  
                                if count == len(time[1:].split(',')):
                                    countValid += 1
                                    # print("countValid++",countValid)
                                # else :
                                    # print("It's not valid!")
                                    
                            if time[0] == '四' :
                                #print(int(time[1:].split(',')[0]))
                                count = 0
                                for segment in range(0,len(time[1:].split(','))) :
                                    if theValidSessList[3][sess2Num(time[1:].split(',')[segment])] == True :
                                        count += 1
                                        #print("valid")
                                    if theValidSessList[3][sess2Num(time[1:].split(',')[segment])] == False :
                                        pass
                                        #print("Not valid")  
                                if count == len(time[1:].split(',')):
                                    countValid += 1
                                    # print("countValid++",countValid)
                                # else :
                                    # print("It's not valid!")
                                    
                            if time[0] == '五' :
                                #print(int(time[1:].split(',')[0]))
                                count = 0
                                for segment in range(0,len(time[1:].split(','))) :
                                    if theValidSessList[4][sess2Num(time[1:].split(',')[segment])] == True :
                                        count += 1
                                        #print("valid")
                                    if theValidSessList[4][sess2Num(time[1:].split(',')[segment])] == False :
                                        pass
                                        #print("Not valid")  
                                if count == len(time[1:].split(',')):
                                    countValid += 1
                                    # print("countValid++",countValid)
                                # else :
                                    # print("It's not valid!")
                                    
                            if time[0] == '六' :
                                pass
                            if time[0] == '日' :
                                pass
                        except:
                            #print("Error!")
                            pass
                
                    
                    if countValid == 3:
                        if aclass not in ValidCourseList :
                            ValidCourseList.append(aclass)
                            # print("\nAppend :",aclass)
                        # else :
                            # print("\nThe course has been appended")
                    # else :
                        # print("\nNot Valid:",aclass,'\n')
                    
    print("\nFollowing courses are valid :\n",ValidCourseList)
    print("\n\n",len(ValidCourseList),"courses are included\n\n")

showValidCourseResult(ValidCourseList[26])