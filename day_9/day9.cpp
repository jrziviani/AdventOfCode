#include <iostream>
#include <vector>
#include <string>
#include <fstream>

using namespace std;


using zchar = vector<int>;
using zstring = vector<vector<int>>;

long long int checksum(const zstring &input) {
    long long int sum = 0;
    int k = 0;
    for (int i = 0; i < input.size(); ++i) {
        for (int j = 0; j < input[i].size(); ++j) {
            sum += input[i][j] * k;
            k++;
        }
    }

    return sum;
}

zchar expand(int s, int n) {
    zchar output(n);

    for (int i = 0; i < n; ++i) {
        output[i] = s;
    }

    return output;
}

zstring expand_fs(const string &input) {
    zstring output;

    for (size_t i = 0, j = 0; i < input.size(); ++i) {
        int ntimes = input[i] - '0';

        if (ntimes == 0) {
            continue;
        }
        
        if (i % 2 == 1) {
            output.push_back(expand(-1, ntimes));
        }
        else {
            output.push_back(expand(j, ntimes));
            j++;
        }
    }

    return output;
}

zstring compact(const zstring &input) {
    int left = 0;
    int i = 0;
    int right = input.size() - 1;
    int j = input[right].size() - 1;

    zstring output;

    zchar c;
    while (left <= right) {
        if (left == right && i > j) {
            break;
        }

        if (j < 0) {
            do {
                right--;
                j = input[right].size() - 1;
            } while (j < 0);
        }

        if (input.size() < right && input[right].size() < j && input[right][j] == -1) {
            j--;
        }
        else if (input.size() < left && input[left].size() < i && input[left][i] == -1) {
            c.push_back(input[right][j]);
            j--;
            i++;
        }
        else {
            c.push_back(input[left][i]);
            i++;
        }

        if (i >= input[left].size()) {
            i = 0;
            left++;
            output.push_back(c);
            c.clear();
        }
    }

    if (c.size() > 0) {
        output.push_back(c);
    }

    return output;
}


zstring compact(zstring &input) {
    int left = 0;
    int i = 0;
    int right = input.size() - 1;
    int j = right >= 0 ? input[right].size() - 1 : -1; // Handle empty input.

    zstring output;
    zchar c;

    while (left <= right) {
        if (left == right && i > j) {
            break;
        }

        // Skip empty rows from the right.
        while (right >= 0 && j < 0) {
            right--;
            j = (right >= 0) ? input[right].size() - 1 : -1;
        }

        if (right < 0) { // If we've exhausted all elements on the right.
            break;
        }

        // Copy or move elements from right to left.
        if (i < input[left].size() && j >= 0 && input[right][j] != -1) {
            input[left][i] = input[right][j];
            c.push_back(input[right][j]);
            j--;
            i++;
        } else if (i < input[left].size() && input[left][i] != -1) {
            c.push_back(input[left][i]);
            i++;
        } else {
            j--;
        }

        // Move to the next row from the left if the current row is done.
        if (i >= input[left].size()) {
            i = 0;
            left++;
            if (!c.empty()) {
                output.push_back(c);
                c.clear();
            }
        }
    }

    // Add any remaining characters to the output.
    if (!c.empty()) {
        output.push_back(c);
    }

    return output;
}


int main() {
    ifstream file("example.txt");
    string line;
    getline(file, line);
    file.close();

    auto expanded = expand_fs(line);
    auto compacted = compact(expanded);
    cout << checksum(compacted) << endl;

    
    return 0;
}