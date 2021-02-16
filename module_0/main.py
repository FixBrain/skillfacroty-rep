def game_core(number):
    predict_a = 1
    predict_b = 100
    predict = (predict_a + predict_b) // 2
    while predict != number:
        if number > predict:
            predict_a = predict
            predict = (predict_a + predict_b) // 2
        elif number < predict:
            predict_b = predict
            predict = (predict_a + predict_b) // 2
    return predict


number = int(input("Введите число от 1 до 100: "))
print(game_core(number))

