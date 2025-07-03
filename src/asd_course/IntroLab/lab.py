from asd_course.base_module import BaseTask, TestCase
import argparse
import os

class IntroLab(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.solve_dir = os.path.dirname(os.path.realpath(__file__))
        self.cpp_complile_args = f"-DSHIFT={self.shift}"
        self.py_compile_args   = f"--shift {self.shift}"

    def check(self) -> tuple[bool, str]:
        tests = [
            "abc",
            "gdkknvnqkc",
            "gnvcxgn",
            "vnvnvnnvnvnvnvnvnvnvnvnvnvnvnvn"
        ]
        return self.run_tests(tests)
        
    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--shift", default=1, type=int)
