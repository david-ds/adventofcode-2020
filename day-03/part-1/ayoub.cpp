#include <iostream>
#include <ctime>

using namespace std;

const int SLOPE_RIGHT = 3;
const int SLOPE_DOWN =  1;

const int WIDTH = 31;
const int HEIGHT = 323;

int run(char* s) {
    int j = -SLOPE_RIGHT, count = 0;
    for (int i = 0; i < HEIGHT; i += SLOPE_DOWN) {
        j = (j + SLOPE_RIGHT) % WIDTH;
        if (s[i*(WIDTH+1)+j] == '#') count++;
    }
    return count;
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
