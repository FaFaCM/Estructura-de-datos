arreglo = [10, 20, 30, 40, 50]
n = 5

def el_pos(pos):
    global n
    for i in range(pos, n, -1):
        arreglo[i] = arreglo[i + 1]
    n-= 1

el_pos(2)
print(arreglo[:n])