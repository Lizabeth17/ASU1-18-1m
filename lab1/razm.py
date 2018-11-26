from parserP import stih_load
from mydict import l
from cols import cols
import codecs
import requests
from bs4 import BeautifulSoup
from chet_nechet_hist import chet_nechet_hist
from treh_hist import treh_hist

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

vowels = list("уеёэоаыяию")
vowelsUP = list("УЕЁЭОАЫЯИЮ")
prepin = list("?!@\#\"№;$%^:&*\(\)-_+=.,<>'[]{}\\/—")
horey = ""
yamb = ""
anapest = "3-"
amfib = "2-"
daktil = "1-"
choise = 0

while choise != 3:   
    choise = input('Будем парсить с lib.ru (1) или из заготовленного файла (2)? 3 - выход: ')
    if choise == '1':
        req = input('Введите ссылку на стихотворение с сайта lib.ru: ')
    else:
        if choise == '2':
            req = input('Введите имя файла в директории с программой (с .txt на конце): ')
        else:
            print('Команда неизвестна.')
            raise SystemExit(1)
        
    stih = stih_load(choise, req)

    if stih != 'false':

        cols_res = cols(stih)

        if cols_res != 'false':
            f = codecs.open('mydict.py', 'w', 'utf-8')
            f.write("l = {")

            print(stih)

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

            print("RAZMER: " + razmer)
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
                        print(cols_res + "дактилем")
                        print("Процент совпадения с дактилем: " + str(da))
                    else:
                        print(cols_res + "амфибрахием")
                        print("Процент совпадения с амфибрахием: " + str(am))
                else:
                    if an < da:
                        if am < da:
                            print(cols_res + "дактилем")
                            print("Процент совпадения с дактилем: " + str(da))
                    else:
                        print(cols_res + "анапестом")
                        print("Процент совпадения с анапестом: " + str(an))
                treh_hist(an, am, da)

            else:
                print("Четных: {}".format(chet))
                print("Нечетных: {}".format(nechet))
                if chet > nechet:
                    print(cols_res + "ямбом")
                else:
                    print(cols_res + "хореем")
                chet_nechet_hist(chet, nechet)
        else:
            print('Скорей всего, текст на данной странице не является стихотворением в классическом его понимании или содержит намного больше одного произведения.')
    else:
        print('Указанная страница имеет неверную верстку или текст на ней не является стихотворением.')
        print('Проверьте, что вы ссылаетесь на сайт lib.ru, и что стихотворение отделено от шапки страницы символами ---.')
