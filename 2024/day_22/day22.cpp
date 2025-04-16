#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <unordered_map>
#include <string>

using namespace std;

uint64_t new_secret(uint64_t secret) {
    auto mix = [](uint64_t value, uint64_t secret) {
        return secret ^ value;
    };

    auto prune = [](uint64_t secret) {
        return secret & (16777216 - 1);
    };

    secret = prune(mix(secret << 6, secret));
    secret = prune(mix(secret >> 5, secret));
    secret = prune(mix(secret << 11, secret));
    return secret;
}

uint64_t find_next_n_secret(uint64_t secret, int n) {
    for (int i = 0; i < n; i++) {
        secret = new_secret(secret);
    }

    return secret;
}

void get_changes(uint64_t secret, int n, unordered_map<string, int>& results) {
    int last_change =  static_cast<int>(secret % 10);
    unordered_map<string, int> subresult;

    int key[4] = {0};
    for (int i = 0; i < n; i++) {
        secret = new_secret(secret);
        int change = static_cast<int>(secret % 10);

        key[i % 4] = change - last_change;
        last_change = change;
        if (i < 3) {
            continue;
        }
        string tblkey = to_string(key[(i + 1) % 4]) + "," +
                        to_string(key[(i + 2) % 4]) + "," +
                        to_string(key[(i + 3) % 4]) + "," +
                        to_string(key[i % 4]);

        bool has_key = subresult.find(tblkey) != subresult.end();
        if (!has_key) {
            subresult[tblkey] = change;
        }
    }

    for (auto [key, value] : subresult) {
        results[key] += value;
    }
}

vector<uint64_t> parse() {
    vector<uint64_t> result;
    auto file = ifstream("input.txt");
    string line;
    while (getline(file, line)) {
        result.push_back(stoull(line));
    }
    file.close();

    return result;
}

int main() {
    auto input = parse();
    uint64_t total = 0;
    for (auto i : input) {
       auto s = find_next_n_secret(i, 2000);
       total += s;
    }

    cout << "Part I: " << total << endl;

    unordered_map<string, int> results;
    int64_t best_score = 0;
    for (auto i : input) {
        get_changes(i, 2000, results);
    }

    for (auto [key, value] : results) {
        if (value > best_score) {
            best_score = value;
        }
    }

    cout << "Part II: " << best_score << endl;

    return 0;
}