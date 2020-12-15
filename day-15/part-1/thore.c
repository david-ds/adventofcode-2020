#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N_TURNS 2020

uint32_t run(char *s)
{
    static uint32_t last_seen[N_TURNS + 1] = {0};
    uint32_t turn = 1;
    uint32_t n = 0;

    char *c = strtok(s, ",");
    while (c != NULL)
    {
        n = atoi(c);
        last_seen[n] = turn;
        turn++;
        c = strtok(NULL, ",");
    }
    turn--;

    while (turn < N_TURNS)
    {
        uint32_t last = last_seen[n];
        last_seen[n] = turn;
        if (last != 0)
        {
            n = turn - last;
        }
        else
        {
            n = 0;
        }
        turn++;
    }
    return n;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);

    printf("_duration:%f\n%d\n", (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC, answer);
    return 0;
}
