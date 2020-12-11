#include <iostream>
#include <ctime>

#define MAX_WIDTH 100
#define MAX_HEIGHT 100

using namespace std;

int width = 0;
int height = 0;

void get_adj(char *s, int i, int j, int* adj, int* size) {
    int u[8] = {-1, -1, -1,  0,  0,  1,  1,  1},
        v[8] = {-1,  0,  1, -1,  1, -1,  0,  1};
    *size = 0;
    for (int k = 0; k < 8; k++) {
        if (i+u[k] < 0) continue;
        if (i+u[k] >= height) continue;
        if (j+v[k] < 0) continue;
        if (j+v[k] >= width) continue;
        int curr = (i+u[k])*(width+1)+(j+v[k]);
        if (s[curr] == 'L' || s[curr] == '#') {
            adj[*size] = curr; (*size)++;
        }
    }
}

bool all_empty(char *s, int* adj, int size) {
    for (int k = 0; k < size; k++) {
        if (s[adj[k]] == '#') return false;
    }
    return true;
}

bool four_or_more(char *s, int* adj, int size) {
    int count = 0;
    for (int k = 0; k < size; k++) {
        if (s[adj[k]] == '#') count++;
        if (count >= 4) return true;
    }
    return false;
}

int simulate(char *s, int *nodes, int nodes_size, int* changed, int occupied) {
    int changed_size = 0;
    int adj[8], size = 0;
    for (int k = 0; k < nodes_size; k++) {
        int curr = nodes[k];
        if (s[curr] == '.') continue;
        int i = curr/(width+1), j = curr%(width+1);
        get_adj(s, i, j, adj, &size);
        if (s[curr] == 'L') {
            if (all_empty(s, adj, size)) {changed[changed_size] = curr; changed_size++;}
        } else {
            if (four_or_more(s, adj, size)) {changed[changed_size] = curr; changed_size++;}
        }
    }
    for (int k = 0; k < changed_size; k++) {
        int curr = changed[k];
        if (s[curr] == 'L') {
            s[curr] = '#';
            occupied++;
        } else {
            s[curr] = 'L';
            occupied--;
        }
    }
    return occupied;
}

int run(char* s) {
    int i = 0;
    while (s[i]) {
        if (s[i] == '\n' && width == 0) width = i;
        if (s[i] == '\n' && s[i+1] != '\n') height++;
        i++;
    }
    height++;
    int occupied = 0, new_occupied = 0;
    int nodes[MAX_WIDTH*MAX_HEIGHT], nodes_size = 0, changed[MAX_WIDTH*MAX_HEIGHT];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int curr = i*(width+1)+j;
            if (s[curr] == '.') continue;
            nodes[nodes_size] = curr; nodes_size++;
        }
    }
    while (true) {
        new_occupied = simulate(s, nodes, nodes_size, changed, occupied);
        if (new_occupied == occupied) break;
        occupied = new_occupied;
    }
    return occupied;
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
