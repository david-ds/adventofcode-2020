#include <iostream>
#include <ctime>

#define WIDTH 96
#define HEIGHT 99
#define MAX_DIAG 140

using namespace std;

void get_adj(char *s, int i, int j, int* adj, int* size) {
    int u[8] = {-1, -1, -1,  0,  0,  1,  1,  1},
        v[8] = {-1,  0,  1, -1,  1, -1,  0,  1};
    *size = 0;
    for (int k = 0; k < 8; k++) {
        int max_f = MAX_DIAG;
        if (u[k] == 0) max_f = WIDTH;
        else if (v[k] == 0) max_f = HEIGHT;
        for (int f = 1; f < max_f; f++) {
            if (i+u[k]*f < 0) break;
            if (i+u[k]*f >= HEIGHT) break;
            if (j+v[k]*f < 0) break;
            if (j+v[k]*f >= WIDTH) break;
            int curr = (i+u[k]*f)*(WIDTH+1)+(j+v[k]*f);
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
        int i = curr/(WIDTH+1), j = curr%(WIDTH+1);
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
    int occupied = 0, new_occupied = 0;
    int nodes[WIDTH*HEIGHT], nodes_size = 0, changed[WIDTH*HEIGHT], adj[WIDTH*HEIGHT];
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            int curr = i*(WIDTH+1)+j;
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
