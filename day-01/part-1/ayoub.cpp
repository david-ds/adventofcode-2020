#include <iostream>
#include <sstream>
#include <unordered_set>
#include <string>
#include <ctime>

using namespace std;

int run(string s) {
    istringstream is(s);
    string line;
    unordered_set<int> set;
    while (getline(is, line, '\n')) {
        set.insert(stoi(line));
    }
    for (const int& x: set) {
        if (set.find(2020 - x) != set.end()) {
            return (2020 - x) * x;
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
    auto answer = run(string(argv[1]));
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
