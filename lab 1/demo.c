/**
 * This demo is made for Lab 1 of the Computer Architecture class of AUTH.
 * 
 * Authors: Anargyros Diamantopoulos
 *          Apostolos Panagiotopoulos
 * 
 * Date:    18/11/2019
 **/

#include <stdio.h>

int main() {
    int counter[1000];

    for (int i = 0; i < 1000000; i++) {
        counter[i%1000] = i;
    }

    printf("idx | value\n");
    printf("===========\n");
    for (int i = 0; i < 1000; i++) {
        printf("%3d  %d\n", i, counter[i]);
    }

    return 0;
}