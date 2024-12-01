#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>

void sieve_of_eratosthenes(int limit) {
    std::vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;

    for (int p = 2; p * p <= limit; ++p) {
        if (is_prime[p]) {
            for (int i = p * p; i <= limit; i += p) {
                is_prime[i] = false;
            }
        }
    }
}

int main() {
    std::ofstream csv_file("prime.csv");
    if (!csv_file.is_open()) {
        std::cerr << "Error: Unable to open file prime.csv for writing.\n";
        return 1;
    }

    csv_file << "limit,execution_time\n";

    for (int limit = 1000000; limit <= 50000000; limit += 1000000) {
        clock_t start_time = clock();
        sieve_of_eratosthenes(limit);
        clock_t end_time = clock();
        double execution_time = 1000.0 * (end_time - start_time) / CLOCKS_PER_SEC;
        csv_file << limit << "," << execution_time << "\n";
    }

    csv_file.close();
    return 0;
}