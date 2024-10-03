from russian_names import RussianNames

# print(RussianNames().get_person())
# , output_type='dict'

def get_fio(patronymic, name, surname):
    data = RussianNames(count=1, patronymic=patronymic, name=name, surname=surname)
    batch = data.get_batch()
    return batch


def get_full_name():
    full_name = ''
    for i in range(3):
        if i == 0:
            data = get_fio(patronymic=False, name=False, surname=True)
        if i == 1:
            data = get_fio(patronymic=False, name=True, surname=False)
        if i == 2:
            data = get_fio(patronymic=True, name=False, surname=False)

        full_name += data[0] + ' '

    return full_name




print(get_fio(patronymic=False, name=False, surname=True))
print(get_full_name())
