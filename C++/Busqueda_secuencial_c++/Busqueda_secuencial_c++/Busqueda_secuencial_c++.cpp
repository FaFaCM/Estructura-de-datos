#include <iostream>
using namespace std;

int main()
{
    int arreglo[] = { 15, 3, 42, 8, 23 };
    int n = 5;
    int valor = 42;
    int resultado = -1;

    for (int i = 0; i < n; i++)
    {
        if (arreglo[i] == valor)
        {
            resultado = i;
            break;
        }
    }

    cout << resultado << endl;

    return 0;
}