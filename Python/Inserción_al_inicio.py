arreglo = [10, 20, 30, 0, 0, 0, 0, 0, 0, 0]
n = 3

def ins_inicio(valor):
    global n 
    for i in range(n, 0, -1):             
        arreglo[i] = arreglo[i - 1]        
    arreglo[0] = valor
    n += 1

ins_inicio(1)
print(arreglo[:n]) #para que solo muestre los que tienen valores en el arreglo