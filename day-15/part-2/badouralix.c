#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Assume that the maximum number of the sequence is not higher than the maximum iteration :becausewhynot:
// See https://www.youtube.com/watch?v=etMJxB-igrc
#define MAXLOOP 30000000
#define MAXSIZE 30000000

uint32_t run(char *s)
{
	uint32_t i = 1, j = 0, last = 0;
	char *c = s, *buf = s;

	// At this point we cannot really initialize with `uint32_t memory[MAXSIZE];` without a segfault
	uint32_t *memory = malloc(MAXSIZE * sizeof(uint32_t));

	// Parse input and store both the step i ( starting at 1 so that it works ) and the latest number seen
	do
	{
		switch (*c)
		{
		case ',':
		case '\0':
			memory[last = atoi(buf)] = i++;
			buf = ++c;
			break;
		default:
			c++;
			break;
		}
	} while (*(c - 1) != '\0');

	// Decrease i before starting the loop so that 0 = i - j and it magically works
	// This assumes that the input last number has not appeared in the sequence yet
	for (i--; i < MAXLOOP; i++)
	{
		if (memory[last] != 0)
		{
			j = memory[last];
			memory[last] = i;
			last = i - j;
		}
		else
		{
			memory[last] = i;
			last = 0;
		}
	}

	return last;
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
