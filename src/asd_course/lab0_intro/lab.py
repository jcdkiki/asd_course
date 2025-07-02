from asd_course.base_module import BaseTask, TestCase
import argparse

class IntroLab(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check(self) -> tuple[bool, str]:
        
        test_strs = [
            "abc",
            "gdkknvnqkc",
            "gnvcxgn",
            "vnvnvnnvnvnvnvnvnvnvnvnvnvnvnvn"
        ]

        tests = [ TestCase(stdin=test, expected=self.solve(test)[0], time_limit=self.solve(test)[1]) for test in test_strs ]
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--shift", default=1, type=int)
