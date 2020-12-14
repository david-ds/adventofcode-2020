#include <iostream>
#include <ctime>

#define MAX_SIZE 100

using namespace std;

ostream& operator<<(ostream& dest, __int128_t value) {
    ostream::sentry s( dest );
    if ( s ) {
        __uint128_t tmp = value < 0 ? -value : value;
        char buffer[ 128 ];
        char* d = end( buffer );
        do
        {
            -- d;
            *d = "0123456789"[ tmp % 10 ];
            tmp /= 10;
        } while ( tmp != 0 );
        if ( value < 0 ) {
            -- d;
            *d = '-';
        }
        int len = end( buffer ) - d;
        if ( dest.rdbuf()->sputn( d, len ) != len ) {
            dest.setstate( ios_base::badbit );
        }
    }
    return dest;
}

// To compute x^y under modulo m 
__int128_t power(__int128_t x, __int128_t y, __int128_t m) {
    if (y == 0) return 1;
    __int128_t p = power(x, y / 2, m) % m;
    p = (p * p) % m;
  
    return (y % 2 == 0) ? p : (x * p) % m;
}
  
// Function to find modular inverse of a under modulo m 
// Assumption: m is prime 
__int128_t modInverse(__int128_t a, __int128_t m) {
    return power(a, m - 2, m);
}

// k is size of num[] and rem[].  Returns the smallest
// number x such that:
//  x % num[0] = rem[0],
//  x % num[1] = rem[1],
//  ..................
//  x % num[k-2] = rem[k-1]
// Assumption: Numbers in num[] are pairwise coprime
// (gcd for every pair is 1)
__int128_t findMinX(__int128_t num[], __int128_t rem[], int k) {
    // Compute product of all numbers
    __int128_t prod = 1;
    for (int i = 0; i < k; i++) prod *= num[i];

    // Initialize result
    __int128_t result = 0;

    // Apply above formula
    for (int i = 0; i < k; i++) {
        __int128_t pp = prod / num[i];
        result += rem[i] * modInverse(pp, num[i]) * pp;
    }

    return result % prod;
}

__int128_t sanitize_modulo(__int128_t x, __int128_t y) {
    return (y - (x % y)) % y;
}

const __int128_t BASE = 10;

__int128_t run(char* s) {
    __int128_t f[MAX_SIZE], p[MAX_SIZE], curr_p = 0;
    int i = 0, n = 0;

    while (s[i] != '\n') i++;
    i++;
    while (s[i] && s[i] != '\n') {
        if (s[i] == 'x') {
            i++;
            if (s[i] == ',') i++;
            curr_p++;
            continue;
        }
        while (s[i] >= '0' && s[i] <= '9') {
            f[n] = f[n]*BASE + (__int128_t)(s[i] - '0');
            i++;
        }
        p[n] = curr_p; curr_p++;
        n++;
        if (s[i] == ',') i++;
    }

    for (i = 0; i < n; i++) {
        p[i] = sanitize_modulo(p[i], f[i]);
    }

    return findMinX(f, p, n);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    __int128_t answer = run(argv[1]);

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
