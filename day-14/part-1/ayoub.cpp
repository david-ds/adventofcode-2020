#include <iostream>
#include <unordered_map>
#include <ctime>

using namespace std;

const uint64_t ALL1 = 68719476735ULL;

uint64_t run(char* s) {
    unordered_map<uint64_t, uint64_t> m;
    uint64_t mask_and = ALL1, mask_or = 0, key = 0, val = 0;
    int i = 0, k;
    while (s[i]) {
        if (s[i] == '\n') {
            i++; continue;
        }
        if (s[i] == 'm' && s[i+1] == 'a') {
            mask_and = ALL1; mask_or = 0;
            i += 7; k = 0;
            while (s[i] != '\n') {
                if (s[i] == '1') mask_or += 1ULL<<(35-k);
                else if (s[i] == '0') mask_and = mask_and & (~(1ULL<<(35-k)));
                k++; i++;
            }
            continue;
        }
        if (s[i] == 'm' && s[i+1] == 'e') {
            i += 4; key = 0;
            while (s[i] >= '0' && s[i] <= '9') {
                key = key*10ULL + s[i]-'0';
                i++;
            }
            i += 4; val = 0;
            while (s[i] >= '0' && s[i] <= '9') {
                val = val*10ULL + s[i]-'0';
                i++;
            }
            m[key] = (val & mask_and) | mask_or;
        }
    }
    uint64_t sum = 0;
    for (const pair<uint64_t, uint64_t>& x: m) {
        sum += x.second;
    }

    return sum;
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
