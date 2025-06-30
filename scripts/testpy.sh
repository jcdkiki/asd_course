#!/bin/bash

docker run --rm -it moevm/asd_course \
--mode check \
--language python3 \
--solution "s = input()
ans = ''
for i in s:
    ans += chr(97 + (ord(i) + 1 - 97) % 26)
print(ans)" \
IntroLab \
--string bcd