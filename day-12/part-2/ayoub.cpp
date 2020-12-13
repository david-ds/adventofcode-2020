#include <iostream>
#include <ctime>

#define NORTH 0
#define WEST  1
#define SOUTH 2
#define EAST  3

using namespace std;

typedef struct Point {
    int x, y;
} Point;

int abs(int x) {
    return (x<0)?(-x):x;
}

int run(char* s) {
    int i = 0;
    Point ship{0, 0}, waypoint{10, 1};

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
        if (c == 'N') waypoint.y += v;
        else if (c == 'S') waypoint.y -= v;
        else if (c == 'E') waypoint.x += v;
        else if (c == 'W') waypoint.x -= v;
        else if (c == 'L' || c == 'R') {
            if (c == 'R') v = 360-v;
            v = ((v % 360) + 360) % 360;
            for (int k = 0; k < v / 90; k++) {
                int x = -waypoint.y;
                int y = waypoint.x;
                waypoint.x = x; waypoint.y = y;
            }
        }
        else if (c == 'F') {
            ship.x += waypoint.x * v;
            ship.y += waypoint.y * v;
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
