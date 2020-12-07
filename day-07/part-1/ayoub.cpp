#include <iostream>
#include <ctime>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>

using namespace std;

int count_shiny(unordered_map<string, vector<string>*>& g, const string& node, unordered_set<string>& visited) {
    if (visited.find(node) != visited.end()) return 0;
    vector<string>* parents = g[node];
    visited.insert(node);
    if (!parents) return 1;
    int sum = 1;
    for (string child: *parents) {
        sum += count_shiny(g, child, visited);
    }
    return sum;
}

int run(char* s) {
    int i = 0, node_i = -1, child_i = -1;
    unordered_map<string, vector<string>*> g;
    vector<string>* parents;
    char node[100], child[100];
    string snode, schild;
    bool mode_node = true;

    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        if (s[i] == '.') {
            mode_node = true;
            node_i = -1;
            i++;
            continue;
        }
        if (s[i] == ' ' && s[i+1] == 'b' && s[i+2] == 'a' && s[i+3] == 'g' && 
           ((s[i+4] == 's' && (s[i+5] == ' ' || s[i+5] == '.' || s[i+5] == ','))
                            || s[i+4] == ' ' || s[i+4] == '.' || s[i+4] == ',')) {
            if (mode_node) {
                node[++node_i] = '\0';
                snode = string(node);
                mode_node = false;
            } else {
                child[++child_i] = '\0';
                child_i = -1;
                schild = string(child);
                if (g.find(schild) == g.end()) {
                    parents = new vector<string>;
                    g[schild] = parents;
                } else {
                    parents = g[schild];
                }
                parents->push_back(snode);
            }
            i += 4;
            if (s[i] == 's') i++;
            if (s[i] == ',') i += 2;
            else if (s[i] == ' ') i += 9;
            if (s[i] == 'n') {
                i += 13;
                continue;
            }
            while ((s[i] <= '9' && s[i] >= '0') || s[i] == ' ') i++;
            continue;
        }
        if (mode_node) node[++node_i] = s[i];
        else child[++child_i] = s[i];
        i++;
    }

    unordered_set<string> visited;
    return count_shiny(g, "shiny gold", visited)-1;
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
