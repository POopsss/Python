def r(): # Запись хода в игровое поле и завершении текущей партии
    for i in range(9):
        # Указатель "Чей ход"
        y = 'x' if i % 2 == 0 else 'o'
        mp[0][0] = y

        u()
        # Запись хода в игровое поле
        x = w()
        mp[x[0]][x[1]] = y
        # Объявление Победы и завершение текущей партии
        if e(x):
            print('Победил [', y,']')
            u()
            return
    # Объявление Ничьи и завершение текущей партии
    print('Ничья')
    u()
    return

def q(): # Ввод хода и проверка корректности введенных значений
    x = input(f'Укажите 2 числа от 0 до 2, первое число строка, второе столбец.\nХод [{mp[0][0]}]: ').split()
    # Проверка на введение 2ух значений
    if len(x) == 2:
        # Проверка на введение числовых значений
        for i in range(2):
            if x[i].isdigit():
                x[i] = int(x[i]) + 1
                # Проверка на вхождение введеных значений в игровое поле
                if x[i] > 3: #'.isdigit()' True если число целое и не отрицательное, поэтому нет проверки '< 0'
                    print('Указанные значения вне игрового поля')
                    return
            else:
                print('Только числа')
                return
        # Проверка на занятость клетки
        if (mp[x[0]][x[1]]) != ' ':
            print('Место занято')
            return

    else:
        print('Введите 2 числа от 0 до 2')
        return

    return x

def w(): # Запрашиваем новые значения пока они не удовлетворят всем требованиям
    x = q()
    while not x:
        x = q()
    return x

def e(a): # Поиск выигрышной комбинации
    w = 0
    if mp[a[0]][1] == mp[a[0]][2] == mp[a[0]][3]: #По горизонтали
        w = 1
        return w
    if mp[1][a[1]] == mp[2][a[1]] == mp[3][a[1]]: #По вертикали
        w = 1
        return w
    if mp[1][1] == mp[2][2] == mp[3][3] or mp[1][3] == mp[2][2] == mp[3][1]: # По диагонали
        if mp[2][2] == 'x' or mp[2][2] == 'o':
            w = 1
    return w

def u(): #Визуализация игрового поля
    for i in mp:
        m = f'{i[0]} | {i[1]} | {i[2]} | {i[3]} |'
        print(m)
        print('---------------')
    return

# Старт Игры
start = input('Начать игру? Да [Y], Нет [N]: ')
while start == 'Y':
    # Генерация игрового поля
    mp = [[' '] * 4 for i in range(4)]
    for i in range(len(mp)):
        mp[0][i], mp[i][0] = i - 1, i - 1

    r()
    start = input('Желаете повторить? Да [Y], Нет [N]: ')
print('Игра окончена')







