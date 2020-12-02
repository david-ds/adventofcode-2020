#include <iostream>
#include <sstream>
#include <regex>
#include <string>
#include <ctime>

using namespace std;

const regex pattern("(\\d+)-(\\d+) ([a-z]): ([a-z]+)"); 

bool check(int a, int b, char c, string password) {
    return (password.at(a-1) == c) ^ (password.at(b-1) == c);
}

int run(string s) {
    istringstream is(s);
    string line;
    smatch sm;
    int count = 0;
    while (getline(is, line)) {
        regex_search(line, sm, pattern);
        if (!sm.size()) continue;
        int a = stoi(string(sm[1])), b = stoi(string(sm[2]));
        char c = string(sm[3]).at(0);
        string password = string(sm[4]);
        if (check(a, b, c, password)) count++;
    }
    return count;
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
