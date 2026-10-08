#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <ctime>
#include <sstream>

class Logger {
public:
    explicit Logger(const std::string& filename) {
        m_file.open(filename, std::ios::out | std::ios::app);
    }

    ~Logger() {
        m_file.close();
    }

    template <typename... Args>
    void log(const char* level, Args... args) {
        auto now = std::time(nullptr);
        auto tm = *std::localtime(&now);

        std::ostringstream oss;
        oss << "[" << std::put_time(&tm, "%Y-%m-%d %H:%M:%S") << "] [" << level << "] ";
        format(oss, args...);
        oss << "\n";

        m_file << oss.str();
    }

private:
    std::ofstream m_file;

    template <typename T>
    void format(std::ostringstream& oss, T value) {
        oss << value;
    }

    template <typename T, typename... Args>
    void format(std::ostringstream& oss, T value, Args... args) {
        format(oss, value);
        format(oss, args...);
    }
};

int main() {
    Logger log("test.log");

    log.log("INFO", "This is a test log message.");
    log.log("WARNING", "The value of pi is approximately ", 3.14159);
    log.log("ERROR", "Failed to open file: ", "test.txt");

    return 0;
}