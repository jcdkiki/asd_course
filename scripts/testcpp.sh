#!/bin/bash
# we mount <full_path>/solution.cpp to app/src/solution.cpp
docker run --rm -it -v ./src/asd_course/lab0_intro/solution.cpp:/app/src/solution.cpp:ro moevm/asd_course \
--mode check \
--language cpp \
IntroLab \
--string bcd