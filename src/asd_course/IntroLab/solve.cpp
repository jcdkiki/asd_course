#include <iostream>
#include <vector>

int main() {
    std::string s;
    std::cin >> s;
    for (int i = 0; i < (int)s.size(); ++i) {
        s[i] = 97 + (s[i] - 97 + 1) % 26;
    }
    std::cout << s;
    return 0;
}
