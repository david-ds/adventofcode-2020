#include <stdio.h>
#include <time.h>
#include <stdlib.h>

// Format example:
//6-7 g: gghggcggg

int run(char *input)
{
    int valid_passwords = 0;

    int i = 0;
    char first_pos_acc[3] = {0};
    char last_pos_acc[3] = {0};
    int first_pos = 0;
    int last_pos = 0;
    char target_char = 0;
    int valid_counter = 0;
    int current_state = 0; // 0: parse min, 1: parse max, 2: parse target, 3: parse password

    for (; *input != '\0'; ++input)
    {
        switch (*input)
        {
        case (' '):
        {
            if (current_state == 1)
            {
                last_pos = atoi(last_pos_acc);
                current_state = 2;
                i = 0;
            }
            break;
        }
        case '\0':
        case '\n':
        {
            if (valid_counter == 1)
                valid_passwords++;
            current_state = 0;
            // Reset accumulators
            for (int j = 0; j < 3; j++)
            {
                first_pos_acc[j] = 0;
                last_pos_acc[j] = 0;
            }
            valid_counter = 0;
            i = 0;
            break;
        }
        case '-':
        {
            first_pos = atoi(first_pos_acc);
            current_state = 1;
            i = 0;
            break;
        }
        case ':':
        {
            current_state = 3;
            i = 0;
            continue;
        }
        default:
        {
            switch (current_state)
            {
            case 0:
            {
                first_pos_acc[i++] = *input;
                break;
            }
            case 1:
            {
                last_pos_acc[i++] = *input;
                break;
            }
            case 2:
            {
                target_char = *input;
                break;
            }
            case 3:
            {
                i++;
                if ((i == first_pos || i == last_pos) && *input == target_char)
                    valid_counter++;
                break;
            }
            default:
                break;
            }
            continue;
        }
        }
    }
    if (valid_counter == 1)
        valid_passwords++;
    return valid_passwords;
}

int main(int argc, char **argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);

    printf("_duration:%f\n%d\n", (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC, answer);
    return 0;
}
