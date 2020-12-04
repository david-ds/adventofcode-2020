#include <iostream>
#include <ctime>

using namespace std;


int run(char* s) {
    int i = 0, count = 0;
    int byr = 0, iyr = 0, eyr = 0, hgt = 0, hcl = 0, ecl = 0, pid = 0;
    while (s[i]) {
        if (s[i] == '\n' && s[i+1] == '\n') {
            if (byr + iyr + eyr + hgt + hcl + ecl + pid == 7) count++;
            byr = 0; iyr = 0; eyr = 0; hgt = 0; hcl = 0; ecl = 0; pid = 0;
            i += 2;
            continue;
        }
        if (s[i+1] && s[i+2] && s[i+3]) {
            if (s[i] == 'b' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') { byr = 1; i += 4; }
            else if (s[i] == 'i' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') { iyr = 1; i += 4; }
            else if (s[i] == 'h' && s[i+1] == 'g' && s[i+2] == 't' && s[i+3] == ':') { eyr = 1; i += 4; }
            else if (s[i] == 'e' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') { hgt = 1; i += 4; }
            else if (s[i] == 'h' && s[i+1] == 'c' && s[i+2] == 'l' && s[i+3] == ':') { hcl = 1; i += 4; }
            else if (s[i] == 'e' && s[i+1] == 'c' && s[i+2] == 'l' && s[i+3] == ':') { ecl = 1; i += 4; }
            else if (s[i] == 'p' && s[i+1] == 'i' && s[i+2] == 'd' && s[i+3] == ':') { pid = 1; i += 4; }
            else i++;
            continue;
        }
        i++;
    }
    if (byr + iyr + eyr + hgt + hcl + ecl + pid == 7) count++;

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
