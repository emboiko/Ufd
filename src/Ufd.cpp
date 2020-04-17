#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main(int argc, char *argv[]) {
	system("C:/Programming/Python/Projects/Ufd/dist/Ufd/ufd.exe stdout=True > paths.txt");
	std::ifstream inFile("paths.txt");

	std::vector<std::string> results;
	std::string result;

	while (getline(inFile, result)) results.push_back(result);
	inFile.close();
	std::remove("paths.txt");

	for (std::string path : results) std::cout << path << "\n";

	std::cin.ignore();
	return 0;
}