#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <cstdint>
#include <string>
#include <unordered_map>

using namespace std;

using v64 = vector<uint64_t>;

v64 GetSimilarity(const v64 &a, const v64 &b) {
    if (a.size() != b.size()) {
        cerr << "The size of two vectors are not equal." << endl;
        return {};
    }

    unordered_map<uint64_t, uint32_t> b_map;
    for (auto &i : b) {
        b_map[i]++;
    }

    v64 result;
    for (int i = 0; i < a.size(); i++) {
        if (b_map.find(a[i]) == b_map.end()) {
            result.push_back(0);
        } else {
            result.push_back(a[i] * b_map[a[i]]);
        }
    }

    return result;
}

int64_t sum(const v64 &a) {
    int64_t sum = 0;
    for (auto &i : a) {
        sum += i;
    }
    return sum;
}

int main(int argc, char *argv[]) {

/*
    v64 a = {3, 4, 2, 1, 3, 3};
    v64 b = {4, 3, 5, 3, 9, 3};
*/

    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <input file>" << endl;
        return 1;
    }

    ifstream file(argv[1]);
    if (!file.is_open()) {
        cerr << "Cannot open file: " << argv[1] << endl;
        return 1;
    }

    v64 a, b;
    int64_t x, y;
    while (file >> x >> y) {
        a.push_back(x);
        b.push_back(y);
    }
    file.close();

    auto result = GetSimilarity(a, b);
    auto total = sum(result);
    cout << total << endl;

    return 0;
}