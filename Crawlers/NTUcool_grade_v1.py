import requests
from bs4 import BeautifulSoup

def crawler(url,cookie):
    try:
        r = requests.get(url, headers = {"cookie": cookie
        ,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3"})
        #print(r.text)
        if r.encoding == "utf-8" and r.status_code == 200:
          #print("\n讀取成功!!!")
          return r
        else :
          print("\nheaders沒設定好...")
        # print("check encoding",r.encoding)
        # print("check headers:\n",r.request.headers)
        # print("check status",r.status_code)
    except:
        print("沒抓到網頁")

class Assignment:
    def __init__(self,title,category,link,due,getpoint,totalpoint,status):
        self.title = title
        self.category = category
        self.link = link
        self.due = due
        self.getpoint = getpoint
        self.totalpoint = totalpoint
        self.status = status
    def display(self):
        print('(',self.status,')')
        if self.due == '_':
            print("Due : undetermined")
        else:
            print("Due:",self.due)
        print(self.category,' - ',self.title)
        print("Link:",self.link)
        print("Score:",self.getpoint,"/",self.totalpoint,'\n')


#課程首頁url -> 成績url
gradeurl="https://cool.ntu.edu.tw/courses/4499" + "/grades"
gradecookie = "_ga=GA1.3.1203695655.1624103286; _csrf=03NimGdlSa47Mt9r3dxtLNxB; log_session_id=05a198fa756e1a8eaa1252c880753e80; _gid=GA1.3.1277859302.1626684125; _legacy_normandy_session=CSYnh8AumeYUy9LUvq-zEA+dDALhAAnaiSZyW5JeNRKsLMmqUoxOdQTWmtBzFKwBIEpjvz5vGZx411vhk5DQQWn8PVMPLwr9dmjCuviKKioNMwupsI5if54mIHtZuYLY_AvnJiF-seazKGqqK-dIlxoPOfULh9-XK5kIton9aX1qgIS27uq00FaQ2nen-GM0xAD_IqtUnJuQfqq0MoahC9D72fLFXyg2Muq7QpYod3d-KjXCW58UmVQZ0muTeZYRn3DrpcJOSc_SkCRMWBraBszPbdv6Law6kA4uYfD_1CFoNBRkdbWAzDGnvh0xOG1r4JIrShLz53Wcs18d2eJNNQx-hKfmqugunlxkEIWnKYBF1RImDlbTP0_4DNP3ZXJXQcaNV5YsltRXvWoA51SDQ1HCsuTLTvG1xksMAUrd3cfy4KIK24FRPwczu9pifI4gLw5jWFavvdptngKa5irPx5xilTmT1Gt9JYLcyk7seaigd6U3i7MrjAujt5YfTp5w8iGGyN5o7dzf-VseqK8ij7x.WBv_UFRbYn9CH3hnlIi6FpeBja8.YPVAnA; _normandy_session=CSYnh8AumeYUy9LUvq-zEA+dDALhAAnaiSZyW5JeNRKsLMmqUoxOdQTWmtBzFKwBIEpjvz5vGZx411vhk5DQQWn8PVMPLwr9dmjCuviKKioNMwupsI5if54mIHtZuYLY_AvnJiF-seazKGqqK-dIlxoPOfULh9-XK5kIton9aX1qgIS27uq00FaQ2nen-GM0xAD_IqtUnJuQfqq0MoahC9D72fLFXyg2Muq7QpYod3d-KjXCW58UmVQZ0muTeZYRn3DrpcJOSc_SkCRMWBraBszPbdv6Law6kA4uYfD_1CFoNBRkdbWAzDGnvh0xOG1r4JIrShLz53Wcs18d2eJNNQx-hKfmqugunlxkEIWnKYBF1RImDlbTP0_4DNP3ZXJXQcaNV5YsltRXvWoA51SDQ1HCsuTLTvG1xksMAUrd3cfy4KIK24FRPwczu9pifI4gLw5jWFavvdptngKa5irPx5xilTmT1Gt9JYLcyk7seaigd6U3i7MrjAujt5YfTp5w8iGGyN5o7dzf-VseqK8ij7x.WBv_UFRbYn9CH3hnlIi6FpeBja8.YPVAnA; _csrf_token=9%2BHJhdfM7kQhg8P1g3M5ShOy%2Fn0OuQXptiFF6t3v1sqftLHtuvy%2BCmfapZHaAH1la8OOGEruXIL8ExWdpbmSrg%3D%3D"
coursenum = str(gradeurl[-4:])

#filename = str(input("Create a file called: "))

result = crawler(gradeurl,gradecookie)
soup = BeautifulSoup(result.text,"html.parser")
print("\nStore html, datatype:",type(soup),'\n')

TitleList = []
LinkList = []
DueList = []
GetPointList = []
TotalPointList = []
StatusList = []

""" title category """
Title2Category = dict()
for line in soup.find_all('th',attrs={"class":"title","scope":"row"}):
    try:
        if line.get_text().split('\n')[1][0] != " ":
            #print("\nTitle:",line.get_text().split('\n')[1])
            #print("\nCategory:",line.get_text().split('\n')[2])
            Title2Category[line.get_text().split('\n')[1]] = line.get_text().split('\n')[2]
    except:
        print("Exception occurs !")

""" title link """
for line in soup.find_all('a'):
    try:
        linkstr = line.get('href')
        #print("link:",linkstr)
        if linkstr[:26] == "/courses/4499/assignments/":
            if line.get_text().strip(" \n") != "" and line.get_text().strip(" ") != "課程資訊" and line.get_text().strip(" ") != "\xa0":
                TitleList.append(line.get_text().strip(" "))
                #print("\nAppend Title:",line.get_text().strip(" \n"))
                linkstr = "https://cool.ntu.edu.tw/" + linkstr
                LinkList.append(linkstr)
                #print("\nAppend link:",linkstr)
    except:
        print("Exception occurs !")
  
""" due NTU cool 網頁是從截止日期先的排到後的 再排沒有的"""  
for line in soup.find_all('td',attrs={"class":"due"}):
    try:
        month = line.get_text().strip(' \n').split('月')[0][-2:].strip(' ')
        day = line.get_text().strip(' \n').split('月')[1][:2].strip(' 日')
        datestr = str(month) + " / " +str(day)
        DueList.append(datestr)
        #print(datestr)
    except:
        DueList.append("_")
        
""" getpoint """
for line in soup.find_all('span',attrs={"class":"original_points"}):
    try:
        GetPointList.append(float(line.get_text().strip(' \n')))
        #print(float(line.get_text().strip(' \n')))
    except:
        GetPointList.append('_')
        #print('_')
        
""" totalpoint """
for line in soup.find_all('td',attrs={"class":"possible points_possible"}):
    try:
        TotalPointList.append(float(line.get_text().strip(' \n')))
        #print(float(line.get_text().strip(' \n')))
    except:
        TotalPointList.append('_')
        #print('_')
    
""" status """    
for line in soup.find_all('span',attrs={"class":"submission_status"}):
    if len(StatusList) == len(TitleList):
        break
    text = line.get_text().strip(' \n')
    if text == "none":
        StatusList.append('_')
        #print('_')
    else:
        StatusList.append(text)
        #print(text)
        
print("\nSuccess\n")
print("\nTitleList",TitleList,len(TitleList))
print("\nLinkList",LinkList,len(LinkList))
print("\nGetPointList",GetPointList,len(GetPointList))
print("\nTotalPointList",TotalPointList,len(TotalPointList))
print("\nStatusList",StatusList,len(StatusList))
print("\nDueList",DueList,len(DueList))

print("There are",len(TitleList),"assignments:\n")
for i in range(0,len(TitleList)):
    """title,category,link,due,getpoint,totalpoint,status"""
    A = Assignment(TitleList[i],Title2Category[TitleList[i]],LinkList[i],DueList[i],GetPointList[i],TotalPointList[i],StatusList[i])
    print(str(i+1)+'.\n')
    A.display()