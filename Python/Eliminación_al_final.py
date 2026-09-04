arreglo = [10, 20, 30, 40]
n = 4

def el_final():
    global n
    n -= 1

el_final()
print(arreglo[:n])