#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

#define N_MOVES 100

long run(char *s)
{
    int n_cups = strlen(s);

    int next_cup[n_cups + 1];
    int i;
    for (i = 0; i < n_cups - 1; i++)
    {
        next_cup[s[i] - '0'] = s[i + 1] - '0';
    }
    next_cup[s[i] - '0'] = s[0] - '0';

    int current_cup = s[0] - '0';
    for (int it = 1; it <= N_MOVES; it++)
    {
        int pickup1 = next_cup[current_cup];
        int pickup2 = next_cup[pickup1];
        int pickup3 = next_cup[pickup2];
        next_cup[current_cup] = next_cup[pickup3];

        int dest_cup = (current_cup == 1) ? n_cups : (current_cup - 1);
        while (dest_cup == pickup1 || dest_cup == pickup2 || dest_cup == pickup3)
        {
            dest_cup--;
            if (dest_cup == 0)
            {
                dest_cup = n_cups;
            }
        }

        int tmp = next_cup[dest_cup];
        next_cup[dest_cup] = pickup1;
        next_cup[pickup3] = tmp;

        current_cup = next_cup[current_cup];
    }

    long answer = 0;
    for (int c = next_cup[1]; c != 1; c = next_cup[c])
    {
        answer += c;
        answer *= 10;
    }

    return answer / 10;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    long answer = run(argv[1]);

    printf("_duration:%f\n%ld\n", (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC, answer);
    return 0;
}
