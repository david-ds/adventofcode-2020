#include <iostream>
#include <ctime>

#define MAX_SIZE 100

using namespace std;

  // To compute x^y under modulo m 
uint64_t power(uint64_t x, uint64_t y, uint64_t m) {
    if (y == 0)
        return 1; 
    uint64_t p = power(x, y / 2, m) % m; 
    p = (p * p) % m; 
  
    return (y % 2 == 0) ? p : (x * p) % m; 
}
  
// Function to find modular inverse of a under modulo m 
// Assumption: m is prime 
uint64_t modInverse(uint64_t a, uint64_t m) {
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
uint64_t findMinX(uint64_t num[], uint64_t rem[], int k)
{
    // Compute product of all numbers
    uint64_t prod = 1;
    for (int i = 0; i < k; i++)
        prod *= num[i];

    // Initialize result
    uint64_t result = 0;

    // Apply above formula
    for (int i = 0; i < k; i++)
    {
        uint64_t pp = prod / num[i];
        result += rem[i] * modInverse(pp, num[i]) * pp;
    }

    return result % prod;
}

uint64_t sanitize_modulo(uint64_t x, uint64_t y) {
    int a = (int)x; a *= -1;
    int b = (int)y;
    return (uint64_t)(((a % b) + b) % b);
}

uint64_t run(char* s) {
    uint64_t f[MAX_SIZE], p[MAX_SIZE], curr_p = 0;
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
            f[n] = f[n]*10LL + (uint64_t)(s[i] - '0');
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
    uint64_t answer = run(argv[1]);

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
