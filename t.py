import subprocess
import time

def main():
    stdin = '10'
    cmd_comand = f"g++ -std=c++11 solve.cpp -DSHIFT=7 -o solve"
    run = subprocess.run(cmd_comand.split())
    cmd_comand = f"./solve"
    start = time.time()
    run = subprocess.run(cmd_comand.split(), 
                         input=stdin,
                         universal_newlines=True, 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    end = time.time()
    print(run.stdout, end - start)
    
if __name__ == "__main__":
    main()
    
    
def test_solution(language, file_path, lab_name, verbose, expect_ok=True):
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(file_path)))
    # Получаем директорию, где лежит тестируемый файл
    file_dir = os.path.dirname(file_path)
    
    # Формируем базовую команду Docker
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{file_path}:/app/solution.{'cpp' if language == 'cpp' else 'py'}",
        "moevm/asd_course",
        "--language", language,
        "--mode", "check",
        lab_name
    ]

    # Добавляем монтирование solve.cpp/solve.py, если они существуют
    additional_files = []
    if language == "cpp":
        solve_cpp = os.path.join(file_dir, "solve.cpp")
        if os.path.exists(solve_cpp):
            additional_files.append(("-v", f"{solve_cpp}:/app/solve.cpp"))
    else:
        solve_py = os.path.join(file_dir, "solve.py")
        if os.path.exists(solve_py):
            additional_files.append(("-v", f"{solve_py}:/app/solve.py"))

    # Вставляем дополнительные параметры монтирования после основного -v
    for mount_param in additional_files:
        docker_cmd.insert(4, mount_param[1])  # Вставляем значение -v
        docker_cmd.insert(4, mount_param[0])  # Вставляем параметр -v

    options = extract_options(file_path)
    docker_cmd += options
    
    print(f"  Testing: {rel_path} ({language.upper()})")
    
    if verbose:
        print(f"    Command: {' '.join(docker_cmd)}")
        print("    Output:")
        result = subprocess.run(
            docker_cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        for line in result.stdout.splitlines():
            print(f"      {line}")
        print(f"    Exit code: {result.returncode}")
    else:
        result = subprocess.run(
            docker_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    if (expect_ok and result.returncode == 0) or (not expect_ok and result.returncode != 0):
        print(f"    \033[32m PASS\033[0m")
        return True
    else:
        print(f"    \033[31m FAIL (exit code: {result.returncode})\033[0m")
        return False