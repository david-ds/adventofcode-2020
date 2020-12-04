#include <iostream>
#include <ctime>

using namespace std;

bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

bool is_n_digits(char *s, int& i, int n) {
    i += 4;
    int l = 0;
    while (s[i] && s[i] != ' ' && s[i] != '\n') {
        if (!is_digit(s[i])) return false;
        l++; i++;
        if (l > n) return false;
    }
    return l == n;
}

bool is_n_digits_bounded(char *s, int& i, int n, int lower, int upper) {
    i += 4;
    int x = 0, l = 0;
    while (s[i] && s[i] != ' ' && s[i] != '\n') {
        if (!is_digit(s[i])) return false;
        x = x*10 + (int)(s[i] - '0');
        l++; i++;
        if (l > n) return false;
    }
    if (l != n) return false;
    if (x >= lower && x <= upper) return true;
    return false;
}

bool is_valid_byr(char *s, int& i) {
    return is_n_digits_bounded(s, i, 4, 1920, 2002);
}

bool is_valid_iyr(char *s, int& i) {
    return is_n_digits_bounded(s, i, 4, 2010, 2020);
}

bool is_valid_eyr(char *s, int& i) {
    return is_n_digits_bounded(s, i, 4, 2020, 2030);
}

bool is_valid_hgt(char *s, int& i) {
    i += 4;
    int x = 0;
    while (s[i] && s[i] != ' ' && s[i] != '\n' && is_digit(s[i])) {
        x = x*10 + (int)(s[i] - '0');
        if (x > 193) return false;
        i++;
    }
    if (x < 59) return false;
    if (s[i] != 'c' && s[i] != 'i') return false;
    if (s[i] == 'c' && s[i+1] != 'm') return false;
    if (s[i] == 'i' && s[i+1] != 'n') return false;
    if (s[i+2] != '\0' && s[i+2] != ' ' && s[i+2] != '\n') return false;
    if (s[i] == 'c' && x >= 150 && x <= 193) { i += 2; return true; }
    if (s[i] == 'i' && x >= 59 && x <= 76) { i += 2; return true; }
    return false;
}

bool is_valid_hcl(char *s, int& i) {
    i += 4;
    if (s[i] != '#') return false;
    i++;
    int l = 0;
    while (s[i] && s[i] != ' ' && s[i] != '\n' && (is_digit(s[i]) || (s[i] >= 'a' && s[i] <= 'f'))) {
        l++; i++;
        if (l > 6) return false;
    }
    if (s[i] != '\0' && s[i] != ' ' && s[i] != '\n') return false;
    return l == 6;
}

bool is_valid_ecl(char *s, int& i) {
    i += 4;
    if (!(s[i] && s[i+1] && s[i+2])) return false;
    if (s[i] == 'a' && s[i+1] == 'm' && s[i+2] == 'b' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'b' && s[i+1] == 'l' && s[i+2] == 'u' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'b' && s[i+1] == 'r' && s[i+2] == 'n' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'g' && s[i+1] == 'r' && s[i+2] == 'y' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'g' && s[i+1] == 'r' && s[i+2] == 'n' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'h' && s[i+1] == 'z' && s[i+2] == 'l' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    if (s[i] == 'o' && s[i+1] == 't' && s[i+2] == 'h' && (s[i+3] == '\0' || s[i+3] == ' ' || s[i+3] == '\n')) {
        i += 3; return true;
    }
    return false;
}

bool is_valid_pid(char *s, int& i) {
    return is_n_digits(s, i, 9);
}

void output_passpport(char *s, int start, int end) {
    for (int i = start; i <= end; i++) cout << s[i];
    cout << "\n";
}

int run(char* s) {
    int i = 0, count = 0, pass = 0;
    int byr = 0, iyr = 0, eyr = 0, hgt = 0, hcl = 0, ecl = 0, pid = 0;
    int last = 0;
    while (s[i]) {
        if (s[i] == '\n' && s[i+1] == '\n') {
            if (byr + iyr + eyr + hgt + hcl + ecl + pid == 7) count++;
            byr = 0; iyr = 0; eyr = 0; hgt = 0; hcl = 0; ecl = 0; pid = 0;
            i += 2;
            pass++;
            last = i;
            continue;
        }
        if (s[i+1] && s[i+2] && s[i+3]) {
            if (s[i] == 'b' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') {
                if (is_valid_byr(s, i)) byr = 1;
            } else if (s[i] == 'i' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') {
                if (is_valid_iyr(s, i)) iyr = 1;
            } else if (s[i] == 'h' && s[i+1] == 'g' && s[i+2] == 't' && s[i+3] == ':') {
                if (is_valid_hgt(s, i)) eyr = 1;
            } else if (s[i] == 'e' && s[i+1] == 'y' && s[i+2] == 'r' && s[i+3] == ':') {
                if (is_valid_eyr(s, i)) hgt = 1;
            } else if (s[i] == 'h' && s[i+1] == 'c' && s[i+2] == 'l' && s[i+3] == ':') {
                if (is_valid_hcl(s, i)) hcl = 1;
            } else if (s[i] == 'e' && s[i+1] == 'c' && s[i+2] == 'l' && s[i+3] == ':') {
                if (is_valid_ecl(s, i)) ecl = 1;
            } else if (s[i] == 'p' && s[i+1] == 'i' && s[i+2] == 'd' && s[i+3] == ':') {
                if (is_valid_pid(s, i)) pid = 1;
            } else i++;
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
