#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int run(char* s) {
  char* inp = s;
  int good_pwd_counter = 0;

  char special;
  int special_counter = 0;
  int min = 0;
  int max = 0;
  int j = 0;

  while (j < 1000) {
    min = 0; max = 0; special_counter = 0;

    min = atoi(inp);
    while (*inp != '-') {
        inp++;
    }
    inp++;

    max = atoi(inp);
    while (*inp != ' ') {
        inp++;
    }
    inp++;

    special = *inp;
    inp++; inp++; inp++;

    while ((*inp != '\n') & (*inp != '\0')) {
        if (*inp == special) {
            special_counter++;
        }
        inp++;
    }

    if ((special_counter <= max) & (special_counter >= min)) {
        good_pwd_counter++;
    }
    j++;
  }
  return good_pwd_counter;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%i\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
