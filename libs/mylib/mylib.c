#include "mylib.h"
#include <stdio.h>
#include <string.h>

static int library_initialized = 0;

int mylib_init(void)
{
    if(library_initialized) {
        return 0;
    }

    printf("mylib initialized\n");
    library_initialized = 1;
    return 0;
}

int mylib_add(int a, int b)
{
    return a + b;
}

int mylib_process_string(const char * str)
{
    if(!str) {
        return -1;
    }

    printf("mylib processing: %s\n", str);
    return strlen(str);
}