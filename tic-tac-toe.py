"""
Игра Крестики-нолики. Учебный проект.
"""
import random


def draw_intro():
    """Выводим название игры и правила."""
    print('              Игра Крестики-нолики                 ')
    print('На поле 3х3 вы можете ходить задавая две координаты')
    print('Например, ход \'1 1\' поставит крестик в центре поля')
    print('Крестики и нолики ходят по очерели, выигрывает тот,')
    print('кто первым поставит три крестика или нолика в ряд  ')
    print('===================================================')


def draw_field(field):
    """Выводим игровое поле."""
    print('    0   1   2 ')
    print('   --- --- ---')
    for i in range(3):
        print(f"{i} | {field[i][0]} | {field[i][1]} | {field[i][2]} |")
        print('   --- --- ---')


def input_a_move(field):
    """Просим ввести ход до тех пор, пока пользователь не введет правильно."""
    while True:
        print('Введите две координаты от 0 до 2 через пробел, например 1 1:')
        try:
            x, y = [int(x) for x in input().split()]
        except ValueError:
            print('Ошибка: Кооодинаты должны быть целым числом от 0 до 2')
            continue
        if not 0 <= x <= 2 or not 0 <= y <= 2:
            print('Ошибка: Координаты должны быть целым числом от 0 до 2')
            continue
        if field[x][y] != ' ':
            print('Ошибка: Эта клетка уже занята, выберите другую')
        return x, y


def check_end_of_game(field, move):
    """Проверяем условия окончания игры и определяем победителя."""
    win_coords = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
                  ((2, 0), (2, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)),
                  ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                  ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for coord in win_coords:
        line = []
        for i in coord:
            line.append(field[i[0]][i[1]])
        if line == ["X", "X", "X"]:
            return 'X'
        if line == ["0", "0", "0"]:
            return '0'
    if move == 9:
        return 'Ничья'
    return ''


def input_type_of_game():
    """Выбор типа игры."""
    print('Выберите вариант игры:')
    print('1 - два человека')
    print('2 - игра с простым компьютером')
    print('3 - игра со сложным компьютером')
    while True:
        type = input()
        if type.isdigit():
            if 1 <= int(type) <= 3:
                return type
        print('Введите целое число от 1 до 3')


def easy_computer_move(field):
    """Выбор хода для простого компьютера."""
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if field[x][y] == ' ':
            return x, y


def minimax_score(field, move, depth):
    """Подсчет суммы выигрыша варианта хода для авгоритма минимакс."""
    if check_end_of_game(field, move) == 'X':
        return 10 - depth
    elif check_end_of_game(field, move) == '0':
        return depth - 10
    else:
        return 0


def minimax(field, move, depth):
    """Выбор хода для сложного компьютера."""
    if check_end_of_game(field, move):
        return 0, 0, minimax_score(field, move, depth)
    candidate_move_nodes = []
    for i in range(3):
        for j in range(3):
            if field[i][j] == ' ':
                if move & 1 == 1:
                    field[i][j] = '0'
                else:
                    field[i][j] = 'X'
                score = minimax(field, move+1, depth+1)
                candidate_move_nodes.append((i, j, score[2]))
                field[i][j] = ' '

    min = 10
    max = -10

    for z in candidate_move_nodes:
        if z[2] > max:
            max = z[2]
            i_max = z[0]
            j_max = z[1]
        if z[2] < min:
            min = z[2]
            i_min = z[0]
            j_min = z[1]
    if move & 1 == 1:
        return i_min, j_min, min
    else:
        return i_max, j_max, max


def computer(field, move, type):
    """Основная фкнуция для игры с любым компьютером."""
    while not check_end_of_game(field, move):
        draw_field(field)
        if move & 1 == 1:
            print('Ходит 0')
            if type == '2':
                x, y = easy_computer_move(field)
            else:
                x, y, z = minimax(field, move, 0)
            field[x][y] = '0'
        else:
            print('Ходит Х')
            x, y = input_a_move(field)
            field[x][y] = 'X'
        move += 1
    return move


def two_people(field, move):
    """Основная функция для игры вдвоем."""
    while not check_end_of_game(field, move):
        draw_field(field)
        if move & 1 == 1:
            print('Ходит 0')
        else:
            print('Ходит Х')
        x, y = input_a_move(field)
        if move & 1 == 1:
            field[x][y] = '0'
        else:
            field[x][y] = 'X'
        move += 1
    return move


if __name__ == '__main__':
    field = [[" "] * 3 for i in range(3)]
    move = 0
    # Тестовые данные для короткой игры
    # field = [['0', 'X', '0'], [' ', 'X', ' '], ['X', ' ', ' ']]
    # move = 5
    draw_intro()
    game_type = input_type_of_game()
    if game_type == '1':
        final_move = two_people(field, move)
    elif game_type == '2' or game_type == '3':
        final_move = computer(field, move, game_type)
    draw_field(field)
    winner = check_end_of_game(field, final_move)
    if winner in ('X', '0'):
        print(f'Выиграл {winner}!')
    else:
        print(winner)
