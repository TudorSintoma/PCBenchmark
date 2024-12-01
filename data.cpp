#include <iostream>
#include <fstream>
#include <ctime>
#include <vector>
#include <tuple>

void writeFile(const std::string &filename, size_t file_size) {
    std::ofstream outfile(filename, std::ios::binary);
    char data[1024];
    for (size_t i = 0; i < file_size / sizeof(data); i++) {
        outfile.write(data, sizeof(data));
    }
    outfile.close();
}

void readFile(const std::string &filename, size_t file_size) {
    std::ifstream infile(filename, std::ios::binary);
    char data[1024];
    while (infile.read(data, sizeof(data))) {}
    infile.close();
}

double measureWriteSpeed(const std::string &filename, size_t file_size) {
    clock_t start_time = clock();
    writeFile(filename, file_size);
    clock_t end_time = clock();
    double time_taken = double(end_time - start_time) / CLOCKS_PER_SEC;
    return time_taken;
}

double measureReadSpeed(const std::string &filename, size_t file_size) {
    clock_t start_time = clock();
    readFile(filename, file_size);
    clock_t end_time = clock();
    double time_taken = double(end_time - start_time) / CLOCKS_PER_SEC;
    return time_taken;
}

void writeResultsToCSV(const std::string &csv_filename, const std::vector<std::tuple<size_t, double, double>> &results) {
    std::ofstream outfile(csv_filename);
    outfile << "file_size,read_speed,write_speed\n";

    for (const auto &result : results) {
        size_t file_size;
        double read_speed, write_speed;
        std::tie(file_size, read_speed, write_speed) = result;
        outfile << file_size << "," << read_speed << "," << write_speed << "\n";
    }

    outfile.close();
}

int main() {
    std::string filename = "test_file.txt";
    std::string csv_filename = "data.csv";

    std::ofstream outfile(filename, std::ios::trunc);

    std::vector<size_t> file_sizes;
    for (size_t size = 10 * 1024 * 1024; size <= 250 * 1024 * 1024; size += 10 * 1024 * 1024) {
        file_sizes.push_back(size);
    }

    std::vector<std::tuple<size_t, double, double>> results;

    for (size_t file_size : file_sizes) {

        double write_time = measureWriteSpeed(filename, file_size);
        double write_speed = (file_size / 1024.0 / 1024.0) / write_time;

        double read_time = measureReadSpeed(filename, file_size);
        double read_speed = (file_size / 1024.0 / 1024.0) / read_time;

        results.push_back(std::make_tuple(file_size, read_speed, write_speed));
    }

    writeResultsToCSV(csv_filename, results);

    return 0;
}