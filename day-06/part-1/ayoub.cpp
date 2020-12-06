#include <iostream>
#include <ctime>

using namespace std;

int run(char* s) {
    bool seen[26] = {false};
    int i = -1, sum = 0, curr = 0;
    while (s[++i]) {
        if (s[i] >= 'a' && s[i] <= 'z') {
            if (!seen[s[i]-'a']) {
                seen[s[i]-'a'] = true;
                curr++;
            }
        } else if (s[i] == '\n' && s[i+1] == '\n') {
            for (int k = 0; k < 26; k++) seen[k] = false;
            sum += curr; 
            curr = 0;
        }
    }
    sum += curr; 
    return sum;
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
