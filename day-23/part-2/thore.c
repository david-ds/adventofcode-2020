#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

#define N_CUPS 1000000
#define N_MOVES 10000000

long run(char *s)
{
    int input_length = strlen(s);

    long next_cup[N_CUPS + 1];
    long i;
    for (i = 0; i < input_length - 1; i++)
    {
        next_cup[s[i] - '0'] = s[i + 1] - '0';
    }
    next_cup[s[i] - '0'] = i + 2;
    i = i + 2;
    for (; i < N_CUPS; i++)
    {
        next_cup[i] = i + 1;
    }
    next_cup[N_CUPS] = s[0] - '0';

    long current_cup = next_cup[N_CUPS];
    for (long it = 1; it <= N_MOVES; it++)
    {
        long pickup1 = next_cup[current_cup];
        long pickup2 = next_cup[pickup1];
        long pickup3 = next_cup[pickup2];
        next_cup[current_cup] = next_cup[pickup3];

        long dest_cup = (current_cup == 1) ? N_CUPS : (current_cup - 1);
        while (dest_cup == pickup1 || dest_cup == pickup2 || dest_cup == pickup3)
        {
            dest_cup--;
            if (dest_cup == 0)
            {
                dest_cup = N_CUPS;
            }
        }

        long tmp = next_cup[dest_cup];
        next_cup[dest_cup] = pickup1;
        next_cup[pickup3] = tmp;

        current_cup = next_cup[current_cup];
    }

    long star_cup1 = next_cup[1];
    long star_cup2 = next_cup[star_cup1];
    return star_cup1 * star_cup2;
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
