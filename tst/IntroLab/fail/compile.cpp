#include <iostream>
#include <vector>

int main() {
    std::string s;
    cin >> s;
    for (int i = 0; i < (int)s.size(); ++i) {
        s[i] = 97 + (s[i] - 97 + 2) % 26;
    }
    std::cout << s;
    return 0;
}
