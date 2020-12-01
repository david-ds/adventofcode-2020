#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int run(char *input)
{
    char acc[4] = {0}; // accumulator for ints
    int acc_i = 0, parsed_total = 0;

    int parsed[300]; // 300 should be far enough, tested inputs are around 200

    // Parse ints
    for (; *input != '\0'; ++input)
    {
        if (*input == '\n')
        {
            parsed[parsed_total++] = atoi(acc);
            acc_i = 0;
            for (int j = 0; j < 4; j++)
                acc[j] = 0;
        }
        else
        {
            acc[acc_i++] = *input;
        }
    }
    for (int i1 = 0; i1 < parsed_total; i1++)
        for (int i2 = i1 + 1; i2 < parsed_total; i2++)
        {
            if (i1 + i2 >= 2020)
                continue;
            for (int i3 = i2 + 1; i3 < parsed_total; i3++)
                if (parsed[i1] + parsed[i2] + parsed[i3] == 2020)
                    return parsed[i1] * parsed[i2] * parsed[i3];
        }
    return 0;
}

int main(int argc, char **argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);

    printf("_duration:%f\n%d\n", (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC, answer);
    return 0;
}
