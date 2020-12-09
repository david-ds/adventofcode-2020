#include <iostream>
#include <ctime>

#define SIZE 1000
#define WINDOW_SIZE 25

using namespace std;

uint64_t max(uint64_t l[], int i, int j) {
    uint64_t r = l[i];
    for (int k = i+1; k <= j; k++) r = (r<l[k])?l[k]:r;
    return r;
}

uint64_t min(uint64_t l[], int i, int j) {
    uint64_t r = l[i];
    for (int k = i+1; k <= j; k++) r = (r>l[k])?l[k]:r;
    return r;
}

uint64_t run(char* s) {
    uint64_t l[SIZE], sum[SIZE], x;
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
        sum[k] = x;
        if (k > 0) sum[k] += sum[k-1];
        
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
            if (!found) {
                for (j = 0; j < k-1; j++) {
                    for (p = j+1; p < k; p++) {
                        if ((j == 0 && sum[p] == x) || (j > 0 && sum[p] - sum[j-1] == x)) {
                            return max(l, j, p) + min(l, j, p);
                        }
                    }
                }
            }
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
