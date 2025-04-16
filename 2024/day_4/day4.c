#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINES 200
#define MAX_LINE_LENGTH 256

const char *text1[] = {
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX"
};

const char keyPartI[] = "XMAS";
const char keyPartII[] = "MAS";

int GetText(size_t *nrows, size_t *ncolumns, char **text) {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        perror("Error opening input.txt");
        return 1;
    }

    char buffer[MAX_LINE_LENGTH];
    while (fgets(buffer, sizeof(buffer), file)) {
        buffer[strcspn(buffer, "\n")] = '\0';
        text[*nrows] = malloc(strlen(buffer) + 1);
        if (text[*nrows] == NULL) {
            perror("Error allocating string for line");
            fclose(file);
            return 1;
        }

        strcpy(text[*nrows], buffer);

        (*nrows)++;
    }

    *ncolumns = strlen(text[0]);

    fclose(file);

    return 0;
}

int SolvePartI() {
    size_t nrows = 0;
    size_t ncolumns = 0;
    size_t keysize = strlen(keyPartI);
    char *text[MAX_LINES];

    if (GetText(&nrows, &ncolumns, text) == 1) {
        return 1;
    }

    int total = 0;
    for (size_t row = 0; row < nrows; row++) {
        for (size_t col = 0; col <= ncolumns - keysize; col++) {
            if ((text[row][col] == keyPartI[0] && text[row][col + 1] == keyPartI[1] && text[row][col + 2] == keyPartI[2] && text[row][col + 3] == keyPartI[3]) ||
                (text[row][col] == keyPartI[3] && text[row][col + 1] == keyPartI[2] && text[row][col + 2] == keyPartI[1] && text[row][col + 3] == keyPartI[0])) {
                    total++;
            }
        }
    }

    for (size_t row = 0; row <= nrows - keysize; row++) {
        for (size_t col = 0; col < ncolumns; col++) {
            if ((text[row][col] == keyPartI[0] && text[row + 1][col] == keyPartI[1] && text[row + 2][col] == keyPartI[2] && text[row + 3][col] == keyPartI[3]) ||
                (text[row][col] == keyPartI[3] && text[row + 1][col] == keyPartI[2] && text[row + 2][col] == keyPartI[1] && text[row + 3][col] == keyPartI[0])) {
                    total++;
            }
        }
    }

    for (size_t row = 0; row <= nrows - keysize; row++) {
        for (size_t col = 3; col < ncolumns; col++) {
            if ((text[row][col] == keyPartI[0] && text[row + 1][col - 1] == keyPartI[1] && text[row + 2][col - 2] == keyPartI[2] && text[row + 3][col - 3] == keyPartI[3]) ||
                (text[row][col] == keyPartI[3] && text[row + 1][col - 1] == keyPartI[2] && text[row + 2][col - 2] == keyPartI[1] && text[row + 3][col - 3] == keyPartI[0])) {
                    total++;
            }
        }

        for (size_t col = 0; col <= ncolumns - keysize; col++) {
            if ((text[row][col] == keyPartI[0] && text[row + 1][col + 1] == keyPartI[1] && text[row + 2][col + 2] == keyPartI[2] && text[row + 3][col + 3] == keyPartI[3]) ||
                (text[row][col] == keyPartI[3] && text[row + 1][col + 1] == keyPartI[2] && text[row + 2][col + 2] == keyPartI[1] && text[row + 3][col + 3] == keyPartI[0])) {
                    total++;
            }
        }
    }

    for (size_t i = 0; i < nrows; i++) {
        free(text[i]);
    }

    return total;
}

int SolvePartII() {
    size_t nrows = 0;
    size_t ncolumns = 0;
    char *text[MAX_LINES];

    if (GetText(&nrows, &ncolumns, text) == 1) {
        return 1;
    }

    int total = 0;
    for (size_t row = 1; row < nrows - 1; row++) {
        for (size_t col = 1; col < ncolumns - 1; col++) {
            if (text[row][col] == keyPartII[1]) {
                if (((text[row - 1][col - 1] == keyPartII[0] && text[row + 1][col + 1] == keyPartII[2]) ||
                     (text[row - 1][col - 1] == keyPartII[2] && text[row + 1][col + 1] == keyPartII[0])) &&
                    ((text[row - 1][col + 1] == keyPartII[0] && text[row + 1][col - 1] == keyPartII[2]) ||
                     (text[row - 1][col + 1] == keyPartII[2] && text[row + 1][col - 1] == keyPartII[0]))) {
                    total++;
                }
            }
        }
    }

    for (size_t i = 0; i < nrows; i++) {
        free(text[i]);
    }
    
    return total;
}

int main(void) {

    printf("PartI: %d\n", SolvePartI());
    printf("PartII: %d\n", SolvePartII());
    return 0;
}