// while True:
//     inp = input()
//     print("asdf" + inp + "NOTHING")

#include <iostream>

int main() {
    std::string inp;
    while (true) {
        std::cin >> inp;
        std::cout << "asdf" << inp << "NOTHING" << std::endl;
    }
    return 0;
}