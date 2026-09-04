#include <iostream>
using namespace std;

int main()
{
    int arreglo[] = { 3, 8, 15, 23, 42, 56, 70 };
    int n = 7;
    int valor = 23;

    int izquierda = 0;
    int derecha = n - 1;
    int resultado = -1;

    while (izquierda <= derecha)
    {
        int medio = (izquierda + derecha) / 2;

        if (arreglo[medio] == valor)
        {
            resultado = medio;
            break;
        }
        else if (arreglo[medio] < valor)
        {
            izquierda = medio + 1;
        }
        else
        {
            derecha = medio - 1;
        }
    }

    cout << resultado << endl;

    return 0;
}