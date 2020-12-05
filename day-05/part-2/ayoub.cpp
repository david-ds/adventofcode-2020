#include <iostream>
#include <ctime>

using namespace std;

int run(char* s) {
    int i = -1, offset = 0;
    int curr_r = 0, curr_c = 0;
    int max = 0;
    bool set[1024] = {false};
    while (s[++i]) {
        switch (s[i]) {
        case 'B':
            curr_r += 1 << (6-((i-offset)%10));
            break;
        case 'R':
            curr_c += 1 << (9-((i-offset)%10));
            break;
        case '\n':
            offset++;
            break;
        default:
            break;
        }
        if ((i-offset+1) % 10 == 0) {
            int curr = 8 * curr_r + curr_c;
            set[curr] = true;
            max = (curr>max)?curr:max;
            curr_r = 0; curr_c = 0;
        }
    }
    for (i = max; i >= 0; i--) {
        if (!set[i]) return i;
    }
    return max;
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
