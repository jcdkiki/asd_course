#!/bin/bash
# we mount <full_path>/solution.py to app/src/solution.py
docker run --rm -it -v ./src/asd_course/lab0_intro/solution.py:/app/src/solution.py:ro moevm/asd_course \
--mode check \
--language python3 \
IntroLab \
--string bcd