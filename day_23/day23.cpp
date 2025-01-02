#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <stack>
#include <algorithm>
#include <vector>
#include <array>

using namespace std;

using adj_t = unordered_set<string>;
using graph_t = unordered_map<string, adj_t>;

graph_t parse() {
    graph_t result;
    auto file = ifstream("input.txt");
    string line;
    while (getline(file, line)) {
        auto from = line.substr(0, 2);
        auto to = line.substr(3, 2);
        result[from].insert(to);
        result[to].insert(from);
    }
    file.close();

    return result;
}

bool is_included(const adj_t &a, const unordered_set<string> &b) {
    for (auto s : b) {
        if (!a.contains(s)) {
            return false;
        }
    }
    return true;
}

void dfs(const graph_t &g, const string &computer, adj_t &visited, unordered_set<string> &group, unordered_set<string> &res) {

    if (visited.contains(computer)) {
        return;
    }

    if (group.size() == 2 && is_included(g.at(computer), group)) {
        string tmp[3] = {computer};
        int i = 1;
        for (auto s : group) {
            tmp[i++] = s;
        }
        sort(tmp, tmp + 3);
        string combined = tmp[0] + "," + tmp[1] + "," + tmp[2];
        res.insert(combined);
        return;
    }
    else if (group.size() > 2) {
        return;
    }

    visited.insert(computer);
    group.insert(computer);
    for (auto &neighbor : g.at(computer)) {
        dfs(g, neighbor, visited, group, res);
    }
    group.erase(computer);
}

void dfs_partII(const graph_t &g, const string &computer, adj_t &visited, unordered_set<string> &group, vector<string> &res) {

    if (visited.contains(computer)) {
        return;
    }

    if (group.size() > res.size()) {
        res.clear();
        for (auto g : group) {
            res.push_back(g);
        }
    }
    visited.insert(computer);

    for (auto &neighbor : g.at(computer)) {
        if (!is_included(g.at(neighbor), group)) {
            continue;
        }

        group.insert(neighbor);
        dfs_partII(g, neighbor, visited, group, res);
    }
}

string join_vector(const vector<string> &v) {
    string result;
    for (int i = 0; i < v.size(); i++) {
        result += v[i];
        if (i != v.size() - 1) {
            result += ",";
        }
    }
    return result;
}

int main() {
    auto graph = parse();
    adj_t res;
    for (auto [key, value] : graph) {
        adj_t group = {key};
        adj_t visited;
        dfs(graph, key, visited, group, res);
    }

    int count = 0;
    for (auto s : res) {
        if (s.starts_with("t") || s.find(",t") != string::npos) {
            count++;
        }
    }
    cout << "Part I: " << count << endl;

    vector<string> resII;
    for (auto [key, value] : graph) {
        adj_t group = {key};
        adj_t visited;
        dfs_partII(graph, key, visited, group, resII);
    }

    sort(resII.begin(), resII.end());
    cout << "Part II: " << join_vector(resII) << endl;
    return 0;
}