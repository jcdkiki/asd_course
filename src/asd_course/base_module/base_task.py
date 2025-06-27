import argparse
import dataclasses

@dataclasses.dataclass
class TestCase:
    stdin : str
    expected : str
    time_limit : int = 1


class BaseTask:
    def __init__(self, *args, **kwargs):
        self.language = kwargs["language"]
        self.is_compiled = False

    def run_python3(self, stdin, time_limit) -> str:
        raise NotImplementedError
    
    def compile_cpp(self):
        raise NotImplementedError

    def run_cpp(self, stdin, time_limit):
        if not self.is_compiled:
            self.compile_cpp()
            self.is_compiled = True
        
        raise NotImplementedError

    # raises Exception on time limit or compilation failure
    def run_solution(self, time_limit, stdin : str) -> str:
        if self.language == "python3":
            return self.run_python3(stdin, time_limit)
        elif self.language == "cpp":
            return self.run_cpp(stdin, time_limit)

    def run_tests(self, tests: list[TestCase]) -> tuple[bool, str]:
        raise NotImplementedError

    def check(self) -> tuple[bool, str]:
        raise NotImplementedError

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        pass
