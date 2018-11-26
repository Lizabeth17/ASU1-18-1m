import requests
from bs4 import BeautifulSoup

def stih_load(choise, req):

    #f = open('тютчев гроза.txt', 'r') 
    #f = open('Памятник.txt', 'r')
    #f = open('блок.txt', 'r') 
    #f = open('Page1.txt', 'r') 
    #f = open('пушкин змний вечер.txt', 'r') 
    #f = open('лермонтов.txt', 'r') 
    #f = open('блок к музе.txt', 'r') 
    
    #page_text1 = requests.get('http://lib.ru/LITRA/PUSHKIN/p2.txt')
    #page_text4 = requests.get('http://lib.ru/POEZIQ/ASADOW/jumbo.txt') 
    #page_text5 = requests.get('http://lib.ru/POEZIQ/ASADOW/ostrow.txt')
    #page_text6 = requests.get('http://lib.ru/POEZIQ/AWERINCEW/stihi.txt')
    #page_text7 = requests.get('http://lib.ru/SHAKESPEARE/shks_sonnets66_1.txt') 
    #page_text8 = requests.get('http://lib.ru/POEZIQ/NADSON/utro.txt') 
    #page_text9 = requests.get('https://www.google.com/search?q=qwerty')
    #page_text2 = requests.get('http://lib.ru/INOFANT/BRADBURY/summer.txt')
    #page_text3 = requests.get('http://lib.ru/INPROZ/OGENRI/stihi.txt')

    try:
        try:
            if choise == '2':
                f = open(req, 'r')
                stihL = f.read()
            else: 
                page_text1 = requests.get(req)
                soup = BeautifulSoup(page_text1.text, "html.parser")
                
                text = soup.select('pre')[1]
                text = text.get_text()

                stihL = text[text.rfind('---')+3:len(text)]

                stihL = stihL.replace("\n\n", "\n")
 
            smas = stihL.split("\n")
            stihL = ""

            i = 0
            numstr = 0
            while i < len(smas):
                if (smas[i] != "") and (not smas[i].isdigit()) and (smas[i].find("Популярность: ") == -1):
                    #print(smas[i])
                    stihL = stihL + smas[i] + "\n"
                i = i + 1
            return stihL
        except all:
            return 'false'
    except TypeError:
        return 'false'
