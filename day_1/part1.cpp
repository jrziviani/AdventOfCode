#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <cstdint>

using namespace std;

using v64 = vector<uint64_t>;

v64 GetDistanceOfPairs(v64 &a, v64 &b) {
    if (a.size() != b.size()) {
        cerr << "The size of two vectors are not equal." << endl;
        return {};
    }

    sort(a.begin(), a.end());
    sort(b.begin(), b.end());

    v64 result;
    for (int i = 0; i < a.size(); i++) {
        result.push_back(llabs(a[i] - b[i]));
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

    // vector<int> a = {3, 4, 2, 1, 3, 3};
    // vector<int> b = {4, 3, 5, 3, 9, 3};

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

    auto result = GetDistanceOfPairs(a, b);
    auto total = sum(result);
    cout << total << endl;

    return 0;
}