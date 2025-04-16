#include <fstream>
#include <iostream>
#include <vector>
#include <tuple>
#include <string>
#include <unordered_map>

using namespace std;

using mem_t = unordered_map<string, long int>;

vector<string> get_input(string filename) {
    ifstream file(filename);
    vector<string> lines;
    string line;
    while (getline(file, line)) {
        line += " ";
        for (int i = 0; i < line.size(); i++) {
            if (line[i] == ' ') {
                lines.push_back(line.substr(0, i));
                line = line.substr(i + 1);
                i = 0;
            }
        }
    }

    return lines;
}

string rule1(const string &input) {
    if (input == "0") {
        return "1";
    }
    return input;
}

string rule2(const string &input) {
    auto remove_zeroes = [](const string &input) -> string {
        return to_string(stol(input));
    };

    if (input.size() % 2 == 0) {
        string left_half = input.substr(0, input.size() / 2);
        string right_half = input.substr(input.size() / 2);
        return left_half + " " + remove_zeroes(right_half);
    }
    return input;
}

string rule3(const string &input) {
    return to_string(stol(input) * 2024L);
}

tuple<string, int> apply_rules(const string &input) {
    string output = rule1(input);
    int rule_applied = 1;
    if (output == input) {
        output = rule2(output);
        rule_applied = 2;
        if (output == input) {
            output = rule3(output);
            rule_applied = 3;
        }
    }

    return {output, rule_applied};
}

long int blinkII(const string &stone, int blink, mem_t &mem) {
    long int result = 0;

    string key = stone + "-" + to_string(blink);
    if (mem.contains(key)) {
        return mem[key];
    }

    if (blink == 0) {
        return 1;
    }

    auto [output, rule_applied] = apply_rules(stone);
    if (rule_applied == 2) {
        string part = output.substr(0, output.find(" "));
        result = blinkII(part, blink - 1, mem);

        part = output.substr(output.find(" ") + 1);
        result += blinkII(part, blink - 1, mem);
    }
    else {
        result = blinkII(output, blink - 1, mem);
    }

    mem[key] = result;
    return mem[key];
}

int blink(int times, vector<string> &stones) {
    auto inner = [](const vector<string> &stones) -> vector<string> {
        vector<string> result;
        for (auto stone : stones) {
            auto [output, rule_applied] = apply_rules(stone);

            if (rule_applied == 2) {
                string part1 = output.substr(0, output.find(" "));
                string part2 = output.substr(output.find(" ") + 1);
                result.push_back(part1);
                result.push_back(part2);
            }
            else {
                result.push_back(output);
            }
        }
        return result;
    };

    for (int i = 0; i < times; i++) {
        stones = move(inner(stones));
    }

    return stones.size();
}

int main() {
    vector<string> stones = get_input("input.txt");
    mem_t mem;

    long int counter = 0;
    for (auto stone : stones) {
        counter += blinkII(stone, 75, mem);
    }
    cout << counter << endl;

    return 0;
}