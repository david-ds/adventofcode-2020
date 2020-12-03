#include <iostream>
#include <string>
#include <ctime>

using namespace std;

const uint64_t SLOPE_RIGHT[5] = {1, 3, 5, 7, 1};
const uint64_t SLOPE_DOWN[5] =  {1, 1, 1, 1, 2};

const uint64_t WIDTH = 31;
const uint64_t HEIGHT = 323;

uint64_t run(char* s) {
    uint64_t res = 1;
    for (uint64_t k = 0; k < 5; k++) {
        uint64_t j = -SLOPE_RIGHT[k], count = 0;
        for (uint64_t i = 0; i < HEIGHT; i += SLOPE_DOWN[k]) {
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
    uint64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
