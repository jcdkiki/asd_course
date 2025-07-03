import argparse
import dataclasses
import subprocess
import time

@dataclasses.dataclass
class TestCase:
    stdin : str
    expected : str
    time_limit : int = 1


class CompileException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        

class LinkException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        
        
class LanguageException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        

class TimeLimitException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        
                
class BaseTask:
    def __init__(self, *args, **kwargs):
        self.language = kwargs["language"]
        self.solution = kwargs["solution"]
        self.solve_dir = None
        self.cpp_complile_args = ""
        self.py_compile_args = ""

        match self.language:
            case "python3":
                with open('solution.py', 'w') as f:
                    f.write(self.solution)
            case "cpp":
                with open('solution.cpp', 'w') as f:
                    f.write(self.solution)
            case _:
                raise LanguageException("Unexpected language")

        self.is_solve_compiled = False
        self.is_compiled = False
        self.cheating_checked = False

    def run_python3(self, stdin, time_limit) -> str:
        if not self.cheating_checked:
            # smth like py_check_for_cheating(self.source)
            self.cheating_checked = True
        
        try:
            r = subprocess.run(
                ["python3", "solution.py"], 
                input=stdin,
                universal_newlines=True,
                timeout=time_limit,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE
            )
            if r.returncode != 0:
                raise Exception(f"Program exited with code {r.returncode}:\n{r.stdout}")
            return r.stdout
        except subprocess.TimeoutExpired:
            raise TimeLimitException("Time limit expired")
    
    # throws CompileException on compilation error
    def compile_cpp(self):
        cpp_flags = "-Wall -Werror -std=c++11"
        compile_cmd = f"g++ {cpp_flags} -c solution.cpp"
        run = subprocess.run(compile_cmd.split(), stderr=subprocess.PIPE)
        if run.returncode != 0:
            raise CompileException(f"Compilation failed:\n{run.stderr.decode()}")
        
    # throws LinkException on linking error
    def link_cpp(self):
        bin_cmd = f"g++ -std=c++11 -o solution solution.cpp"
        run = subprocess.run(bin_cmd.split(), stderr=subprocess.PIPE)
        if run.returncode != 0:
            raise LinkException(f"Linking failed:\n{run.stderr.decode()}")
        
    def run_cpp(self, stdin, time_limit) -> str:
        if not self.is_compiled:
            self.compile_cpp()
            self.link_cpp()
            self.is_compiled = True
        if not self.cheating_checked:
            # smth like cpp_check_for_cheating("src.o")
            self.cheating_checked = True
        
        try:
            r = subprocess.run(
                ["./solution"], 
                input=stdin,
                text=True,
                universal_newlines=True,
                timeout=time_limit,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE
            )
            if r.returncode != 0:
                raise Exception(f"Program exited with code {r.returncode}:\n{r.stdout}")
            return r.stdout
        except subprocess.TimeoutExpired:
            raise TimeLimitException("Time limit expired")

    # raises Exception on time limit or compilation failure
    def run_solution(self, time_limit, stdin : str) -> str:
        if self.language == "python3":
            return self.run_python3(stdin, time_limit)
        elif self.language == "cpp":
            return self.run_cpp(stdin, time_limit)
        else:
            raise LanguageException(f"Unknown language {self.language}")

    def run_tests(self, tests : list[str]) -> tuple[bool, str]:
        for test in tests:
            expected, time_limit = self.solve(test)
            ok, msg = self.run_test(TestCase(test, expected, time_limit))
            if not ok:
                return ok, msg
        
        return True, "OK!"

    def run_test(self, test : TestCase) -> tuple[bool, str]:
        try:
            raw_answ = self.run_solution(test.time_limit, test.stdin)
            answ = raw_answ.strip()
        except Exception as e:
            return False, \
                f"Test failed:\n" \
                f"Error: {str(e)}" 
        
        if answ != test.expected:
            return False, \
                f"Test failed:\n" \
                f"Input: {test.stdin}\n" \
                f"Output: {answ}\n"
        
        return True, "OK!"

    def check(self) -> tuple[bool, str]:
        raise NotImplementedError
    
    def solve(self, stdin : str) -> tuple[str, float]:
        if self.language == "python3":
            cmd_comand = f"python3 {self.solve_dir}/solve.py {self.py_compile_args}" 
        elif self.language == "cpp":
            if not self.is_solve_compiled:
                cmd_comand = f"g++ -std=c++11 {self.cpp_complile_args} -o solve {self.solve_dir}/solve.cpp"
                subprocess.run(cmd_comand.split())
                self.is_solve_compiled = True
            cmd_comand = f"./solve"
        
        start = time.time()
        run = subprocess.run(cmd_comand.split(),
                             input=stdin,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        end = time.time()
        time_limit = 2 * (end - start) if end - start > 0 else 1
        return run.stdout.strip(), time_limit

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None:
        pass
