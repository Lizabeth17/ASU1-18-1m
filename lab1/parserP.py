import requests
from bs4 import BeautifulSoup


#f = open('тютчев гроза.txt', 'r') #ямб  -  ямб
#f = open('Памятник.txt', 'r') #ямб  - дактиль
#f = open('блок.txt', 'r') #ямб  - анапест
#f = open('Page1.txt', 'r') #ямб  - ямб
#f = open('пушкин змний вечер.txt', 'r') #хорей  - хорей
#f = open('лермонтов.txt', 'r') #амфибрахий  - амфибрахий
f = open('блок к музе.txt', 'r') #анапест  - анапест


page_text1 = requests.get('http://lib.ru/LITRA/PUSHKIN/p2.txt')
page_text4 = requests.get('http://lib.ru/POEZIQ/ASADOW/jumbo.txt') #асадов - парсит
page_text5 = requests.get('http://lib.ru/POEZIQ/ASADOW/ostrow.txt')
page_text6 = requests.get('http://lib.ru/POEZIQ/AWERINCEW/stihi.txt')
page_text7 = requests.get('http://lib.ru/SHAKESPEARE/shks_sonnets66_1.txt') #шекспир - парсит
page_text8 = requests.get('http://lib.ru/POEZIQ/NADSON/utro.txt') #Надсон - парсит


page_text2 = requests.get('http://lib.ru/INOFANT/BRADBURY/summer.txt')
page_text3 = requests.get('http://lib.ru/INPROZ/OGENRI/stihi.txt')

soup = BeautifulSoup(page_text8.text, "html.parser")

text = soup.select('pre')[1]
text = text.get_text()
#text.pre.decompose()
#print(text.get_text())
#print(text.get_text())

stih = text[text.rfind('---')+3:len(text)]

stih = stih.replace("\n\n", "\n")
smas = stih.split("\n")
#print(smas[3])
stih = ""

i = 0
numstr = 0
while i < len(smas):
    #print(stih.count("\n"))
    #stih2 = stih[numstr:stih.find("\n")]
    #numstr = stih.find("\n", numstr) + 1
    if (smas[i] != "") and (not smas[i].isdigit()) and (smas[i].find("Популярность: ") == -1):
        #print(smas[i])
        stih = stih + smas[i] + "\n"
    #if smas[i].isdigit():
    #    break
    #stih = stih.replace(stih[0:stih.find("\n")], "")
    i = i + 1

#stih = f.read()
