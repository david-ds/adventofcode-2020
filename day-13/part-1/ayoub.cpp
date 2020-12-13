#include <iostream>
#include <ctime>

#define MAX_SIZE 100

using namespace std;

long run(char* s) {
    long start = 0, f[MAX_SIZE];
    int i = 0, n = 0;

    while (s[i] >= '0' && s[i] <= '9') {
        start = start*10L + (long)(s[i] - '0');
        i++;
    }
    i++;
    while (s[i] && s[i] != '\n') {
        if (s[i] == 'x') {
            i++;
            if (s[i] == ',') i++;
            continue;
        }
        while (s[i] >= '0' && s[i] <= '9') {
            f[n] = f[n]*10L + (long)(s[i] - '0');
            i++;
        }
        n++;
        if (s[i] == ',') i++;
    }

    long x = start;
    while (1) {
        for (i = 0; i < n; i++) {
            if (x % f[i] == 0) return (x-start)*f[i];
        }
        x++;
    }

    return 0;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    long answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
