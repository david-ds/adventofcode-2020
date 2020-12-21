#include <iostream>
#include <unordered_set>
#include <ctime>

#define SIZE 10
#define MAX_BORDER 1024
#define MASK 1023U

using namespace std;

enum Side {
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,
};

uint16_t inverse[MAX_BORDER] = {0};

typedef struct Tile {
    uint16_t id;
    uint16_t borders[4];
    uint16_t get_side(Side side, int orientation) const {
        uint64_t rotated[4] = {borders[0], borders[1], borders[2], borders[3]};
        if ((orientation%4) == 1) {
            rotated[0] = inverse[borders[3]];
            rotated[1] = borders[0];
            rotated[2] = inverse[borders[1]];
            rotated[3] = borders[2];
        } else if ((orientation%4) == 2) {
            rotated[0] = inverse[borders[2]];
            rotated[1] = inverse[borders[3]];
            rotated[2] = inverse[borders[0]];
            rotated[3] = inverse[borders[1]];
        } else if ((orientation%4) == 3) {
            rotated[0] = borders[1];
            rotated[1] = inverse[borders[2]];
            rotated[2] = borders[3];
            rotated[3] = inverse[borders[0]];
        }
        return rotated[side];
    };
} Tile;

uint16_t border_to_uint16(const char* s, int i, bool vertical, bool reversed) {
    uint16_t x = 0U;
    for (int j = 0; j < SIZE; j++) {
        char c = 0;
        if (!vertical) c = s[i+j];
        else c = s[i+j*(SIZE+1)];
        if (c == '#') {
            if (reversed) x += 1U << j;
            else x += 1U << (SIZE-1-j);
        }
    }
    return x & MASK;
}

uint64_t run(const char* s) {
    int i = 0;
    unordered_set<Tile*> tiles_by_border[MAX_BORDER];
    unordered_set<Tile*> tiles;

    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        if (s[i] == 'T') i += 5;
        uint16_t id = 0;
        while (s[i] >= '0' && s[i] <= '9') {
            id = id*10U + (uint16_t)(s[i]-'0');
            i++; 
        }
        i += 2;
        Tile *tile = new Tile;
        tile->id = id;

        tile->borders[0] = border_to_uint16(s, i, false, false);
        inverse[tile->borders[0]] = border_to_uint16(s, i, false, true);
        inverse[inverse[tile->borders[0]]] = tile->borders[0];

        tile->borders[1] = border_to_uint16(s, i+SIZE-1, true, false);
        inverse[tile->borders[1]] = border_to_uint16(s, i+SIZE-1, true, true);
        inverse[inverse[tile->borders[1]]] = tile->borders[1];

        tile->borders[2] = border_to_uint16(s, i+(SIZE+1)*(SIZE-1), false, false);
        inverse[tile->borders[2]] = border_to_uint16(s, i+(SIZE+1)*(SIZE-1), false, true);
        inverse[inverse[tile->borders[2]]] = tile->borders[2];

        tile->borders[3] = border_to_uint16(s, i, true, false);
        inverse[tile->borders[3]] = border_to_uint16(s, i, true, true);
        inverse[inverse[tile->borders[3]]] = tile->borders[3];

        tiles_by_border[tile->borders[0]].insert(tile);
        tiles_by_border[tile->borders[1]].insert(tile);
        tiles_by_border[tile->borders[2]].insert(tile);
        tiles_by_border[tile->borders[3]].insert(tile);

        tiles_by_border[inverse[tile->borders[0]]].insert(tile);
        tiles_by_border[inverse[tile->borders[1]]].insert(tile);
        tiles_by_border[inverse[tile->borders[2]]].insert(tile);
        tiles_by_border[inverse[tile->borders[3]]].insert(tile);

        tiles.insert(tile);

        i += (SIZE+1)*SIZE-1;
    }

    uint64_t res = 1ULL;
    for (const Tile* tile: tiles) {
        for (int orientation = 0; orientation < 4; orientation++) {
            uint16_t north_border = tile->get_side(NORTH, orientation);
            uint16_t west_border  = tile->get_side(WEST, orientation);
            if (tiles_by_border[north_border].size() == 1 && tiles_by_border[west_border].size() == 1) {
                res *= (uint64_t)tile->id;
                break;
            }
        }
    }

    return res;

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
