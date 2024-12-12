#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stack>
#include <string>
#include <vector>

using namespace std;

using grid_t = vector<string>;
using point_t = uint64_t;
using mem_t = set<pair<point_t, point_t>>;
using mem2_t = set<vector<point_t>>;

point_t setxy(int x, int y) { return (point_t)x << 32 | y; }
int getx(point_t p) { return p >> 32; }
int gety(point_t p) { return p & 0xFFFFFFFF; }

grid_t read_input(const string &filename) {
  grid_t grid;

  ifstream file(filename);
  string line;
  while (getline(file, line)) {
    grid.push_back(line);
  }

  file.close();

  return grid;
}

stack<point_t> get_trailheads(const grid_t &grid) {
  stack<point_t> trailheads;
  for (int i = 0; i < grid.size(); ++i) {
    for (int j = 0; j < grid[i].size(); ++j) {
      if (grid[i][j] == '0') {
        trailheads.push(setxy(i, j));
      }
    }
  }

  return trailheads;
}

int count_trails(const grid_t &grid, stack<point_t> &trailheads) {
  mem_t mem;
  int result = 0;

  point_t start = -1;
  while (!trailheads.empty()) {
    auto p = trailheads.top();
    trailheads.pop();

    int x = getx(p);
    int y = gety(p);

    if (grid[x][y] == '0') {
      start = p;
    }

    int height = grid[x][y] - '0';

    if (height == 9) {
      if (!mem.contains(pair(start, p))) {
        result++;
        mem.insert(pair(start, p));
      }
    }

    if (x > 0 && grid[x - 1][y] == height + 1 + '0')
      trailheads.push(setxy(x - 1, y));
    if (x < grid.size() - 1 && grid[x + 1][y] == height + 1 + '0')
      trailheads.push(setxy(x + 1, y));
    if (y > 0 && grid[x][y - 1] == height + 1 + '0')
      trailheads.push(setxy(x, y - 1));
    if (y < grid[x].size() - 1 && grid[x][y + 1] == height + 1 + '0')
      trailheads.push(setxy(x, y + 1));
  }

  return result;
}

int count_ratings(const grid_t &grid, stack<point_t> &trailheads) {
  int result = 0;
  mem2_t mem;
  vector<point_t> trail;

  point_t start = -1;
  while (!trailheads.empty()) {
    auto p = trailheads.top();
    trailheads.pop();

    trail.push_back(p);

    int x = getx(p);
    int y = gety(p);

    int height = grid[x][y] - '0';

    if (height == 9) {
      if (!mem.contains(trail)) {
        result++;
        mem.insert(trail);
      }
    }

    if (x > 0 && grid[x - 1][y] == height + 1 + '0')
      trailheads.push(setxy(x - 1, y));
    if (x < grid.size() - 1 && grid[x + 1][y] == height + 1 + '0')
      trailheads.push(setxy(x + 1, y));
    if (y > 0 && grid[x][y - 1] == height + 1 + '0')
      trailheads.push(setxy(x, y - 1));
    if (y < grid[x].size() - 1 && grid[x][y + 1] == height + 1 + '0')
      trailheads.push(setxy(x, y + 1));
  }

  return result;
}

void run_testcases(const char *filename, int expected) {
  auto grid = read_input(filename);
  auto trailheads = get_trailheads(grid);
  mem_t mem;

  int result = count_trails(grid, trailheads);
  if (result == expected) {
    cout << filename << " passed" << endl;
  } else {
    cout << filename << " failed - expected: " << expected
         << ", got: " << result << endl;
  }
}

void run_testcases2(const char *filename, int expected) {
  auto grid = read_input(filename);
  auto trailheads = get_trailheads(grid);
  mem_t mem;

  int result = count_ratings(grid, trailheads);
  if (expected > -1 && result == expected) {
    cout << filename << " passed" << endl;
  } else {
    cout << filename << " failed - expected: " << expected
         << ", got: " << result << endl;
  }
}

void part_i() {
  run_testcases("example1.txt", 1);
  run_testcases("example2.txt", 2);
  run_testcases("example3.txt", 4);
  run_testcases("example4.txt", 3);
  run_testcases("example5.txt", 36);
  run_testcases("input.txt", 659);
}

void part_ii() {
  run_testcases2("example6.txt", 3);
  run_testcases2("example3.txt", 13);
  run_testcases2("example7.txt", 227);
  run_testcases2("example5.txt", 81);
  run_testcases2("input.txt", 1463);
}

int main() {
  part_i();
  part_ii();

  return 0;
}
