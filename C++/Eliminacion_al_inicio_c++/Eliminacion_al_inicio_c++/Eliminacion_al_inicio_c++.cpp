#include <iostream>
using namespace std;

int main()
{
    int arreglo[] = { 10, 20, 30, 40 };
    int n = 4;

    for (int i = 0; i < n - 1; i++)
    {
        arreglo[i] = arreglo[i + 1];
    }
    n--;

    for (int i = 0; i < n; i++)
        cout << arreglo[i] << " ";

    return 0;
}