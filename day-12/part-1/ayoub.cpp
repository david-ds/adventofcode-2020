#include <iostream>
#include <ctime>

#define NORTH 0
#define WEST  1
#define SOUTH 2
#define EAST  3

using namespace std;

typedef struct Ship {
    int direction;
    int x, y;
} Ship;

int abs(int x) {
    return (x<0)?(-x):x;
}

int run(char* s) {
    int i = 0;
    Ship ship{EAST, 0, 0};
    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        char c = s[i];
        int v = 0;
        i++;
        while (s[i] >= '0' && s[i] <= '9') {
            v = v*10 + s[i] - '0'; i++;
        }
        if (c == 'N') ship.y += v;
        else if (c == 'S') ship.y -= v;
        else if (c == 'E') ship.x += v;
        else if (c == 'W') ship.x -= v;
        else if (c == 'L') ship.direction = (ship.direction + (v / 90) + 4) % 4;
        else if (c == 'R') ship.direction = (ship.direction - (v / 90) + 4) % 4;
        else if (c == 'F') {
            if (ship.direction == NORTH) ship.y += v;
            else if (ship.direction == SOUTH) ship.y -= v;
            else if (ship.direction == EAST) ship.x += v;
            else if (ship.direction == WEST) ship.x -= v;
        }
    }
    return abs(ship.x)+abs(ship.y);
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
