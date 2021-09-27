import requests
from bs4 import BeautifulSoup
import re

""" 
v1 : 
1. 成功crawl到台大課程網的通識課資料 獲得一共有多少筆資料dataNum
2. 利用得到的dataNum修改網址 使全部課程資訊都在同一頁
3. 再一次crawl 用函式storeCourseInfo抽取關於課程的資訊(未存)

"""

urlPiece = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=&allproced=&op=stu&classarea=a&coursename=&teachername=&startrec=0&current_sem=110-1&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&page_cnt="
origurl = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=&allproced=&op=stu&classarea=a&coursename=&teachername=&startrec=0&current_sem=110-1&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&page_cnt=5"
cookie = "_ga=GA1.3.1203695655.1624103286; _gcl_au=1.1.261291191.1627552169; ASPSESSIONIDASBSQATC=DAOCBALAHMHPLJJBLPKDBAGJ; BIGipServernol_http=760652042.20480.0000; PHPSESSID=e2smm2609d497bttfqkn9hrra3; NOLlang=CH; user=YjA5NjExMDA3OiYjeDk2NzM7JiN4NjdjZjsmI3g5NzE2OzpzdHVkZW50OqZQvsc%3D; TS0117f60b=01048815221941082362c5dd059232df6e89a614a5ef9d6e469b87b45d406e76dd8f440bf1ac7a5e008b607ef3498fc936da4a1de64818febb00bb61a817c90c4cf9c1598637ddc9a78af3b40a96f8a8901e3eb4b5a8552da72a83369e009ba56aeac1e36ba2e249487a46555d2572b5a643ab2b21d44468f3b587484c431eb09b9e870eda; TSf86f2d17027=08eee1de4aab2000514fa6ff8dd1821335a3fbe0d3175a90123bd214adb49b1f41cbc5ddf0e5654008e2a7036e1130009d70487ae08a35775cbe3a2ad8a3e2feeba716b67ed51cf17dbada7b4b5ecf19cd74056810f76413aafb82840dcc485c"

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
    courseName = str(infoList[4].split('" target="_blank">')[1].strip('</a>')) #課程名稱
    credit = float(infoList[6].strip(' ')) #學分數
    identifier = str(infoList[7].strip(' ')) #課程識別碼
    period = str(infoList[8].strip(' ')) #全 半年
    prof = str(infoList[9].split('_new">')[1].strip('</a>')) #授課教師
    regisAppr = int(infoList[10].strip(' ')) #加選方式
    addsesstring = '' #第二個時間
    moresesstring = '' #第三個時間
    if str(infoList[11].split('<a')[0][0]) == "第" :
        sesstring = str(infoList[11].split('<a')[0].split('週<br/>')[1])
        #print('\n\n\n\n\n\n\nUnusual session',sesstring,'\n\n\n\n\n\n\n') #特例:第1,2,3,4,5,6,7,8,9   週<br/>三3,4<a href=http://map.ntu.edu.tw/index.htm?layer=build&uid=AT1020   target=_new >(新501)</a>
    else:
        sesstring = str(infoList[11].split('<a')[0].strip(' ')) #時間
        if sesstring.strip(' ')[-7:] == "(請洽系所辦)":
            sesstring = sesstring.strip(' ').strip("(請洽系所辦)")
            classroom = "請洽系所辦"
        try:
            addsesstring = str(infoList[11].split('<a')[1].split('</a>')[1]) #第二個時間
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
            pass
    except:
        print('\n\n\n\n\n\n\nUnusual field',"!!!!!",'\n\n\n\n\n\n\n')
    # print('\n0',infoList[0],'\n1',infoList[1],'\n2',infoList[2],'\n3',infoList[3],'\n4',infoList[4],'\n5',infoList[5],'\n6',infoList[6]
    # ,'\n7',infoList[7],'\n8',infoList[8],'\n9',infoList[9],'\n10',infoList[10],'\n11',infoList[11],'\n12',infoList[12],'\n13',infoList[13])
    print('\n\n流水號:',serialNum,'\n課號:',courseNum,'\n課程名稱:',courseName,'\n學分數:',credit,'\n課程識別碼:',identifier
    ,'\n全/半年:',period,'\n授課教師:',prof,'\n加選方式:',regisAppr,'\n時間:',sesstring,'\n第二時間:',addsesstring,'\n第三時間:',moresesstring
    ,'\n教室:',classroom,'\n人數:',studentNum,'\n領域: A',field)
    
origReq = crawler(origurl,cookie)
origReq.encoding = 'big5'
print("Successfully crawl the orig url")

origsoup = BeautifulSoup(origReq.text,"html.parser")
print("\nStore orig html as origsoup, datatype:",type(origsoup),'\n')
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
print("\nStore new html as soup, datatype:",type(soup),'\n')
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
        linkstr = segments[0] + '&' + segments[1][4:] + '&' + segments[2][4:] + '&' + segments[3][4:] + '&' + segments[4][4:]+ '&' + segments[5][4:]
        #print(index1,index2)
        #print(linkstr)
        #print(infoString,courseInfo)
        storeCourseInfo(str(courseInfo),linkstr)
    if infoString.strip(' \n\t') == "流水號授課對象課號班次課程名稱查看課程大綱，請點選課程名稱簡介影片學分課程識別碼全/半年授課教師加選方式時間教室總人數選課限制條件備註課程網頁本學期我預計要選的課程":
        print("Start collecting data\n")
        startFlag = True
        
"""
https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101 11230&amp;class=&amp;dpt_code=0000&amp;ser_no=74987&amp;semester=110-1&amp;lang=CH

https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101&2011230&amp;class=&amp;dpt_code=0000&amp;ser_no=74987&amp;semester=110-1&amp;lang=CH

https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101%2011230&class=&dpt_code=0000&ser_no=74987&semester=110-1&lang=CH

https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101%2011230&class=&dpt_code=0000&ser_no=74987&semester=110-1&lang=CH

https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101 12110&amp;class=&amp;dpt_code=0000&amp;ser_no=21919&amp;semester=110-1&amp;lang=CH

https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=101%2012110&class=&dpt_code=0000&ser_no=21919&semester=110-1&lang=CH
"""
