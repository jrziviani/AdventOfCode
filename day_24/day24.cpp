#include <fstream>
#include <iostream>
#include <unordered_map>
#include <string>
#include <stack>
#include <vector>
#include <unordered_set>


using namespace std;

enum OPERATION {
    AND,
    OR,
    XOR
};

using wires_t = unordered_map<string, int>;
using circuit_t = unordered_map<string, tuple<OPERATION, string, string>>;

tuple<wires_t, circuit_t> parse(vector<int> &x, vector<int> &y) {
    wires_t wires;
    circuit_t circuit;

    auto file = ifstream("input.txt");
    string line;
    bool first_part = true;
    while (getline(file, line)) {
        if (line.empty()) {
            first_part = false;
            continue;
        }

        if (first_part) {
            auto wire_name = line.substr(0, 3);
            auto value = stoi(line.substr(5));
            if (wire_name[0] == 'x') {
                x.push_back(value);
            }
            else {
                y.push_back(value);
            }
            wires[wire_name] = value;
        }
        else {
            int pos = 0;
            auto wireA = line.substr(pos, 3);
            pos += 4;

            auto operation = OR;
            if (line[pos] == 'A') {
                operation = AND;
                pos += 1;
            }
            else if (line[pos] == 'X') {
                operation = XOR;
                pos += 1;
            }
            pos += 3;

            auto wireB = line.substr(pos, 3);
            pos += 7;
            auto wire_name = line.substr(pos, 3);
            circuit[wire_name] = {operation, wireA, wireB};
        }
    }
    file.close();
    return {wires, circuit};
}

void solve(circuit_t& circuit, wires_t& wires) {
    stack<string> st;
    for (auto &[name, operation_tuple] : circuit) {
        st.push(name);
    }

    while (!st.empty()) {
        auto name = st.top();
        st.pop();

        auto &[operation, wireA, wireB] = circuit[name];

        auto has_valueA = wires.find(wireA) != wires.end();
        auto has_valueB = wires.find(wireB) != wires.end();

        if (has_valueA && has_valueB) {
            int valueA = wires[wireA];
            int valueB = wires[wireB];
            int result = 0;
            switch (operation) {
                case AND:
                    result = valueA & valueB;
                    break;
                case OR:
                    result = valueA | valueB;
                    break;
                case XOR:
                    result = valueA ^ valueB;
                    break;
            }
            wires[name] = result;
            continue;
        }

        st.push(name);
        if (!has_valueA) {
            st.push(wireA);
        }

        if (!has_valueB) {
            st.push(wireB);
        }
    }
}

long pow(int exp) {
    long result = 1;
    for (int i = 0; i < exp; i++) {
        result *= 2;
    }
    return result;
}

long fold_left(vector<int>& values) {
    long result = 0;
    for (int i = 0; i < values.size(); i++) {
        result += values[i] * pow(i);
    }
    return result;
}

int main() {
    vector<int> vx, vy;
    auto [wires, circuit] = parse(vx, vy);
    solve(circuit, wires);

    long value = 0;
    for (int i = 0; i < 100; i++) {
        string key = "z" + (i < 10 ? "0" + to_string(i) : to_string(i));
        if (wires.contains(key)) {
            value += wires[key] * pow(i);
        }
    }

    cout << "Part I: " << value << endl;
}