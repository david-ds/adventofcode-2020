#include <iostream>
#include <ctime>

using namespace std;

const long SLOPE_RIGHT[5] = {1, 3, 5, 7, 1};
const long SLOPE_DOWN[5] =  {1, 1, 1, 1, 2};

const long WIDTH = 31;
const long HEIGHT = 323;

long run(char* s) {
    long res = 1;
    for (long k = 0; k < 5; k++) {
        long j = -SLOPE_RIGHT[k], count = 0;
        for (long i = 0; i < HEIGHT; i += SLOPE_DOWN[k]) {
            j = (j + SLOPE_RIGHT[k]) % WIDTH;
            if (s[i*(WIDTH+1)+j] == '#') count++;
        }
        res *= count;
    }
    return res;
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
