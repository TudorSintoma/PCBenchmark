#include <iostream>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <vector>
#include <string>

using namespace std;

void generateInputFile(const string &fileName, int sizeMB) {
    ifstream fileCheck(fileName, ios::binary);
    if (fileCheck) {
        cout << fileName << " already exists, skipping generation." << endl;
        return;
    }
    fileCheck.close();

    ofstream outFile(fileName, ios::binary);
    if (!outFile) {
        cerr << "Error creating file: " << fileName << endl;
        return;
    }

    cout << "Generating " << fileName << " with size " << sizeMB << " MB..." << endl;

    const int bytesPerMB = 1024 * 1024;
    vector<char> buffer(bytesPerMB, 0);

    srand(static_cast<unsigned>(time(0)));
    for (int i = 0; i < bytesPerMB; ++i) {
        buffer[i] = static_cast<char>(rand() % 256);
    }

    for (int i = 0; i < sizeMB; ++i) {
        outFile.write(buffer.data(), bytesPerMB);
    }

    outFile.close();
}

void notEncrypt(ifstream &inFile, ofstream &outFile) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(~ch);
    }
}

void andEncrypt(ifstream &inFile, ofstream &outFile, char key) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch & key);
    }
}

void orEncrypt(ifstream &inFile, ofstream &outFile, char key) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch | key);
    }
}

void xorEncrypt(ifstream &inFile, ofstream &outFile, char key) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch ^ key);
    }
}

double measureEncryptionTime(const string& inputFile, const string& outputFile, void(*encryptionFunc)(ifstream&, ofstream&, char), char key) {
    ifstream inFile(inputFile, ios::binary);
    ofstream outFile(outputFile, ios::binary);

    if (!inFile || !outFile) {
        cerr << "Error opening file!" << endl;
        return -1;
    }

    clock_t start = clock();
    encryptionFunc(inFile, outFile, key);
    clock_t end = clock();
    double elapsedTime = double(end - start) / CLOCKS_PER_SEC;

    inFile.close();
    outFile.close();

    return elapsedTime;
}

int main() {
    int fileSizes[] = { 10, 15, 20, 25, 30, 35, 40, 45, 50 };
    char key = 0xAA; //encryption key

    ofstream resultFile("logic.csv");
    resultFile << "file_size,time_not,time_and,time_or,time_xor" << endl;
    resultFile << fixed << setprecision(3);

    for (int size : fileSizes) {
        string inputFile = to_string(size) + "MB_input.txt";
        string outputFile = "output.txt";

        generateInputFile(inputFile, size);

        double time_not = measureEncryptionTime(inputFile, outputFile, [](ifstream &in, ofstream &out, char) { notEncrypt(in, out); }, key);
        double time_and = measureEncryptionTime(inputFile, outputFile, andEncrypt, key);
        double time_or = measureEncryptionTime(inputFile, outputFile, orEncrypt, key);
        double time_xor = measureEncryptionTime(inputFile, outputFile, xorEncrypt, key);

        resultFile << size << ',' << time_not << ',' << time_and << ',' << time_or << ',' << time_xor << endl;
        cout << "Results for " << size << "MB file: NOT=" << fixed << setprecision(3) << time_not 
             << "s, AND=" << time_and << "s, OR=" << time_or << "s, XOR=" << time_xor << "s" << endl;
    }

    resultFile.close();
    cout << "Results saved to logic.csv" << endl;

    return 0;
}
