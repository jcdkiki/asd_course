import argparse

class BaseTask:
    NAME = "base_task"
    def __init__(self):
        pass

    def check(self):
        raise NotImplementedError
    
    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        pass
