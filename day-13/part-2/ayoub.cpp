#include <iostream>
#include <ctime>

#define MAX_SIZE 100

using namespace std;

// Returns modulo inverse of a with respect to m using extended 
// Euclid Algorithm. Refer below post for details: 
// https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/ 
int64_t inv(int64_t a, int64_t m) 
{ 
    int64_t m0 = m, t, q; 
    int64_t x0 = 0, x1 = 1; 
  
    if (m == 1) 
       return 0; 
  
    // Apply extended Euclid Algorithm 
    while (a > 1) 
    { 
        // q is quotient 
        q = a / m; 
  
        t = m; 
  
        // m is remainder now, process same as 
        // euclid's algo 
        m = a % m, a = t; 
  
        t = x0; 
  
        x0 = x1 - q * x0; 
  
        x1 = t; 
    } 
  
    // Make x1 positive 
    if (x1 < 0) 
       x1 += m0; 
  
    return x1; 
} 
  
// k is size of num[] and rem[].  Returns the smallest 
// number x such that: 
//  x % num[0] = rem[0], 
//  x % num[1] = rem[1], 
//  .................. 
//  x % num[k-2] = rem[k-1] 
// Assumption: Numbers in num[] are pairwise coprime 
// (gcd for every pair is 1) 
int64_t findMinX(int64_t num[], int64_t rem[], int k) 
{ 
    // Compute product of all numbers 
    int64_t prod = 1; 
    for (int i = 0; i < k; i++) 
        prod *= num[i]; 
  
    // Initialize result 
    int64_t result = 0; 
  
    // Apply above formula 
    for (int i = 0; i < k; i++) 
    { 
        int64_t pp = prod / num[i]; 
        result += rem[i] * inv(pp, num[i]) * pp; 
    } 
  
    return result % prod; 
}

int64_t sanitize_modulo(int64_t x, int64_t y) {
    int a = (int)x; a *= -1;
    int b = (int)y;
    return (int64_t)(((a % b) + b) % b);
}

int64_t run(char* s) {
    int64_t f[MAX_SIZE], p[MAX_SIZE], curr_p = 0;
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
            f[n] = f[n]*10LL + (int64_t)(s[i] - '0');
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
    int64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
