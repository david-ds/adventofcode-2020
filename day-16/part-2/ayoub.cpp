#include <iostream>
#include <unordered_set>
#include <ctime>

#define MAX_FIELDS 50
#define N_RANGES 2

using namespace std;

typedef struct Range {
    uint64_t from, to;
} Range;

typedef struct Field {
    bool is_important = false;
    Range ranges[N_RANGES];
} Field;

uint64_t parse_int(char* s, int *i) {
    uint64_t x = 0;
    while (s[*i] >= '0' && s[*i] <= '9') {
        x = x*10ULL + (uint64_t)(s[*i]-'0');
        (*i)++;
    }
    return x;
}

bool all_uniq(unordered_set<int> possibilities[], int k) {
    for (int i = 0; i < k; i++) {
        if (possibilities[i].size() > 1) return false;
    }
    return true;
}

uint64_t run(char* s) {
    Field fields[MAX_FIELDS];
    int k = 0, i = 0, j = 0;
    uint64_t x = 0, count = 0;
    uint64_t values[MAX_FIELDS] = {0}, current[MAX_FIELDS] = {0};
    unordered_set<int> possibilities[MAX_FIELDS];

    while (!(s[i] == '\n' && s[i+1] == '\n')) {
        if (s[i] == '\n') { i++; continue; }
        
        while (s[i] != ':') {
            if (s[i] == 'd' && s[i+1] == 'e' && s[i+2] == 'p' && s[i+3] == 'a' && s[i+4] == 'r' && s[i+5] == 't' && s[i+6] == 'u' && s[i+7] == 'r' && s[i+8] == 'e') {
                i += 9;
                fields[k].is_important = true;
            }
            i++;
        }
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
    while (s[i] != '\n') {
        values[j] = parse_int(s, &i);
        j++;
        i++;
    }
    i += 2;
    while (s[i] != '\n') i++;
    i++;

    int p = 0;
    for (p = 0; p < k; p++) {
        for (j = 0; j < k; j++) {
            possibilities[p].insert(j);
        }
    }
    p = 0;
    bool is_valid = false;
    while (s[i]) {
        if (s[i] == '\n') {
            for (p = 0; p < k; p++) {
                x = current[p];
                for (j = 0; j < k; j++) {
                    if (!((fields[j].ranges[0].from <= x && x <= fields[j].ranges[0].to) ||
                         (fields[j].ranges[1].from <= x && x <= fields[j].ranges[1].to))) {
                        possibilities[p].erase(j);
                    }
                }
            }
            p = 0;
            i++;
            continue;
        }
        else if (s[i] == ',')  { i++; continue; }
        x = parse_int(s, &i);
        is_valid = false;
        for (j = 0; j < k; j++) {
            if ((fields[j].ranges[0].from <= x && x <= fields[j].ranges[0].to) ||
                (fields[j].ranges[1].from <= x && x <= fields[j].ranges[1].to)) {
                is_valid = true;
                break;
            }
        }
        current[p] = x; p++;
        if (!is_valid) {
            while (s[i] && s[i] != '\n') i++;
            p = 0;
            if (s[i] == '\n') i++;
        }
    }
    if (is_valid) {
        for (p = 0; p < k; p++) {
            x = current[p];
            for (j = 0; j < k; j++) {
                if (!((fields[j].ranges[0].from <= x && x <= fields[j].ranges[0].to) ||
                    (fields[j].ranges[1].from <= x && x <= fields[j].ranges[1].to))) {
                    possibilities[p].erase(j);
                }
            }
        }
    }

    while (!all_uniq(possibilities, k)) {
        for (p = 0; p < k; p++) {
            if (possibilities[p].size() == 1) {
                for (const int& a: possibilities[p]) {
                    for (j = 0; j < k; j++) {
                        if (j == p) continue;
                        possibilities[j].erase(a);
                    }
                }
            }
        }
    }

    count = 1ULL;
    for (p = 0; p < k; p++) {
        for (const int& a: possibilities[p]) {
            Field field = fields[a];
            uint64_t value = values[p];
            if (field.is_important) count *= value;
        }
    }
    

    return count;
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
