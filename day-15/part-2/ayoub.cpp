#include <iostream>
#include <unordered_map>
#include <ctime>


using namespace std;

int run(char* s) {
    unordered_map<int, int> seen_first, seen_second;
    int i = 0, r = 0, pos = 1;
    while (s[i]) {
        r = 0;
        while (s[i] >= '0' && s[i] <= '9') {
            r = r*10 + s[i]-'0';
            i++;
        }
        seen_first[r] = pos; pos++;
        if (s[i] == ',') i++;
    }
    while (pos <= 30000000) {
        if (!seen_first[r] || (seen_first[r] && !seen_second[r])) r = 0;
        else r = seen_second[r]-seen_first[r];
        if (!seen_first[r]) seen_first[r] = pos;
        else if (seen_first[r] && !seen_second[r]) seen_second[r] = pos;
        else if (seen_first[r] && seen_second[r]) {
            seen_first[r] = seen_second[r];
            seen_second[r] = pos;
        }
        pos++;
    }
    return r;
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
