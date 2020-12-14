#include <iostream>
#include <unordered_map>
#include <ctime>

using namespace std;

void override_all(unordered_map<uint64_t, uint64_t>& m, uint64_t key, uint64_t value, bool floating[], int k = 0) {
    if (k == 36) {
        m[key] = value;
        return;
    }
    if (!floating[k]) {
        override_all(m, key, value, floating, k+1);
        return;
    }
    override_all(m, key & (~(1ULL<<(35-k))), value,  floating, k+1);
    override_all(m, key | (1ULL<<(35-k)), value, floating, k+1);
}

int count_floating(bool floating[]) {
    int c = 0;
    for (int k = 0; k < 36; k++) c += (floating[k])?1:0;
    return c;
}

uint64_t run(char* s) {
    unordered_map<uint64_t, uint64_t> m;
    uint64_t mask_or = 0, key = 0, val = 0;
    int i = 0, k;
    bool floating[36] = {false};
    while (s[i]) {
        if (s[i] == '\n') {
            i++; continue;
        }
        if (s[i] == 'm' && s[i+1] == 'a') {
            mask_or = 0;
            i += 7; k = 0;
            while (s[i] != '\n') {
                floating[k] = false;
                if (s[i] == '1') mask_or += 1ULL<<(35-k);
                else if (s[i] == 'X') floating[k] = true;
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
            key |= mask_or;  
            override_all(m, key, val, floating);
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
