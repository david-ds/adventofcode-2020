#include <iostream>
#include <ctime>

#define MAX_SIZE 100

using namespace std;

int64_t run(char* s) {
    int64_t start = 0, f[MAX_SIZE];
    int i = 0, n = 0;

    while (s[i] >= '0' && s[i] <= '9') {
        start = start*10 + (s[i] - '0');
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
            f[n] = f[n]*10 + (s[i] - '0');
            i++;
        }
        n++;
        if (s[i] == ',') i++;
    }

    int64_t min = 1<<30, x, r = 0;
    for (i = 0; i < n; i++) {
        x = start - (start % f[i]);
        while (x <= start) x += f[i];
        if (x < min) {
            min = x;
            r = (x-start)*f[i];
        }
    }

    return r;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
