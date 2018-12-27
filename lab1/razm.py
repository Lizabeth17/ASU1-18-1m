from parserP import stih_load
from mydict import l
from cols import cols
import codecs
import requests
from bs4 import BeautifulSoup
from chet_nechet_hist import chet_nechet_hist
from treh_hist import treh_hist
import datetime

now = datetime.datetime.now()

def search_partial_text(src, dst):
    dst_buf = dst
    result = 0
    for char in src:
        if char in dst_buf:
            dst_buf = dst_buf.replace(char, '', 1)
            result += 1
    r1 = int(result / len(src) * 100)
    r2 = int(result / len(dst) * 100)
    return (r1 if r1 < r2 else r2)

def detect_poetry_and_genre(stih, filenameforplots):
    vowels = list("уеёэоаыяию")
    vowelsUP = list("УЕЁЭОАЫЯИЮ")
    prepin = list("?!@\#\"№;$%^:&*\(\)-_+=.,<>'[]{}\\/—")
    horey = ""
    yamb = ""
    anapest = "3-"
    amfib = "2-"
    daktil = "1-"
    if stih != 'false':
        cols_res = cols(stih)
        if cols_res != False:
            f = codecs.open('mydict.py', 'w', 'utf-8')
            f.write("l = {")
            stih = stih.lower()
            stih = " "+ stih +" "
            stih = stih.replace("\n", " ")
            stih2=""
            start = 0
            try:
                while not stih.index(" ", start)==ValueError:
                    start = stih.find(" ", start) + 1
                    s = stih[start:stih.find(" ", start)]
                    for i in s:
                        if i in prepin:
                            s = s.replace(i, "")
                    isFound = False
                    for k, v in l.items():
                        if k == s:
                            s=v
                            isFound = True
                            break
                        else:
                            isFound = False
                    if not isFound:
                        sk=s
                        try:
                            reqst = "https://где-ударение.рф/в-слове-" + s + "/"
                            print(reqst)
                            page_text1 = requests.get(reqst)
                            soup = BeautifulSoup(page_text1.text, "html.parser")
                            soup_text = soup.find(class_='rule')
                            s = soup_text.get_text()
                            s = s[s.find("— "):s.find(",")]
                            s = s[s.find("— ")+2:s.find(".")]
                        except AttributeError:
                            s = s.replace("у", "У")
                        l[sk] = s            
                    stih2 = stih2+s
            except ValueError:
                print('')
            for key,val in l.items():
                f.write("'{}':'{}',\n".format(key,val))
            f.write("}")
            f.close()
            j=0
            slog=0
            slog2=0
            isOpred = False
            isTreh = False
            chet = 0
            nechet = 0
            razmer=""
            while (j<len(stih2)):
                if stih2[j] in vowels:
                    if not stih2[j-1] in vowelsUP:
                        slog = slog + 1
                if stih2[j] in vowelsUP:
                    slog = slog + 1
                    if (slog2 != 0) and (isOpred == False):
                        if slog-slog2 > 2:
                            isTreh = True
                            isOpred = True
                        else:
                            isOpred = True
                    else:
                        slog2 = slog
                    if slog % 2 == 0:
                        chet = chet + 1
                    else:
                        nechet = nechet + 1
                    razmer = razmer + str(slog) + "-"
                j = j+1
            h = 0
            while len(yamb)<len(razmer):
                h = h+1
                if h%2 == 0:
                    yamb = yamb + str(h) + "-"
            h = 0
            while len(horey)<len(razmer):
                h = h+1
                if h%2 != 0:
                    horey = horey + str(h) + "-"
            h = 1
            while len(daktil)<len(razmer):
                h = h+3
                daktil = daktil + str(h) + "-"
            h = 2
            while len(amfib)<len(razmer):
                h = h+3
                amfib = amfib + str(h) + "-"
            h = 3
            while len(anapest)<len(razmer):
                h = h+3
                anapest = anapest + str(h) + "-"                
            if isTreh:
                an = search_partial_text(razmer, anapest)
                am = search_partial_text(razmer, amfib)
                da = search_partial_text(razmer, daktil)
                if an < am:
                    if am < da:
                        razm_res_t = "дактиль"
                        razm_res_p = da
                    else:
                        razm_res_t = "амфибрахий"
                        razm_res_p = am
                else:
                    if an < da:
                        if am < da:
                            razm_res_t = "дактиль"
                            razm_res_p = da
                    else:
                        razm_res_t = "анапест"
                        razm_res_p = an
                treh_hist(an, am, da, filenameforplots)
                return [cols_res, razm_res_t, razm_res_p]
            else:
                if chet > nechet:
                    razm_res_t = "ямб"
                    razm_res_p = nechet
                    razm_res_p1 = chet
                else:
                    razm_res_t = "хорей"
                    razm_res_p = nechet
                    razm_res_p1 = chet
                chet_nechet_hist(chet, nechet, filenameforplots)
                return [cols_res, razm_res_t, razm_res_p, razm_res_p1]
        else:
            return False
    else:
        return False

def get_default_reqs():
    reqs = {}
    reqs.update({'http://lib.ru/LITRA/PUSHKIN/p2.txt': '1'})
    reqs.update({'http://lib.ru/INOFANT/BRADBURY/summer.txt': '1'})
    reqs.update({'http://lib.ru/INPROZ/OGENRI/stihi.txt': '1'})
    reqs.update({'http://lib.ru/POEZIQ/ASADOW/jumbo.txt': '1'})
    reqs.update({'http://lib.ru/POEZIQ/ASADOW/ostrow.txt': '1'})
    reqs.update({'http://lib.ru/POEZIQ/AWERINCEW/stihi.txt': '1'})
    reqs.update({'http://lib.ru/SHAKESPEARE/shks_sonnets66_1.txt': '1'})
    reqs.update({'http://lib.ru/POEZIQ/NADSON/utro.txt': '1'})
    reqs.update({'http://lib.ru/INOFANT/BRADBURY/summer.txt': '1'})
    reqs.update({'тютчев гроза.txt': '2'})
    reqs.update({'Памятник.txt': '2'})
    reqs.update({'блок.txt': '2'})
    reqs.update({'Page1.txt': '2'})
    reqs.update({'пушкин змний вечер.txt': '2'})
    reqs.update({'лермонтов.txt': '2'})
    reqs.update({'блок к музе.txt': '2'})
    reqs.update({'блок к музе123.txt': '2'})
    return reqs

def main(reqs = {}):
    chi = 0
    filenameres = 'result_' + now.strftime("%d-%m-%Y_%H-%M") + '.txt'
    with open(filenameres, 'w') as flrs:
        for req in reqs.keys():
            stih = stih_load(reqs[req], req)
            filenameforplots = 'Object_' + str(chi)
            print(filenameforplots + ': ' + req)
            print(" ", file=flrs)
            print(filenameforplots, file=flrs)
            print(req, file=flrs)
            filenameforplots = filenameforplots + '.png'
            chi+=1
            text_data = detect_poetry_and_genre(stih, filenameforplots)
            if text_data != False:
                print("Жанр: " + text_data[0], file=flrs)
                print("Размер: " + text_data[1], file=flrs)
                if text_data[1] == "ямб" or text_data[1] == "хорей":
                    print("Кол-во нечетных ударных слогов: " + str(text_data[2]), file=flrs)
                    print("Кол-во четных ударных слогов: " + str(text_data[3]), file=flrs)
                else:
                    print("Процент совпадения с эталоном: " + str(text_data[2]), file=flrs)
            else:
                print("ОШИБКА! Указанный документ имеет неправильную верстку, содержит несколько произведений или не является стихотворением.", file=flrs)
            print("Done!")
            print("")
    print("Программа выполнена!")
    return 0

if __name__ == '__main__':
    reqs = get_default_reqs()
    main(reqs)
