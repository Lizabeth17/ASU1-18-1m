from parserP import stih_load

def cols(stih):
    count=0
    if stih != 'false':
        while stih.count("\n\n") != 0:
            stih = stih.replace("\n\n", "\n")
        smas = stih.split("\n")
        count_strok = 0
        count_long_strok = 0
        for smasi in smas:
            if len(smasi) > 70:
                count_long_strok = count_long_strok + 1
        for smasi in smas:
            if smasi != "":
                count_strok = count_strok + 1
        if (count_strok//2 < count_long_strok):
            return False
        else:
            if count_strok == 14:
                return "сонет 14 строк"
            else:
                if len(smas) > 200:
                    return False
                else:
                    return "стихотворение " + str(count_strok) + " строк"
