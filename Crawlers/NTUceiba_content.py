from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import smtplib
import requests
from bs4 import BeautifulSoup

def crawler(url,cookie):
    try:
        r = requests.get(url, headers = {"cookie": cookie
        ,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3"})
        r.encoding == "UTF-8"
        return r
        if r.encoding == "utf-8" and r.status_code == 200:
          print("\nSuccess!!!")
        else :
          print("\nFailed...")
        print("check encoding",r.encoding)
        print("check headers:\n",r.request.headers)
        print("check status",r.status_code)
    except:
        print("沒抓到網頁")
        
content_url = "https://ceiba.ntu.edu.tw/modules/syllabus/syllabus.php?default_lang=english"
content_cookie = "_ga=GA1.3.1203695655.1624103286; _gid=GA1.3.1277859302.1626684125; PHPSESSID=22f41b16cfe20efc9d28bd470cb4995d; user=YjA5NjExMDA3OumZs%2Bafj%2BmcljpzdHVkZW50OuWQjOWtuA%3D%3D; TS01fb8d58=0104881522a42bebbe99e3614f78292244c7b46c36d91912c50f536f54c1cf2e869d22052a2c269b8aee2f7dbf2c106a7ef8ef5848b88161ee1252f04f2b5a8c19fbb32dd8ece2f81232a2bad6fef91293adfc9c96"
result = crawler(content_url,content_cookie)
print("success")

result.encoding = "utf-8"
result = result.text
# result = result.encode('ISO-8859-1') #解碼 ISO to Unicode
# result = result.decode('utf-8') #編碼 Unicode to utf-8
print(result)

soup = BeautifulSoup(result,"html.parser")
print("\nStore html, datatype:",type(soup),'\n')

for line in soup.find_all('a'):
    try:
        linkstr = "https://ceiba.ntu.edu.tw/" + line.get('href')[6:]
        print(linkstr.strip(' \n'))
    except:
        print("Exception")
       
countline = 0  
weeklist = ["start"]
datelist = ["start"]
titlelist = ["start"]
filelist = ["start"]

for line in soup.find_all('td'):
    countline += 1
    info = line.get_text().strip(' \n\r\t\xa0')
    if countline%4 == 1 :
        weeklist.append(info)
        print("Append week:",info)
    if countline%4 == 2 :
        datelist.append(info)
        print("Append date:",info)
    if countline%4 == 3 :
        titlelist.append(info)
        print("Append title:",info)
    if countline%4 == 0 :
        filelist.append(info)
        print("Append file:",info)
    
