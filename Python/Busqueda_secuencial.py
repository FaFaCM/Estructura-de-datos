arreglo = [10, 5, 42, 64, 23]

def bus_sec(valor):
    for i in range(len(arreglo)):
        if arreglo[i] == valor:
            return 1 
    return -1

print(bus_sec(23))