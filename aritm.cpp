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

void addOperation(ifstream &inFile, ofstream &outFile, char value) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch + value);
    }
}

void subOperation(ifstream &inFile, ofstream &outFile, char value) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch - value);
    }
}

void mulOperation(ifstream &inFile, ofstream &outFile, char value) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(ch * value);
    }
}

void divOperation(ifstream &inFile, ofstream &outFile, char value) {
    char ch;
    while (inFile.get(ch)) {
        outFile.put(value != 0 ? ch / value : ch); // Avoid division by zero
    }
}

double measureArithmeticTime(const string& inputFile, const string& outputFile, void(*arithmeticFunc)(ifstream&, ofstream&, char), char value) {
    ifstream inFile(inputFile, ios::binary);
    ofstream outFile(outputFile, ios::binary);

    if (!inFile || !outFile) {
        cerr << "Error opening file!" << endl;
        return -1;
    }

    clock_t start = clock();
    arithmeticFunc(inFile, outFile, value);
    clock_t end = clock();
    double elapsedTime = double(end - start) / CLOCKS_PER_SEC;

    inFile.close();
    outFile.close();

    return elapsedTime;
}

int main() {
    int fileSizes[] = { 10, 15, 20, 25, 30, 35, 40, 45, 50 };
    char value = 3;

    ofstream resultFile("aritm.csv");
    resultFile << "file_size,time_add,time_sub,time_mul,time_div" << endl;
    resultFile << fixed << setprecision(3);

    for (int size : fileSizes) {
        string inputFile = to_string(size) + "MB_input.txt";
        string outputFile = "output.txt";

        generateInputFile(inputFile, size);

        double time_add = measureArithmeticTime(inputFile, outputFile, addOperation, value);
        double time_sub = measureArithmeticTime(inputFile, outputFile, subOperation, value);
        double time_mul = measureArithmeticTime(inputFile, outputFile, mulOperation, value);
        double time_div = measureArithmeticTime(inputFile, outputFile, divOperation, value);

        resultFile << size << ',' << time_add << ',' << time_sub << ',' << time_mul << ',' << time_div << endl;
        cout << "Results for " << size << "MB file: ADD=" << time_add 
             << "s, SUB=" << time_sub << "s, MUL=" << time_mul << "s, DIV=" << time_div << "s" << endl;
    }

    resultFile.close();
    cout << "Results saved to aritm.csv" << endl;

    return 0;
}
