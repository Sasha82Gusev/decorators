import os
from _datetime import datetime


def logger_func(path):
    def __logger(oldfunction):
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%d-%m-%Y время %H:%M:%S')
            func_name = oldfunction.__name__
            result = oldfunction(*args, **kwargs)
            with open(path, 'a') as file:
                file.write(f'\nВремя вызова функции: {call_time}\n'
                           f'Имя функции: {func_name}\n'
                           f'Аргументы функции: {args, kwargs}\n'
                           f'Возвращаемое значение функции: {result}\n'
                           f'{"___________________________________"}\n')
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_func(path)
        def hello_world():
            return 'Hello World'

        @logger_func(path)
        def summator(a, b=0):
            return a + b

        @logger_func(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        print(log_file_content)
        assert 'summator' in log_file_content, 'должно записаться имя функции'
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()