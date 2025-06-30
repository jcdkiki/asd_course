#!/bin/bash

docker run --rm -it moevm/asd_course \
--mode check \
--language python3 \
--solution "s = input()
ans = ""
for i in input:
    ans += chr(97 + (int(i) + 1) % 26)
print(ans)" \
IntroLab \
--string abc