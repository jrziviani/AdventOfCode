#include <iostream>
#include <vector>
#include <string>
#include <fstream>

using namespace std;

struct aocfile {
    int id;
    int size;
    string repr;

    aocfile(int id, int size, string repr) : id(id), size(size), repr(repr) {}

    string getrepr() const {
        return repr;
    }

    string getid() const {
        if (id == -1) {
            return ".";
        }
        else {
            return to_string(id);
        }
    }
};

using files = vector<aocfile>;

files expand(const string &input) {
    files output;

    int k = 0;
    for (int i = 0; i < input.size(); ++i) {
        int ntimes = input[i] - '0';
        if (i & 1 == 1) {
            for (int j = 0; j < ntimes; ++j) 
                output.push_back(aocfile(-1, ntimes - j, "."));
        }
        else {
            for (int j = 0; j < ntimes; ++j) 
                output.push_back(aocfile(k, ntimes, "x"));
            k++;
        }
    }

    return output;
}

void print(const files &f) {
    for (int i = 0; i < f.size(); ++i) {
        cout << f[i].repr;
    }
    cout << endl;
}

void compact(files &input) {
    auto is_free_space = [&input](int i) { return i >= 0 && i < input.size() && input[i].id == -1; };
    auto has_free_capacity = [&input](int i, int j) { return i >= 0 &&
                                                             i < input.size() &&
                                                             j >= 0 &&
                                                             j < input.size() &&
                                                             input[i].id == -1 &&
                                                             input[j].id != -1 &&
                                                             input[j].size <= input[i].size; };
    int k = input.size() - 1;
    int i = 0;
    for (int i = 0; i < input.size(); ++i) {
        print(input);
        if (!is_free_space(i)) {
            continue;
        }

        int lastk = k;
        for (int j = 0; j < k; j++) {
            if (is_free_space(j) && has_free_capacity(j, k) && k >= j) {
                auto id = input[k].id;
                while (k >= 0 && input[k].id == id) {
                    input[j].id = input[k].id;
                    input[j].repr = input[k].repr;
                    input[k].id = -1;
                    input[k].repr = ".";
                    k--;
                    j++;
                }
                break;
            }
        }

        if (k < 0) {
            break;
        }

        if (lastk == k) {
            auto id = input[k].id;
            while (k >= 0 && input[k].id == id) {
                k--;
            }
        }
    }
    // print(input);

    long long int sum = 0;
    for (i = 0; i < input.size(); ++i) {
        if (input[i].id == -1) {
            continue;
        }
        sum += input[i].id * i;
    }

     cout << sum << endl;
}

long long int checksum(files &input) {
    long long int sum = 0;
    int left = 0;
    int right = input.size() - 1;
    long long int k = 0;
    while (left <= right) {
        if (input[left].id == -1 && input[right].id == -1) {
            right--;
        }
        else if (input[left].id == -1 && input[right].id != -1) {
            sum += input[right].id * k;
            left++;
            k++;
            right--;
        }
        else if (input[left].id != -1) {
            sum += input[left].id * k;
            left++;
            k++;
        }
    }

    return sum;
}

int main() {
    ifstream file("example.txt");
    string line;
    getline(file, line);
    file.close();

    files expanded = expand(line);
    //print(expanded);

    cout << checksum(expanded) << endl;

    compact(expanded);
    // print(expanded);
    
    return 0;
}