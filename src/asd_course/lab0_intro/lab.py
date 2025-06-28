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
        self.string = kwargs["string"]

    def check(self) -> tuple[bool, str]:
        tests = [
            TestCase(stdin = "", expected = self.string, time_limit = 1)
        ]
        
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--string", default="Hello, World!")
