"""抓取網頁原始碼(HTML)"""
import urllib.request as req
import requests
import json

urlPiece1 = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=&allproced=&op=stu&classarea=a&coursename=&teachername=&startrec=0&current_sem=110-1&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&page_cnt="
url = urlPiece1 + "220"
url="https://medium.com/_/graphql"
cookie = "_ga=GA1.3.1203695655.1624103286; _gcl_au=1.1.261291191.1627552169; ASPSESSIONIDASBSQATC=DAOCBALAHMHPLJJBLPKDBAGJ; BIGipServernol_http=760652042.20480.0000; PHPSESSID=e2smm2609d497bttfqkn9hrra3; NOLlang=CH; user=YjA5NjExMDA3OiYjeDk2NzM7JiN4NjdjZjsmI3g5NzE2OzpzdHVkZW50OqZQvsc%3D; TS0117f60b=01048815221941082362c5dd059232df6e89a614a5ef9d6e469b87b45d406e76dd8f440bf1ac7a5e008b607ef3498fc936da4a1de64818febb00bb61a817c90c4cf9c1598637ddc9a78af3b40a96f8a8901e3eb4b5a8552da72a83369e009ba56aeac1e36ba2e249487a46555d2572b5a643ab2b21d44468f3b587484c431eb09b9e870eda; TSf86f2d17027=08eee1de4aab2000514fa6ff8dd1821335a3fbe0d3175a90123bd214adb49b1f41cbc5ddf0e5654008e2a7036e1130009d70487ae08a35775cbe3a2ad8a3e2feeba716b67ed51cf17dbada7b4b5ecf19cd74056810f76413aafb82840dcc485c"

#建立一個Request物件 要設定headers
#requestData:要給伺服器request的data(F12/Headers/Request payload/view source)
#json檔的特殊處理
request=req.Request(url, headers = { #"cookie": cookie
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
with req.urlopen(request) as response:
    result = response.read().decode("utf-8")
	
print(result)

# result=json.loads(result)
# #print(result["data"]["extendedFeedItems"][0]["post"]["title"]) 第一篇title
# print(result["data"].keys())
# for i in range(0,len(result["data"]["extendedFeedItems"])):
    # print(result["data"]["extendedFeedItems"][i]["post"]["title"])


# print(request.content)
# print(request.encoding)

#print(result)

# print(type(result))
# result = request.content.decode('ISO-8859-1') #解碼 ISO to Unicode
# print(result)
# result = result.decode('ISO-8859-1')
# print(type(result))
# result = result.encode('utf8',errors='ignore') #編碼 Unicode to utf-8
# print(type(result))
#print(result)

#print(result) .decode('utf-8',errors='ignore').encode('utf-8')