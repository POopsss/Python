from random import randint


class Error(Exception):
    pass


class Input_error_1(Error):
    def __str__(self):
        return '2 координаты!'


class Input_error_2(Error):
    def __str__(self):
        return 'Цыфры!!'


class Input_error_3(Error):
    def __str__(self):
        return 'Значения за пределами поля'


class Input_error_4(Error):
    def __str__(self):
        return 'Сюда уже стреляли!'


class Ship:
    def __init__(self, dot, len, orient):
        self.len = len
        self.orient = orient
        self.dot = dot
        self.lives = len

    def contour(self):  # Контур корабля
        self.contour = []
        x = self.dot[0]
        y = self.dot[1]
        for i in range(self.len):
            self.contour.append([x, y])
            if self.orient == 0:
                y += 1
            else:
                x += 1
        return self.contour

    def ship_gen():  # Генерация кораблей
        len = [3, 2, 2, 1, 1, 1]
        ship_list = []
        busy = []
        b = 0
        for i in len:
            while True:
                b += 1
                if b == 1000:
                    break
                a = 1
                ship = Ship([randint(0, 5), randint(0, 5)], i, randint(0, 1))
                ship.contour()
                if Error_Test().gen_ship_error(ship.contour, busy):
                    ship_list.append(ship)
                    busy += Shot.busy(ship.contour)
                    break
        return ship_list

    def wound(self):  # Корабль получает рану
        self.lives += -1
        if self.lives == 0:
            print('Уничтожил!')
            return True
        return False


class Desk:  # Отрисовка доски
    def __init__(self, ship_list, shot_list, hid):
        self.ship_list = ship_list
        self.shot_list = shot_list
        self.board = [[' '] * 6 for i in range(6)]
        self.hid = hid

    def add_ship_shot(self):  # Добавление на доску кораблей и выстрелов
        for i in range(len(self.ship_list)):
            for a in self.ship_list[i].contour:
                self.board[a[0]][a[1]] = '■'

        for i in self.shot_list:
            if self.board[i[0]][i[1]] == '■':
                self.board[i[0]][i[1]] = 'X'
            else:
                self.board[i[0]][i[1]] = '×'
        return self.board

    def __str__(self):
        res = ""
        res += " | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.board):
            res += f"\n{i + 1} | " + "   ".join(row) + " |"

        if self.hid:
            res = res.replace("■", " ")
        return res


class Error_Test:  # Проверки на ошибки генерации и ввода
    def input_error(self, test, shot_list):
        self.test = ''
        self.test = test.split()
        self.shot_list = shot_list
        if len(self.test) != 2:
            raise Input_error_1()

        for i in range(len(self.test)):
            if not (self.test[i]).isdigit():
                raise Input_error_2()
            self.test[i] = int(self.test[i])

            if self.test[i] > 6 or self.test[i] < 1:
                raise Input_error_3()

            self.test[i] += -1
        return self.test

    def shot_list_test(test, shot_list, ai=0):
        if test in shot_list:
            raise Input_error_4()
        return test

    def gen_ship_error(self, contour, busy):
        for i in contour:
            if i[0] > 5 or i[1] > 5:
                return False
            if i in busy:
                return False
        return True


class Shot:  # Стрельба
    def shot(shot_list, ai):
        while True:
            try:
                if ai == 0:
                    shot = Error_Test().input_error(input(), shot_list)
                    Error_Test.shot_list_test(shot, shot_list)
                else:
                    shot = Error_Test.shot_list_test([randint(0, 5), randint(0, 5)], shot_list, 1)
            except Error as e:
                if ai == 0:
                    print(e)
            else:
                return shot

    def hit(shot, ship_list):  # Проверка на попадание
        for i in range(len(ship_list)):
            if shot in ship_list[i].contour:
                print('Попал!')
                ship_list[i].wound()
                return i + 1

    def busy(contour):  # Генерация точек выстрела после уничтожения корабля
        c = [[1, 1], [1, 0], [0, 1], [-1, 0], [0, 0], [0, -1], [-1, -1], [1, -1], [-1, 1]]
        d = []
        for i in contour:
            for o in c:
                u = (list(map(sum, zip(o, i))))
                if -1 < u[0] < 6 and -1 < u[1] < 6 and u not in d:
                    d.append(u)
        return d


class Player:  # Генерация игроков и их ходы
    def __init__(self, ai):
        self.shot_list = []
        self.life = 6
        self.ai = ai
        self.ship = []
        while len(self.ship) < 6:
            self.ship = Ship.ship_gen()

    def shot(self):
        shot = Shot
        self.shot_list.append(shot.shot(self.shot_list, self.ai))
        hit = shot.hit(self.shot_list[-1], self.ship)
        if hit:
            g.a += -1
            if self.ship[hit - 1].lives == 0:
                self.life += -1
                busy = Shot.busy(self.ship[hit - 1].contour)
                for i in busy:
                    if i not in self.shot_list:
                        self.shot_list.append(i)


class Game:  # Логика
    def __init__(self):
        self.player = Player(0)
        self.ai_player = Player(1)
        self.a = 0

    def loop(self):
        while True:
            if self.a % 2 == 0:
                board_1 = Desk(self.player.ship, self.player.shot_list, 1)
                board_1.add_ship_shot()
                board_2 = Desk(self.ai_player.ship, self.ai_player.shot_list, 0)
                board_2.add_ship_shot()
                print('\n', board_2, f'\n {"-" * 25} \n', board_1, '\n', 'Ход Игрока:')
                self.player.shot()
            else:
                self.ai_player.shot()
            self.a += 1
            if self.player.life == 0:
                print('Победил игрок!')
                break
            if self.ai_player.life == 0:
                print('Победил AI!')
                break


g = Game()
g.loop()