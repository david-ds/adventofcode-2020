#include <iostream>
#include <ctime>

#define MAX_SIZE 1000
#define O_NOP 0
#define O_ACC 1
#define O_JMP 2

using namespace std;

typedef struct Instruction{
    int op;
    int arg;
} Instruction;

int nop(int *i, int a, int arg) {
    (*i)++;
    return a;
}

int acc(int *i, int a, int arg) {
    (*i)++;
    return a+arg;
}

int jmp(int *i, int a, int arg) {
    (*i) += arg;
    return a;
}

int exec(int *i, int a, Instruction ins) {
    switch (ins.op) {
    case O_NOP:
        return nop(i, a, ins.arg);
        break;
    case O_ACC:
        return acc(i, a, ins.arg);
        break;
    case O_JMP:
        return jmp(i, a, ins.arg);
        break;
    default:
        break;
    }
    return 0;
}

int run(char* s) {
    Instruction code[MAX_SIZE];
    int k = -1, i = 0;
    while (s[i]) {
        Instruction inst;
        if (s[i] == 'n') inst.op = O_NOP;
        else if (s[i] == 'a') inst.op = O_ACC;
        else if (s[i] == 'j') inst.op = O_JMP;
        else {
            i++;
            continue;
        }
        i += 4;
        int f = 1;
        inst.arg = 0;
        if (s[i] == '-') f = -1;
        i++;
        while (s[i] >= '0' && s[i] <= '9') {
            inst.arg = inst.arg*10 + (s[i]-'0');
            i++;
        }
        inst.arg *= f;
        if (s[i] == '\n') i++;
        code[++k] = inst;
    }

    int a = 0;
    i = 0;
    bool seen[MAX_SIZE] = {false}; 
    while (!seen[i]) {
        seen[i] = true;
        a = exec(&i, a, code[i]);
    }
    return a;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    auto answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
