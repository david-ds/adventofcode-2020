#include <iostream>
#include <ctime>

#define MAX_V 200

using namespace std;


int run(char* s) {
    bool exists[MAX_V] = {false};
    int x, i = 0, max = 0;
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
        exists[x] = true;
    }
    int v = 0;
    int count_1 = 0, count_3 = 0;
    while (v < max) {
        if (exists[v+1]) {
            v += 1;
            count_1++;
        } else if (exists[v+2]) {
            v += 2;
        } else if (exists[v+3]) {
            v += 3;
            count_3++;
        }
    }
    count_3++;

    return count_1 * count_3;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
