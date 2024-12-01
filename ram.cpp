#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>
#include <tuple>
#include <cstring> 

double measureRAMWriteSpeed(size_t dataSize) {
    std::vector<char> buffer(dataSize); 
    clock_t start = clock();
    memset(buffer.data(), 1, dataSize); 
    clock_t end = clock();
    double timeTaken = double(end - start) / CLOCKS_PER_SEC;
    return (dataSize / 1024.0 / 1024.0) / timeTaken; 
}

double measureRAMReadSpeed(size_t dataSize) {
    std::vector<char> buffer(dataSize, 1); 
    volatile char temp = 0;
    clock_t start = clock();
    for (size_t i = 0; i < dataSize; i += 64) {
        temp += buffer[i];
    }
    clock_t end = clock();
    double timeTaken = double(end - start) / CLOCKS_PER_SEC;
    return (dataSize / 1024.0 / 1024.0) / timeTaken; 
}

void writeResultsToCSV(const std::string &csvFilename, const std::vector<std::tuple<size_t, double, double>> &results) {
    std::ofstream outfile(csvFilename);
    outfile << "file_size,read_speed,write_speed\n";
    for (const auto &result : results) {
        size_t fileSize;
        double readSpeed, writeSpeed;
        std::tie(fileSize, readSpeed, writeSpeed) = result;
        outfile << fileSize << "," << readSpeed << "," << writeSpeed << "\n";
    }
    outfile.close();
}

int main() {
    std::vector<size_t> fileSizes; 
    for (size_t size = 10 * 1024 * 1024; size <= 1000 * 1024 * 1024; size += 10 * 1024 * 1024) {
        fileSizes.push_back(size);
    }

    std::vector<std::tuple<size_t, double, double>> results;

    for (size_t fileSize : fileSizes) {
        double writeSpeed = measureRAMWriteSpeed(fileSize);
        double readSpeed = measureRAMReadSpeed(fileSize);
        results.push_back(std::make_tuple(fileSize, readSpeed, writeSpeed));
    }

    writeResultsToCSV("ram.csv", results);
    return 0;
}
