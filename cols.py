from parserP import stih

count=0

while stih.count("\n\n") != 0:
    stih = stih.replace("\n\n", "\n")

#print(stih)
#print(stih.count("\n"))

if stih.count("\n") == 14:
    cols_res = "Скорей всего, это сонет, написанный "
else:
    cols_res = "Скорей всего, это стихотворение, написанное "
