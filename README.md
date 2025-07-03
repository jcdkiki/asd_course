# asd_course

## Как добавить свою лабу?

1. Создать папку `src/asd_course/LAB_NAME`

2. Создать в этой папке `__init__.py`:

```py
from .lab import LAB_NAME
```

3. Создать в этой папке `lab.py`:

```py
from asd_course.base_module import BaseTask, TestCase
import argparse
import os

class LAB_NAME(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.shift = kwargs["shift"]

        self.solve_dir = os.path.dirname(os.path.realpath(__file__))
        self.cpp_complile_args = f"-DSHIFT={self.shift}"    # см. "Компиляция solve-файла"
        self.py_compile_args   = f"--shift {self.shift}"

    def check(self) -> tuple[bool, str]:
        tests = [       # см. "Тесты для проверки решения"
            "abc",
            "gdkknvnqkc",
            "gnvcxgn",
            ...
        ]
        return self.run_tests(tests)

    @staticmethod
    def add_args(parser : argparse.ArgumentParser) -> None: 
        parser.add_argument("--shift", default=1, type=int) # см. "Вариация условия задания"
```

4. Создать в этой папке `solve.cpp` -- решение задания на C++

5. Создать в этой папке `solve.py` -- решение задания на Python

6. Создать папки `tst/LAB_NAME/fail` и `tst/LAB_NAME/success`:

Это тесты на работоспособность системы проверки. Перед своими коммитами проверяйте чтобы всё работало, запуская тесты с помощью:

```sh
python3 ./tst/test.py
```

В папке success должны лежать правильные решения задания.
В папке fail должны лежать неправильные решения задания.

Все тесты пройдены, если в конце будет написано:
```
==================================================
Final result: ALL TESTS PASSED
```

Для подробного анализа результатов тестирования используйте флаг `--verbose`:

```sh
python3 ./tst/test.py --verbose
```


## Как запустить проверку лабы

1. Сначала убедитесь, что докер образ собран:

```sh
./scripts/build.sh
```

2. Запустите докер контейнер:

```sh
docker run --rm -v PATH_TO_YOUR_FILE:/app/solution.cpp moevm/asd_course --language cpp --mode check LAB_NAME
```

или

```sh
docker run --rm -v PATH_TO_YOUR_FILE:/app/solution.py moevm/asd_course --language python3 --mode check LAB_NAME
```

3. Альтернативно, можно запустить сразу все тесты из папки `tst`

```sh
python3 ./tst/main.py
```

## Вариация условия задания

Условия заданий лаб можно менять, например, в зависимости от ID студента.

В конструкторе класс с вашей лабой принимает `**kwargs`.
Через него можно передавать всякие параметры для вашей лабы.

## Тесты для проверки решения

Метод `self.run_tests` ожидает список строк. Эти строки будут поданы в `solve.cpp` или `solve.py` в стандартный поток ввода (stdin).
Аналогично эти же строки будут поданы в решение студента в stdin. Результаты сравниваются.

## Компиляция solve-файла

Поскольку условие задания может варьироваться, то solve-файлы (файлы с правильным решением задания) должны варьироваться соответствующим образом.

Поэтому при компиляции cpp файла параметры для варьирования условия задания передаются в качестве макроопределений, а при запуске решения на python параметры в качестве аргументов командной строки.
