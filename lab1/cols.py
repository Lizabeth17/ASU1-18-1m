from parserP import stih

def cols(stih):

    count=0

    if stih != 'false':

        while stih.count("\n\n") != 0:
            stih = stih.replace("\n\n", "\n")

        smas = stih.split("\n")

        count_long_strok = 0
        for smasi in smas:
            if len(smasi) > 70:
                count_long_strok = count_long_strok + 1

        if (len(smas)//2 < count_long_strok):
            return 'false'
        else:
            if len(smas) == 14:
                return "Скорей всего, это сонет, написанный "
            else:
                if len(smas) > 200:
                    return 'false'
                else:
                    return "Скорей всего, это стихотворение, написанное "
