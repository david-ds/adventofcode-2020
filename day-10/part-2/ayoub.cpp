#include <iostream>
#include <algorithm>
#include <ctime>

#define MAX_SIZE 200

using namespace std;


uint64_t run(char* s) {
    uint64_t l[MAX_SIZE];
    uint64_t x, i = 0, max = 0, size = 0;
    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        x = 0;
        while (s[i] >= '0' && s[i] <= '9') {
            x = x*10 + s[i]-'0';
            i++;
        }
        max = (max<x)?x:max;
        l[size] = x; size++;
    }
    l[size] = max+3;
    size++;
    sort(l, l+size);

    uint64_t f, f_1, f_2, f_3;
    f_3 = 1;
    f_2 = f_3;
    if (l[1] <= 3) f_2 += 1;
    f_1 = f_2;
    if (l[2] - l[0] <= 3) f_1 += f_3;
    if (l[2] <= 3) f_1 += 1;
    for (i = 3; i < size; i++) {
        f = f_1;
        if (l[i] - l[i-2] <= 3) f += f_2;
        if (l[i] - l[i-3] <= 3) f += f_3;
        f_3 = f_2;
        f_2 = f_1;
        f_1 = f;
    }
    
    return f;
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
