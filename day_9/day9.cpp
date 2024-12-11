#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <unordered_map>

using namespace std;

struct aocfile {
    int id;
    int index;
    int size;
    char repr;
};

using disk_t = vector<aocfile*>;

void print(const disk_t &disk) {
    for (int i = 0; i < disk.size(); ++i) {
        if (disk[i] == nullptr) {
            continue;
        }

        const aocfile *file = disk[i];
        if (file->id == -1) {
            for (int j = 0; j < file->size; ++j) {
                cout << file->repr;
            }
        }
        else {
            for (int j = 0; j < file->size; ++j) {
                cout << file->id;
            }
        }
    }
    cout << endl;
}

long int checksum(const disk_t &disk) {
    long int sum = 0;
    for (int i = 0, k = 0; i < disk.size(); i++) {
        if (disk[i] == nullptr) {
            continue;
        }

        if (disk[i]->id == -1) {
            k += disk[i]->size;
            continue;
        }

        const aocfile *file = disk[i];
        for (int j = 0; j < file->size; ++j) {
            sum += file->id * k;
            k++;
        }
    }

    return sum;
}

void defragblocks(disk_t &disk) {
    int j = disk.size() - 1;
    int i = 0;
    while (i < j) {
        if (disk[i] == nullptr || disk[i]->id != -1) {
            i++;
            continue;
        }
        // print(disk);

        aocfile *free_block = disk[i];
        aocfile *last_file = disk[j];

        while (last_file == nullptr || last_file->id == -1) {
            last_file = disk[--j];
        }

        aocfile *new_free_block = new aocfile{-1, j, 1, '.'};
        aocfile *new_file = new aocfile{last_file->id, i, 1, last_file->repr};
        
        delete last_file;
        disk[j] = new_free_block;

        delete free_block;
        disk[i] = new_file;

        j--;
        i++;
    }
}

void defrag(disk_t &disk) {
    int j = disk.size() - 1;
    for (int i = 0; i < disk.size(); ++i) {
        if (disk[i] == nullptr || disk[i]->id != -1) {
            continue;
        }

        for (int l = 0; l < j; l++) {
            const aocfile *free_block = disk[l];
            if (free_block == nullptr || free_block->id != -1) {
                continue;
            }

            aocfile *last_file = disk[j];
            while (last_file == nullptr || last_file->id == -1) {
                last_file = disk[--j];
            }

            if (last_file->size > free_block->size) {
                continue;
            }

            int rest_size = free_block->size - last_file->size;

            aocfile *new_free_block = new aocfile{-1, j, last_file->size, '.'};
            delete free_block;
            disk[l] = nullptr;

            if (rest_size > 0) {
                aocfile *new_rest_block = new aocfile{-1, l, rest_size, '.'};
                disk[l + last_file->size] = new_rest_block;
            }

            aocfile *new_file = new aocfile{last_file->id, l, last_file->size, last_file->repr};
            delete last_file;
            disk[j] = nullptr;

            disk[new_file->index] = new_file;
            disk[new_free_block->index] = new_free_block;
            break;
        }

        j--;
    }
}

void partII(const string &line) {
    disk_t disk;
    for (int i = 0, j = 0, k = 0; i < line.size(); ++i) {
        int n = line[i] - '0';

        if (i & 1 == 1) {
            disk.push_back(new aocfile{-1, k, n, '.'});
        }
        else {
            disk.push_back(new aocfile{j, k, n, 'x'});
            j++;
        }

        k += n;

        while (n-- > 0) {
            disk.push_back(nullptr);
        }
    }

    defrag(disk);
    cout << "Part II: " << checksum(disk) << endl;
}

void partI(const string &line) {
    disk_t disk;
    for (int i = 0, k = 0; i < line.size(); ++i) {
        int n = line[i] - '0';

        if (i & 1 == 1) {
            for (int j = 0; j < n; ++j) {
                disk.push_back(new aocfile{-1, i, 1, '.'});
            }
        }
        else {
            for (int j = 0; j < n; ++j) {
                disk.push_back(new aocfile{k, i, 1, 'x'});
            }
            k++;
        }
    }

    defragblocks(disk);
    cout << "Part I: " << checksum(disk) << endl;
}

int main() {
    ifstream file("input.txt");
    string line;
    getline(file, line);
    file.close();

    partI(line);
    partII(line);

    return 0;
}