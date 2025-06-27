from asd_course.base_module import BaseTask
import argparse

class IntroLab(BaseTask):
    def __init__(self):
        pass

    def check(self):
        return True
    
    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        parser.add_argument("--seed", required=True)
        parser.add_argument("--n-numbers", required=True, default=2)
