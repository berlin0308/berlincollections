"""抓取網頁原始碼(HTML)"""
import urllib.request as req
import requests
from bs4 import BeautifulSoup 
gossipurl="https://www.ptt.cc/bbs/Gossiping/index.html" #八卦版


def getdata(url):
		#建立一個Request物件 要設定headers(F12仿使用者)
		#F12-Application-cookie
		request=req.Request(url, headers = { "cookie":"over18=1", #cookie over18=1時可過
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
		with req.urlopen(request) as response:
			data = response.read().decode("utf-8")

		"""解析原始碼 找特徵 標籤"""
		import bs4
		root = bs4.BeautifulSoup(data, "html.parser")
		#titles = root.find("div", class_="title")  #find->找一個class="title" 的div標籤
		titles = root.find_all("div", class_="title") #find_all->找全部的 存成list
		#print(titles.a.string) #印被<a></a>包夾的單一字串

		#titles list中有每行的title 逐行分析
		for title in titles:
			if title.a != None: #有些在<title>裡面但沒有<a>(本文已被刪除)
				print(title.a.string)
				
		nextlink = root.find("a",string="最舊") #find到的是包含" "的整行程式碼
		return nextlink["href"] #顯示屬性為超連結的網址

pageurl = gossipurl

"""抓取不同頁面的資訊"""
for i in range(3):
	pageurl = getdata(pageurl) #return 得到下一個頁面的網址
	pageurl = "https://www.ptt.cc"+ pageurl #觀察到超連結的網址只有後面
	print(pageurl)
