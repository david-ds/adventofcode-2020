#include <iostream>
#include <ctime>

#define MAX_WIDTH 100
#define MAX_HEIGHT 100
#define MAX_DIAG 150

using namespace std;

int width = 0;
int height = 0;

void get_adj(char *s, int i, int j, int* adj, int* size) {
    int u[8] = {-1, -1, -1,  0,  0,  1,  1,  1},
        v[8] = {-1,  0,  1, -1,  1, -1,  0,  1};
    *size = 0;
    for (int k = 0; k < 8; k++) {
        int max_f = MAX_DIAG;
        if (u[k] == 0) max_f = width;
        else if (v[k] == 0) max_f = height;
        for (int f = 1; f < max_f; f++) {
            if (i+u[k]*f < 0) break;
            if (i+u[k]*f >= height) break;
            if (j+v[k]*f < 0) break;
            if (j+v[k]*f >= width) break;
            int curr = (i+u[k]*f)*(width+1)+(j+v[k]*f);
            if (s[curr] == 'L' || s[curr] == '#') {
                adj[*size] = curr; (*size)++;
                break;
            }
        }
    }
}

bool all_empty(char *s, int* adj, int size) {
    for (int k = 0; k < size; k++) {
        if (s[adj[k]] == '#') return false;
    }
    return true;
}

bool five_or_more(char *s, int* adj, int size) {
    int count = 0;
    for (int k = 0; k < size; k++) {
        if (s[adj[k]] == '#') count++;
        if (count >= 5) return true;
    }
    return false;
}

int simulate(char *s, int *nodes, int nodes_size, int *adj, int* changed, int occupied) {
    int changed_size = 0;
    int size = 0;
    for (int k = 0; k < nodes_size; k++) {
        int curr = nodes[k];
        if (s[curr] == '.') continue;
        int i = curr/(width+1), j = curr%(width+1);
        get_adj(s, i, j, adj, &size);
        if (s[curr] == 'L') {
            if (all_empty(s, adj, size)) {changed[changed_size] = curr; changed_size++;}
        } else {
            if (five_or_more(s, adj, size)) {changed[changed_size] = curr; changed_size++;}
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
    int nodes[MAX_WIDTH*MAX_HEIGHT], nodes_size = 0, changed[MAX_WIDTH*MAX_HEIGHT], adj[MAX_WIDTH*MAX_HEIGHT];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int curr = i*(width+1)+j;
            if (s[curr] == '.') continue;
            nodes[nodes_size] = curr; nodes_size++;
        }
    }
    while (true) {
        new_occupied = simulate(s, nodes, nodes_size, adj, changed, occupied);
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
