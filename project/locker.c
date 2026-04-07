#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {

    if(argc < 4) {
        printf("Usage: locker <encrypt/decrypt> <file> <key>\n");
        return 1;
    }

    char *mode = argv[1];
    char *filename = argv[2];
    char key = argv[3][0];

    FILE *fp = fopen(filename, "rb");
    if(fp == NULL) {
        printf("File not found!\n");
        return 1;
    }

    char outputFile[300];

    if(strcmp(mode, "encrypt") == 0) {
        sprintf(outputFile, "%s.enc", filename);
    } else {
        int len = strlen(filename);
        if(len > 4 && strcmp(filename + len - 4, ".enc") == 0) {
            strncpy(outputFile, filename, len - 4);
            outputFile[len - 4] = '\0';
        } else {
            sprintf(outputFile, "%s.dec", filename);
        }
    }

    FILE *out = fopen(outputFile, "wb");

    int ch;
    while((ch = fgetc(fp)) != EOF) {
        fputc(ch ^ key, out);
    }

    fclose(fp);
    fclose(out);

    printf("Output: %s\n", outputFile);
    return 0;
}