def async(action):
    def decorator(thread_cnt):
        def wrapper(*args, **kwargs):
            print(thread_cnt)
            result = action(*args, **kwargs)
            result['thread'] = 1
            return result
        return wrapper
    return decorator

def logger(action):
    def wrapper(*args, **kwargs):
        print('Запуск действия')
        result = action(*args, **kwargs)
        print('Действие выполнено')
        return result
    return wrapper

@logger
@async(thread_cnt=1)
def action(num):
    return {
        'result': [
            str(x) for x in range(num) if x % 2 == 0
        ],
    }

print('Результат', action(10))
