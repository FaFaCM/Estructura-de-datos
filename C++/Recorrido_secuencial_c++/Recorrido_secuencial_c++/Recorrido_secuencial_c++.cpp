#include <iostream>
using namespace std;

int main()
{
    int arreglo[] = { 10, 20, 30, 40, 50 };
    int n = 5;

    for (int i = 0; i < n; i++)
    {
        cout << "Posición " << i << ": " << arreglo[i] << endl;
    }

    return 0;
}