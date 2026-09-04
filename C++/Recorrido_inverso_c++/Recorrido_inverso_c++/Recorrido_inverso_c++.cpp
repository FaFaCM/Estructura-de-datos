#include <iostream>
using namespace std;

int main()
{
    int arreglo[] = { 10, 20, 30, 40, 50 };
    int n = 5;

    for (int i = n - 1; i >= 0; i--)
    {
        cout << "Posicion " << i << ": " << arreglo[i] << endl;
    }

    return 0;
}