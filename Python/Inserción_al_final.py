arreglo = [10, 20, 30, 0, 0, 0, 0, 0, 0, 0]
n = 3

def ins_final(valor):
    global n
    arreglo[n] = valor
    n += 1

ins_final(40)
print(arreglo[:n])
