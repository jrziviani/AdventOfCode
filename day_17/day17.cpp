#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

enum { A, B, C };
array<int64_t, 3> registers = {0ULL, 0ULL, 0ULL};
vector<int> output;

int64_t pc = 0;

int64_t pow(int64_t a) {
    int64_t result = 1;
    while (a > 0) {
        result *= 2;
        a--;
    }
    return result;
}

int64_t oper(int64_t a) {
    if (a >= 0 && a <= 3) {
        return a;
    } else if (a == 4) {
        return registers[A];
    } else if (a == 5) {
        return registers[B];
    } else if (a == 6) {
        return registers[C];
    }
    return 0;
}

string join(const vector<int> &v) {
    string result = "";
    for (int64_t i = 0; i < v.size(); i++) {
        result += to_string(v[i]);
        if (i != v.size() - 1) {
            result += ",";
        }
    }
    return result;
}

uint64_t toint(const vector<int> &v) {
    uint64_t result = 0;
    for (int64_t i = 0; i < v.size(); i++) {
        result = result * 10 + v[i];
    }
    return result;
}

uint64_t toint(const string &s) {
    uint64_t result = 0;
    for (int64_t i = 0; i < s.size(); i += 2) {
        result = result * 10 + s[i] - '0';
    }
    return result;
}

void adv(int64_t a) { registers[A] /= pow(a); };

void bxl(int64_t a) { registers[B] ^= a; }

void bst(int64_t a) { registers[B] = a & 0x7; }

void jnz(int64_t a) { pc = a * 2; }

void bxc(int64_t a) { registers[B] ^= registers[C]; }

void out(int64_t a, vector<int> &o) { o.push_back((a & 0x7)); }

void bdv(int64_t a) { registers[B] = registers[A] / pow(a); }

void cdv(int64_t a) { registers[C] = registers[A] / pow(a); }

vector<int> run(const string &program) {
    pc = 0;
    vector<int> otp;
    while (pc < program.size()) {
        int64_t operand = program[pc + 2] - '0';

        switch (program[pc]) {
        case '0':
            adv(oper(operand));
            pc += 4;
            break;

        case '1':
            bxl(operand);
            pc += 4;
            break;

        case '2':
            bst(oper(operand));
            pc += 4;
            break;

        case '3':
            if (registers[A] > 0)
                jnz(operand);
            else
                pc += 4;
            break;

        case '4':
            bxc(operand);
            pc += 4;
            break;

        case '5':
            out(oper(operand), otp);
            pc += 4;
            break;

        case '6':
            bdv(oper(operand));
            pc += 4;
            break;

        case '7':
            cdv(oper(operand));
            pc += 4;
            break;
        }
    }
    return otp;
}

int64_t backtrack(int64_t a, int i, const string &program) {
    if (i < 0) {
        return a;
    }

    a <<= 3;

    for (int j = 0; j < 8; j++) {
        registers[A] = a + j;
        auto r = run(program);
        cout << "output: " << join(r) << ", a: " << a << endl;
        if (r[0] == program[i] - '0') {
            auto result = backtrack(a + j, i - 2, program);
            if (result >= 0) {
                return result;
            }
        }
    }

    return -1;
}

int main() {
    ifstream file("input.txt");
    string line;
    string program = "";
    while (getline(file, line)) {
        if (line.starts_with("Register A")) {
            registers[A] = stoi(line.substr(12));
        } else if (line.starts_with("Register B")) {
            registers[B] = stoi(line.substr(12));
        } else if (line.starts_with("Register C")) {
            registers[C] = stoi(line.substr(12));
        } else if (line.starts_with("Program")) {
            program = line.substr(9);
        }
    }

    // registers[A] = 114615199003400;
    // run(program);
    // cout << "program: " << program << endl;
    // cout << "output: " << join(output) << endl;

    cout << "A: " << backtrack(0, program.size() - 1, program) << endl;

    return 0;
}
