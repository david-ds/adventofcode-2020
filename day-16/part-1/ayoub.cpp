#include <iostream>
#include <ctime>

#define MAX_FIELDS 100
#define N_RANGES 2

using namespace std;

typedef struct Range {
    int from, to;
} Range;

typedef struct Field {
    Range ranges[N_RANGES];
} Field;

int parse_int(char* s, int *i) {
    int x = 0;
    while (s[*i] >= '0' && s[*i] <= '9') {
        x = x*10 + s[*i]-'0';
        (*i)++;
    }
    return x;
}

int run(char* s) {
    Field fields[MAX_FIELDS];
    int k = 0, i = 0, count = 0, x = 0;

    while (!(s[i] == '\n' && s[i+1] == '\n')) {
        if (s[i] == '\n') { i++; continue; }
        while (s[i] != ':') i++;
        i += 2;
        fields[k].ranges[0].from = parse_int(s, &i);
        i++;
        fields[k].ranges[0].to = parse_int(s, &i);
        i += 4;
        fields[k].ranges[1].from = parse_int(s, &i);
        i++;
        fields[k].ranges[1].to = parse_int(s, &i);
        k++;
    }
    i += 2;
    while (s[i] != '\n') i++;
    i++;
    while (s[i] != '\n') i++;
    i += 2;
    while (s[i] != '\n') i++;
    i++;

    while (s[i]) {
        if (s[i] == '\n' || s[i] == ',')  { i++; continue; }
        x = parse_int(s, &i);
        bool is_valid = false;
        for (int j = 0; j < k; j++) {
            if ((fields[j].ranges[0].from <= x && x <= fields[j].ranges[0].to) ||
                (fields[j].ranges[1].from <= x && x <= fields[j].ranges[1].to)) {
                is_valid = true;
                break;
            }
        }
        if (!is_valid) count += x;
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
