from functools import wraps


"""
counter_decorator 데코레이터가 적용된 함수 X의 실행횟수를 
X.counter 속성의 변수로 저장하며, 함수 각자만의 고유의 속성이된다.

이 속성은 다른 함수의 counter 값을 공유하지않는다.

또한 counter_decorator 내부의 wrapper 의 이름을 가지는
inner function 에 @wraps 데코레이터를 사용하여
counter_decorator 데코레이터를 호출하는 함수들 간의 메타데이터를
변경되지않도록 제작하였다.
"""

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

my_func() #1회 호출
my_func() #2회 호출
my_func() #3회 호출
my_func() #4회 호출

you_func() #1회 호출
you_func() #2회 호출


#my_func의 counter 속성으로 저장된 값 4가 출력된다.
print('my_func 출력 횟수 :', my_func.counter)
#you_func의 counter 속성으로 저장된 값 2가 출력된다.
print('you _func 출력 횟수 :', you_func.counter)
