#include <stdio.h>

extern double distance();

void print_i32(int val) {
    printf(">>> print_i32: %d\n", val);
}

void print_f64(double val) {
    printf(">>> print_i64: %f\n", val);
}

int main() {
    distance();
    return 0;
}
