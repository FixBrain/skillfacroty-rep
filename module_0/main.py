import numpy as np


def game_core(number):
    """Функция, угадывающая загаданное целое число методом половинного деления.

    :param number: угадываемое число
    :return: угаданное число
    """
    count = 0
    predict_a = 1 # начало диапазона, которому принадлежит загаданное число
    predict_b = 100 # конец диапазона, которому принадлежит загаданное число
    predict = (predict_a + predict_b) // 2 # стартовое значение, с которого перебираем

    # выполняем алгоритм, пока значения прогноза и введенного числа не сойдутся
    while predict != number:
        # если введенное число больше текущего прогноза
        if number > predict:
            # сдвигаем нижнюю границу исследуемого диапазона в текущее предсказание
            predict_a = predict + 1
        # если введенное число меньше текущего прогноза
        elif number < predict:
            # сдвигаем верхнюю границу исследуемого диапазона в текущее предсказание
            predict_b = predict - 1
        # в качестве нового прогноза выбираем середину измененного диапазона
        predict = (predict_a + predict_b) // 2
        count += 1

    return count


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


# проверяем
score_game(game_core)

