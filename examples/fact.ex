def max():
    pass

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def main():
    print('Вычисление факториалов')
    for i in range(10):
        print('Факториал ', i, ' = ', factorial(i))

main()
