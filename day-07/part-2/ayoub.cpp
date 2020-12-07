#include <iostream>
#include <ctime>
#include <string>
#include <vector>
#include <unordered_map>

using namespace std;

typedef struct Bag {
    int n;
    string name;
} Bag;

int count_shiny(unordered_map<string, vector<Bag>*>& g, const string& node, unordered_map<string, int>& visited) {
    if (visited.find(node) != visited.end()) return visited[node];
    vector<Bag>* children = g[node];
    if (!children) return 0;
    int sum = 0;
    for (Bag child: *children) {
        sum += child.n + child.n * count_shiny(g, child.name, visited);
    }
    visited[node] = sum;
    return sum;
}

int run(char* s) {
    int i = 0, node_i = -1, child_i = -1, child_f = 0;
    unordered_map<string, vector<Bag>*> g;
    vector<Bag>* children;
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
                if (g.find(snode) == g.end()) {
                    children = new vector<Bag>;
                    g[snode] = children;
                } else {
                    children = g[snode];
                }
                mode_node = false;
            } else {
                child[++child_i] = '\0';
                child_i = -1;
                schild = string(child);
                children->push_back(Bag{child_f, schild});
                child_f = 0;
            }
            i += 4;
            if (s[i] == 's') i++;
            if (s[i] == ',') i += 2;
            else if (s[i] == ' ') i += 9;
            if (s[i] == 'n') {
                i += 13;
                continue;
            }
            while (s[i] <= '9' && s[i] >= '0') {
                child_f = child_f*10+(s[i]-'0');
                i++;
            }
            if (s[i] == ' ') i++;
            continue;
        }
        if (mode_node) node[++node_i] = s[i];
        else child[++child_i] = s[i];
        i++;
    }

    unordered_map<string, int> visited;
    return count_shiny(g, "shiny gold", visited);
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
