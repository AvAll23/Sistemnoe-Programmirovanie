import time
menu = 0
while True:
    if menu == 0:
        print("ПР 3 Мухин Д.Е. Вариант 11")
        print("Задания для самостоятельного выполнения:")
        print("Выберите задание (1-3)")
        menu = int(input())
    elif menu == 1:
        print("Задание 1:")
        answer = input("Укажите дату начала второй мировой войны:")
        if "1939" in answer:
            print("Правильно!")
        else:
            print("Неправильно! Вторая мировая началась 1 сентября 1939 года.")
    elif menu == 2:
        print("Задание 2:")
        x = float(input("Введите x: "))
        y = float(input("Введите y: "))
        if x ** 2 + y ** 2 <= 25 and y >= x ** 2:
            print("Точка принадлежит заштрихованной области")
        else:
            print("Точка не принадлежит заштрихованной области")
    elif menu == 3:
        print("Задание 3:")
    #доделать
    else:
        print("Такого номера задания нет!")
        print("Возвращаем вас назад...")
        time.sleep(2)
        menu = 0