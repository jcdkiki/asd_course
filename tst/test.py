import os
import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed test output")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    overall_success = True
    
    for entry in os.listdir(base_dir):
        lab_dir = os.path.join(base_dir, entry)
        if os.path.isdir(lab_dir):
            print(f"\n\033[1mTesting lab: {entry}\033[0m")
            lab_success = True
            
            for root, _, files in os.walk(os.path.join(lab_dir, "success")):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(".cpp"):
                        lab_success &= test_solution("cpp", file_path, entry, args.verbose)
                    elif file.endswith(".py"):
                        lab_success &= test_solution("python3", file_path, entry, args.verbose)
            
            for root, _, files in os.walk(os.path.join(lab_dir, "fail")):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(".cpp"):
                        lab_success &= test_solution("cpp", file_path, entry, args.verbose, False)
                    elif file.endswith(".py"):
                        lab_success &= test_solution("python3", file_path, entry, args.verbose, False)

            status = "\033[32mPASS\033[0m" if lab_success else "\033[31mFAIL\033[0m"
            print(f"\nLab {entry} overall: {status}")
            overall_success &= lab_success
    
    print("\n" + "=" * 50)
    final_status = "\033[32mALL TESTS PASSED\033[0m" if overall_success else "\033[31mSOME TESTS FAILED\033[0m"
    print(f"Final result: {final_status}")
    sys.exit(0 if overall_success else 1)

def extract_options(file_path):
    options = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("# options:"):
                    options = stripped.split(" ", 2)[2].split()
                    break
                elif stripped.startswith("// options:"):
                    options = stripped.split(" ", 2)[2].split()
                    break
    except Exception as e:
        print(f"    \033[33mWarning: Failed to read options from {file_path}: {e}\033[0m")
    return options

def test_solution(language, file_path, lab_name, verbose, expect_ok=True):
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(file_path)))
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{file_path}:/app/solution.{'cpp' if language == 'cpp' else 'py'}",
        "moevm/asd_course",
        "--language", language,
        "--mode", "check",
        lab_name
    ]

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

if __name__ == "__main__":
    main()
