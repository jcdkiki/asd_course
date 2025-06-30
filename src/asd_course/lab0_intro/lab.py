from asd_course.base_module import BaseTask, TestCase
import argparse

class IntroLab(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_a = kwargs["test_a"]
        self.test_b = kwargs["test_b"]
        self.test_c = kwargs["test_c"]
        self.test_d = kwargs["test_d"]

    def check(self) -> tuple[bool, str]:
        tests = [
            TestCase(stdin = "abc", expected = self.test_a, time_limit = 1),
            TestCase(stdin = "gdkknvnqkc", expected = self.test_b, time_limit = 1),
            TestCase(stdin = "gnvcxgn", expected = self.test_c, time_limit = 1),
            TestCase(stdin = "vnvnvnnvnvnvnvnvnvnvnvnvnvnvnvn", expected = self.test_d, time_limit = 1)
        ]
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--test_a", default="helloworld")
        parser.add_argument("--test_b", default="helloworld")
        parser.add_argument("--test_c", default="helloworld")
        parser.add_argument("--test_d", default="helloworld")
