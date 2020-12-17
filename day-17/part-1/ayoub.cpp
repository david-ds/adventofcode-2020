#include <iostream>
#include <unordered_set>
#include <ctime>

#define MAX_WIDTH 100000
#define ITERATIONS 6

using namespace std;

typedef struct Cube {
    long x, y, z;
    bool operator==(const Cube& p) const {
        return x == p.x && y == p.y && z == p.z;
    }
} Cube;

class CubeHash {
public:
    size_t operator()(const Cube& p) const {
        return p.x*10000 + p.y*100 + p.z;
    }
};

int count_active_adj(const unordered_set<Cube, CubeHash>& active, const Cube& p) {
    int count_active = 0;
    for (int u = -1; u <= 1; u++)
    for (int v = -1; v <= 1; v++)
    for (int t = -1; t <= 1; t++) {
        if (u == 0 && v == 0 && t == 0) continue;
        Cube adj{p.x+u, p.y+v, p.z+t};
        if (active.find(adj) != active.end()) count_active++;
    }
    return count_active;
}

int run(char* s) {
    int i = 0, ofst = 0, width = MAX_WIDTH;
    unordered_set<Cube, CubeHash> active;
    unordered_set<Cube, CubeHash> next_active;

    while (s[i]) {
        if (s[i] == '#') active.insert(Cube{(i-ofst)%width, (i-ofst)/width, 0});
        else if (s[i] == '\n') {
            if (width == MAX_WIDTH) width = i;
            ofst++;
        }
        i++;
    }

    for (i = 0; i < ITERATIONS; i++) {
        next_active = active;
        for (int u = -1; u <= 1; u++)
        for (int v = -1; v <= 1; v++)
        for (int t = -1; t <= 1; t++) {
            for (const Cube& p: active) {
                Cube a{p.x+u, p.y+v, p.z+t};
                int count_active = count_active_adj(active, a);
                if (active.find(a) != active.end()) {
                    // active cube
                    if (count_active == 2 || count_active == 3) next_active.insert(a);
                    else next_active.erase(a);
                } else {
                    // inactive cube
                    if (count_active == 3) next_active.insert(a);
                    else next_active.erase(a);
                }
            }
        }
        active = next_active;
    }
    
    return active.size();
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
