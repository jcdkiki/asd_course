import argparse
import dataclasses
import subprocess

@dataclasses.dataclass
class TestCase:
    stdin : str
    expected : str
    time_limit : int = 1


class CompileException(Exception):
    def __init__(msg):
        super().__init__(msg)
        

class LinkException(Exception):
    def __init__(msg):
        super().__init__(msg)
        
        
class LanguageException(Exception):
    def __init__(msg):
        super().__init__(msg)
        
                
class BaseTask:
    def __init__(self, *args, **kwargs):
        self.language = kwargs["language"]
        match self.language:
            case "python3":
                self.filename = "__tester__.py"
                with open("./src/solution.py", "r") as file:
                    self.source = '\n'.join(file.readlines())
            case "cpp":
                self.filename = "__tester__.cpp"
                with open("./src/solution.cpp", "r") as file:
                    # ??? - student writes includes by himself or not
                    self.source = '\n'.join(file.readlines())
            case _:
                raise LanguageException("Unexpected language")
        self.is_compiled = False
        self.cheating_checked = False

    def run_python3(self, stdin, time_limit) -> str:
        if not self.cheating_checked:
            # smth like py_check_for_cheating(self.source)
            self.cheating_checked = True
        # we need to give subproc smth like ["python3", "./src.py"]
        return subprocess.check_output(["python3", self.filename], input=stdin, universal_newlines=True)
    
    def compile_cpp(self):
        # where source code stored? (self.source or just self.source seems good idk)
        # compile with 11 std like in moodle and get object src.o
        cpp_flags = "-Wall -Werror -std=c++11"
        compile_cmd = (f"g++ {cpp_flags} -c -o ./__tester__.o {self.filename}").split()
        return_code = subprocess.check_call(compile_cmd)
        if return_code != 0:
            raise CompileException("Compilation failed. Testing aborted")
        print(str(subprocess.check_call(["ls","-l"])))

    def build_cpp(self):
        # link an object and get binary src
        bin_cmd = (f"g++ -std=c++11 -o __tester__ ./__tester__.o").split()
        return_code = subprocess.check_call(bin_cmd)
        if return_code != 0:
            raise LinkException("Linking failed. Testing aborted")
        print(str(subprocess.check_call(["ls","-l"])))
        
    def run_cpp(self, stdin, time_limit) -> str:
        if not self.is_compiled:
            self.compile_cpp()
            self.build_cpp()
            self.is_compiled = True
        if not self.cheating_checked:
            # smth like cpp_check_for_cheating("src.o")
            self.cheating_checked = True
        # we need to give subproc smth like [./src]
        return subprocess.check_output(["./__tester__"], input=stdin, universal_newlines=True)

    # raises Exception on time limit or compilation failure
    def run_solution(self, time_limit, stdin : str) -> str:
        if self.language == "python3":
            return self.run_python3(stdin, time_limit)
        elif self.language == "cpp":
            return self.run_cpp(stdin, time_limit)
        else:
            raise LanguageException(f"Unknown language {self.language}")

    def run_tests(self, tests: list[TestCase]) -> tuple[bool, str]:
        # we can skip it if student will write includes by himself idk
        with open(self.filename, "w") as file:
            print(self.source, file=file)
        
        correct = 0
        for test in tests:
            try:
                answ = self.run_solution(test.time_limit, test.stdin).strip()
                print(answ)
            except subprocess.CalledProcessError as e:
                return False, e.output
            except (LinkException, CompileException, LanguageException) as e:
                return False, str(e)
            if answ == test.expected: # maybe we can skip expected item if we will run example code in timelimit checks
                correct+=1
        print(f"{len(tests)} have passed!")
        if correct == len(tests):
            return True, "OK"
        else:
            return False, f"{len(tests) - correct} has failed"
                

    def check(self) -> tuple[bool, str]:
        raise NotImplementedError

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        pass
