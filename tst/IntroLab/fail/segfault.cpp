#include <iostream>
#include <vector>

int main() {
    std::string s;
    std::cin >> s;
    s.resize(0);
    for (int i = 0; i < 1000; ++i) {
        s[i] = 97 + (s[i] - 97 + 1) % 26;
    }
    std::cout << s;
    return 0;
}
