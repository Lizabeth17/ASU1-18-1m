import requests
from bs4 import BeautifulSoup

def stih_load(choise, req):
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
                    stihL = stihL + smas[i] + "\n"
                i = i + 1
            return stihL
        except all:
            return 'false'
    except TypeError:
        return 'false'
