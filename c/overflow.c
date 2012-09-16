#include <stdio.h>

void print_bits_char(char c)
{
    for (int i = 7; i >= 0; i--) {
        printf("%d", (c >> i) & 1);
    }
    printf("\n");
}

void print_bits_int(int c)
{
    for (int i = 31; i >= 0; i--) {
        printf("%d", (c >> i) & 1);
    }
    printf("\n");
}

int main()
{
    char c1 = 1, c2 = 127;
    int n = c1 + c2;
    char c3= c1 + c2;
    printf("n = %d, c3 = %d\n", n, c3);
    print_bits_int(n);
    char c4 = -2;
    print_bits_char(c4);
    return 0;
}

