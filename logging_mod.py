import time

from .common.singletones import SingletonByName


class ConsoleWriter:
    @staticmethod
    def write(text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file = file_name

    def write(self, text):
        with open(self.file, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write(f'log--> {text}')


def debug(func):

    def decor(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG------>', func.__name__, end - start)
        return result

    return decor


if __name__ == '__main__':

    logger = Logger('log')
    logger.log('test')

    file_log = Logger('file_log', FileWriter('logs'))
    file_log.log('test')
