from flask import Flask,render_template ,request
import requests
import time
import json
from bs4 import BeautifulSoup as bs


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/toons')
def toons():
    #request.args.get('type')#type에 어떤 값이 들었는지 받아내는 것 
    cat = request.args.get('type')
    if(cat == 'naver'):
        today = time.strftime("%a").lower()#오늘 날짜 요일
        naver_url = 'https://comic.naver.com/webtoon/weekdayList.nhn?week='+today
        response = requests.get(naver_url).text
    
        soup = bs(response, 'html.parser')
        li = soup.select('.img_list li')#클래스 별명일떄는 .을 붙여서 검색
                                         #ID로 검색할떄는 #아이디로 검색
                                         #빈칸을 띄우면 그 클래스 안에 있는것에서 li를 검색한다는 의미
        toons = []
        print(li)
          
        for item in li:
          toon = {"title":item.select('.thumb a')[0]["title"],#같은의미 "title":item.select_one('dt a').text
                  "url":"https://comic.naver.com{}".format(item.select('.thumb a')[0]["href"]),
                  "img_url":item.select('.thumb img')[0]["src"]#src라는 키값으로 값을 구한다는 의미
          }
          
          toons.append(toon)
          
    elif(cat=='daum'):
        today = time.strftime("%a").lower()#오늘 날짜 요일
        daum_url = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/thu'
        response = requests.get(daum_url).text
        document = json.loads(response)
        data = document["data"]
        toons=[]
        
        for toon in data:
            toons.append({"title":toon["title"],
                            "url":"http://webtoon.daum.net/webtoon/view/"+toon["nickname"],
                            "img_url":toon["pcThumbnailImage"]["url"]
            })
                
    return render_template('toons.html',t=toons,c=cat)
    


@app.route('/lotto')
def lotto():
    return render_template('lotto.html')
    
    
@app.route('/apart')
def apart():
    #1.내가 원하는 정보를 얻을 수 있는 url을 url변수에 저장한다.
    url = 'http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20333305&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode='
    #1-1 request header에 추가할 정보를 dictionary 형태로 저장한다.
    headers = {
        "Host": "rt.molit.go.kr",
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"}
    
    #2. request의 get기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
    response = requests.get(url,headers = headers).text
    document = json.loads(response)
    
    for d in document["result"]:
        print(d["BLDG_NM"])
        print(d["JIBUN_NAME"])
        print(d["SUM_AMT"])
        print(d["BLDG_AREA"])
        
    #print(response)
    
    
    #3. 응답으로 온 코드의 형태를 살펴본다.(json/xml/html)
    return render_template('apart.html')
    
@app.route('/exchange')
def exchange():
    #어느 사이트든 좋습니다 
    url = 'http://finance.daum.net/api/exchanges/summaries'


    headers = {
    "Host": "finance.daum.net"
    ,"Referer": "http://finance.daum.net/exchanges"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    response = requests.get(url,headers = headers).text
    document = json.loads(response)
    print(document)
    
    money_info=[]
    
    for d in document["data"]:
        money_info.append({"name":d["name"],
                            "basePrice":d["basePrice"],
                            "changeRate":d["changeRate"],
                            "exchangeCommission":d["exchangeCommission"]
            
        })
        
    print(money_info)
    
    #li = soup.select("td")
    #print(li)
    #for d in li:
        #print(d["a"])
        #print(d[""])
        #print(d[""])
        #print(d[""])
    
    
    '''
    for i in li :
        print(i["td"])
       ''' 
    #li = soup.select('.img_list li')
    #money_info = []
    
    #print(li)
    

    #for i in li :
        #print(i("a")[0])
     #   print(i("#sale"))
        
    '''
    for item in li:
      money = {"title":item.select("a"),#같은의미 "title":item.select_one('dt a').text
              "money":item.select("#sale")
             # "img_url":item.select('.thumb img')[0]["src"]#src라는 키값으로 값을 구한다는 의미
      }
       '''   
      #money_info.append(money)
    
    
    #print(money_info)
    
    #for nation in money_info :
    #    print(money_info["title"])
    #document = json.loads(response)
    
    #print(response)
    #print(soup)
    
    #print(document)
    #크롤링을 통해 가장 많은 환율 정보를 끌어 오시는 분께
    #커피 삽니다.
    #무조건 개수 기준/3시 40분
    #1등 자유이용권
    #2등 커피종류
    #3드 아이스 아메리카노
    
    return render_template('exchange.html')
    