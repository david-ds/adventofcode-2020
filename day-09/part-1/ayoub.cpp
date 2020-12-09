#include <iostream>
#include <ctime>

#define SIZE 1000
#define WINDOW_SIZE 25

using namespace std;

uint64_t run(char* s) {
    uint64_t l[SIZE], x;
    int i = 0, k = -1, j, p;
    bool found;
    while (s[i]) {
        if (s[i] == '\n') {
            i++; continue;
        }
        x = 0ULL;
        while (s[i] >= '0' && s[i] <= '9') {
            x = x*10ULL + (uint64_t)(s[i]-'0');
            i++;
        }
        i++;

        l[++k] = x;
        if (k >= WINDOW_SIZE) {
            found = false;
            for (j = k-WINDOW_SIZE; j < k-1; j++) {
                for (p = j+1; p < k; p++) {
                    if (l[j] + l[p] == x) {
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
            if (!found) return x;
        }
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    uint64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
