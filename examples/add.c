#include <stdio.h>

int calc(int a, int b){
    return a+b;
}

void main(){
    int x, y, dump;
    dump = scanf("%d", &x);
    dump = scanf("%d", &y);
    printf("%d\n", calc(x, y));
}