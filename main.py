import argparse
import asd_course

def check_task(task):
    passed, msg = task.check()
    print(passed, msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["check"])
    parser.add_argument("--language", required=True, choices=["cpp", "python3"])
    parser.add_argument("--solution", required=True)
    subparsers = parser.add_subparsers(required=True)

    subclasses = asd_course.base_module.BaseTask.__subclasses__()
    for cls in subclasses:
        subparser = subparsers.add_parser(cls.__name__)
        subparser.set_defaults(func=cls)
        cls.add_args(subparser)

    args = parser.parse_args()
    task = args.func(**vars(args))

    match args.mode:
        case "check": check_task(task)
