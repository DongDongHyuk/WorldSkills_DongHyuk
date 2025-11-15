from functools import wraps


def counter_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)
    wrapper.counter = 0
    return wrapper

@counter_decorator
def my_func():
    pass

@counter_decorator
def you_func():
    pass

my_func()
my_func()
my_func()
my_func()

you_func()
you_func()

print('my_func 출력 횟수 :', my_func.counter)
print('you _func 출력 횟수 :', you_func.counter)
