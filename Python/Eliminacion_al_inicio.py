arreglo = [10, 20, 30, 40]
n = 4

def el_inicio():
    global n
    for i in range(0, n - 1):
        arreglo[i] = arreglo[i + 1]
    n -= 1

el_inicio()
print(arreglo[:n])