#include <iostream>
#include <vector>
#include <tuple>
#include <unordered_map>
#include <string>
#include <fstream>

using namespace std;

enum direction : int {
    UP,
    RIGHT,
    DOWN,
    LEFT
};

using board_t = vector<vector<char>>;
using coord_t = tuple<int, int, int>;

struct coord_hash {
    size_t operator()(const coord_t &coord) const {
        const auto &[x, y, dir] = coord;

        size_t h1 = std::hash<int>()(x);
        size_t h2 = std::hash<int>()(y);
        size_t h3 = std::hash<int>()(dir);

        return h1 ^ (h2 << 1) ^ (h3 << 2);
    }
};

using visited_t = unordered_map<coord_t, bool, coord_hash>;

bool dfs(board_t &board, int x, int y, direction dir, visited_t &visited) {
    if (visited.count({ x, y, static_cast<int>(dir) }) > 0) {
        return true;
    }

    if (x < 0 || x >= board.size() || y < 0 || y >= board[0].size()) {
        return false;
    }

    if (board[x][y] == '#') {
        //                       UP, RIGHT, DOWN, LEFT
        static const int dx[] = { 0,     1,    0,   -1};
        static const int dy[] = { 1,     0,   -1,    0};
        int new_dir = (dir + 1) % 4;

        visited[{ x, y, static_cast<int>(dir) }] = true;
        return dfs(board, x + dx[new_dir], y + dy[new_dir], static_cast<direction>(new_dir), visited);
    }
    else {
        //                       UP, RIGHT, DOWN, LEFT
        static const int dx[] = { -1,     0,    1,     0};
        static const int dy[] = {  0,     1,    0,    -1};
        // board[x][y] = 'X';
        return dfs(board, x + dx[dir], y + dy[dir], dir, visited);
    }
}

int main() {
    std::ifstream file("input.txt");

    board_t board;
    string line;
    while (getline(file, line)) {
        vector<char> row(line.begin(), line.end());
        board.push_back(row);
    }
    file.close();

    int x = -1;
    int y = -1;
    for (int i = 0; i < board.size(); i++) {
        for (int j = 0; j < board[i].size(); j++) {
            if (board[i][j] == '^') {
                x = i;
                y = j;
                break;
            }
        }

        if (x != -1) {
            break;
        }
    }

    /* PART I
    visited_t visited;
    int count = 0;
    dfs(board, x, y, direction::UP, visited);
    for (auto kv : board) {
        for (auto c : kv) {
            if (c == 'X') {
                count++;
            }
            // cout << c;
        }
        // cout << endl;
    }
    cout << "Count: " << count << endl;
    */

    /* PART II */
    int num_lines = board.size();
    int max_obstacles = 0;
    for (int i = 0; i < board.size(); i++) {
        for (int j = 0; j < board[i].size(); j++) {
            if (board[i][j] == '.') {
                board[i][j] = '#';

                visited_t visited;
                if (dfs(board, x, y, direction::UP, visited)) {
                    max_obstacles++;
                }

                board[i][j] = '.';
            }
        }

        cout << "Progress: " << (i + 1) << "/" << num_lines << endl;
    }

    cout << "Max obstacles: " << max_obstacles << endl;

    return 0;
}