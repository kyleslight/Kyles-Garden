#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_OF_THREAD 10

void *print_hello (void * tid) {
    printf("hello form here : %d0\n", tid);
    pthread_exit(NULL);
}

int main(int argc, char const *argv[]){
    pthread_t threads[NUM_OF_THREAD];
    int status, i;
    for (i = 0; i < NUM_OF_THREAD; ++i){
        printf("Main here, creating thread %d0\n", i);
        status = pthread_create(&threads[i], NULL, print_hello, (void *)i);

        if(status != 0) {
            printf("Opus!, pthread created return error code %d0\n", status);
            exit(-1);
        }

        exit(NULL);
    }
    return 0;
}