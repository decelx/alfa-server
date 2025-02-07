def write_log(message):
    try:
        with open('log.txt', 'a') as file:
            file.write(message.args[0] + '\n')
    except:
        print('ошибка логера')