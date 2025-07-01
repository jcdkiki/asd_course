from asd_course.base_module import BaseTask, TestCase
import argparse

TASK_DESCRIPTION = """
Написать программу, принимающую на вход строку, состоящую из символов латинского алфавита нижнего регистра 
и выдающую ответ в виде строки с символами, каждый из которых на 1 больше исходного по модулю 26 + 97 (латинские буквы нижнего регистра в ASCII).

Примеры:

1.  Входная строка:  abc
    Выходная строка: bcd

2.  Входная строка:  gdkknvnqkc
    Выходная строка: helloworld
    
Гарантируется, что входная (соответственно и выходная) строка размера не более 10^5 символов
"""

class IntroLab(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shift = kwargs["shift"]

    def solve(self, str) -> str:
        return ''.join([chr(97 + (ord(c) + self.shift - 97) % 26) for c in str])

    def check(self) -> tuple[bool, str]:
        test_strs = [
            "abc",
            "gdkknvnqkc",
            "gnvcxgn",
            "vnvnvnnvnvnvnvnvnvnvnvnvnvnvnvn"
        ]

        tests = [ TestCase(stdin=test, expected=self.solve(test), time_limit=1) for test in test_strs ]
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--shift", default=1, type=int)
