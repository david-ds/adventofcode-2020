#include <iostream>
#include <unordered_set>
#include <string>
#include <ctime>

#define MAX_RULES_SIZE 200
#define MAX_OR_LIST_SIZE 4
#define MAX_AND_LIST_SIZE 4

using namespace std;

typedef struct Rule {
    int id = -1;
    char litteral = 0;
    int r_or[MAX_OR_LIST_SIZE][MAX_AND_LIST_SIZE];
    size_t r_or_size = 1;
    size_t r_or_sizes[MAX_OR_LIST_SIZE] = {0};
} Rule;

int parse_int(const char* s, int *i) {
    int x = 0;
    while (s[*i] >= '0' && s[*i] <= '9') {
        x = x*10 + (s[*i]-'0');
        (*i)++;
    }
    return x;
}

bool is_match(unordered_set<string> mem_true[], unordered_set<string> mem_false[], const Rule rules[], const char* s, int p, int n, int id = 0) {
    Rule rule = rules[id];
    if (rule.litteral != 0) {
        return (n - p == 1) && (rule.litteral == s[p]);
    }
    string str(s+p, s+n);
    if (mem_true[id].find(str) != mem_true[id].end()) return true;
    if (mem_false[id].find(str) != mem_false[id].end()) return false;

    for (int or_i = 0; or_i < rule.r_or_size; or_i++) {
        bool matches = true;
        int partitions = rule.r_or_sizes[or_i];
        if (partitions == 1) {
            matches = is_match(mem_true, mem_false, rules, s, p, n, rule.r_or[or_i][0]);
        } else if (partitions == 2) {
            matches = false;
            for (int i = p+1; i < n; i++) {
                matches = is_match(mem_true, mem_false, rules, s, p, i, rule.r_or[or_i][0])
                       && is_match(mem_true, mem_false, rules, s, i, n, rule.r_or[or_i][1]);
                if (matches) break;
            }
        } else if (partitions == 3) {
            matches = false;
            for (int i = p+1; i < n-1; i++) {
                for (int j = i+1; j < n; j++) {
                    matches = is_match(mem_true, mem_false, rules, s, p, i, rule.r_or[or_i][0])
                           && is_match(mem_true, mem_false, rules, s, i, j, rule.r_or[or_i][1])
                           && is_match(mem_true, mem_false, rules, s, j, n, rule.r_or[or_i][2]);
                    if (matches) break;
                }
                if (matches) break;
            }
        } else if (partitions == 4) {
            matches = false;
            for (int i = p+1; i < n-2; i++) {
                for (int j = i+1; j < n-1; j++) {
                    for (int k = j+1; k < n; k++) {
                        matches = is_match(mem_true, mem_false, rules, s, p, i, rule.r_or[or_i][0])
                               && is_match(mem_true, mem_false, rules, s, i, j, rule.r_or[or_i][1])
                               && is_match(mem_true, mem_false, rules, s, j, k, rule.r_or[or_i][2])
                               && is_match(mem_true, mem_false, rules, s, k, n, rule.r_or[or_i][3]);
                        if (matches) break;
                    }
                    if (matches) break;
                }
                if (matches) break;
            }
        } else {
            cerr << "cannot partition more than 4\n";
            return false;
        }
        if (matches) {
            mem_true[id].insert(str);
            return true;
        }
    }
    mem_false[id].insert(str);
    return false;
}

int run(const char* s) {
    Rule rules[MAX_RULES_SIZE];
    int i = 0;

    while (s[i] && !(s[i] == '\n' && s[i+1] == '\n')) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        int id = parse_int(s, &i);
        rules[id].id = id;
        rules[id].r_or_size = 1;
        rules[id].litteral = 0;
        for (int k = 0; k < MAX_OR_LIST_SIZE; k++) rules[id].r_or_sizes[k] = 0;
        i += 2;
        // litteral match
        if (s[i] == '"') {
            i++;
            rules[id].litteral = s[i];
            i += 2;
            continue;
        }
        // expression
        while (s[i] != '\n') {
            int curr = parse_int(s, &i);
            int or_i = rules[id].r_or_size-1;
            int and_i = rules[id].r_or_sizes[or_i];
            rules[id].r_or[or_i][and_i] = curr;
            rules[id].r_or_sizes[or_i]++;
            while (s[i] == ' ') i++;
            if (s[i] == '|') {
                rules[id].r_or_size++;
                i++;
            }
            while (s[i] == ' ') i++;
        }
    }
    i += 2;
    int count = 0;
    unordered_set<string> mem_true[MAX_RULES_SIZE], mem_false[MAX_RULES_SIZE];

    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        int p = i;
        while (s[i] && s[i] != '\n') i++;
        if (is_match(mem_true, mem_false, rules, s, p, i)) count++;
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
    clock_t end = clock();

    cout << "_duration:" << float( end - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
