from asd_course.base_module import BaseTask, TestCase
import argparse

class IntroLab(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.string = kwargs["string"]

    def check(self) -> tuple[bool, str]:
        tests = [
            TestCase(stdin = "abc", expected = self.string, time_limit = 1)
        ]
        
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--string", default="Hello, World!")
