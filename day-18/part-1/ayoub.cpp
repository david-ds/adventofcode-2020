#include <iostream>
#include <ctime>

#define OP_ADD 1
#define OP_MUT 2

using namespace std;

uint64_t parse_int(char *s, int *i) {
    uint64_t r = 0;
    while (s[*i] >= '0' && s[*i] <= '9') {
        r = r*10ULL + (uint64_t)(s[*i]-'0');
        (*i)++;
    }
    return r;
}

uint64_t eval(char *s, int *i) {
    uint64_t r = 0, x = 0;
    uint8_t pending_op = 0;
    while (s[*i] && s[*i] != '\n' && s[*i] != ')') {
        if (s[*i] == '(') {
            (*i)++;
            x = eval(s, i);
            // s[i] should be ')'
            (*i)++;
            if (pending_op == OP_ADD) r += x;
            else if (pending_op == OP_MUT) r *= x;
            else r = x;
            continue;
        }
        if (s[*i] >= '0' && s[*i] <= '9') {
            x = parse_int(s, i);
            if (pending_op == OP_ADD) r += x;
            else if (pending_op == OP_MUT) r *= x;
            else r = x;
            continue;
        }
        if (s[*i] == '+') {
            pending_op = OP_ADD;
            (*i)++;
            continue;
        }
        if (s[*i] == '*') {
            pending_op = OP_MUT;
            (*i)++;
            continue;
        }
        (*i)++;
    }
    return r;
}

uint64_t run(char* s) {
    int i = 0;
    uint64_t sum = 0;
    while (s[i]) {
        sum += eval(s, &i);
        if (s[i] == '\n') i++;
    }
    return sum;
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
