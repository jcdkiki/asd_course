import argparse
import asd_course
import sys

def check_task(task):
    passed, msg = task.check()
    if passed:
        print("OK!")
        sys.exit(0)
    
    print(msg)
    sys.exit(1)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["check"])
    parser.add_argument("--language", required=True, choices=["cpp", "python3"])
    subparsers = parser.add_subparsers(required=True)

    subclasses = asd_course.base_module.BaseTask.__subclasses__()
    for cls in subclasses:
        subparser = subparsers.add_parser(cls.__name__)
        subparser.set_defaults(func=cls)
        cls.add_args(subparser)

    args = parser.parse_args()
    
    stud_code = open(f"/app/solution.{'cpp' if args.language == 'cpp' else 'py'}").read()
    task = args.func(solution = stud_code, **vars(args))

    match args.mode:
        case "check": check_task(task)
