def add_word(user, dict, russian, translate):
    with open(f"./data/{user}_{dict}.csv", "a", encoding="utf-8") as f:
        f.write(f"{russian},{translate}\n")

def add_dict(user, name):
    with open(f"./data/{user}_{name}.csv", "w", encoding="utf-8") as f:
        f.write(f"Cлово,Перевод\n")
    with open(f"./data/{user}_dicts.csv", "a", encoding="utf-8") as f:
        f.write(f'{name}\n')

def get_dicts(user):
    users = []
    with open(f"./data/{user}_dicts.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            users.append(line[:-1])
    return users

def add_user(user):
    with open(f"./data/{user}_materials.csv", "w", encoding="utf-8") as f:
        f.write(f"Название,Сылка,Оценка\n")
    with open(f"./data/{user}_lessons.csv", "w", encoding="utf-8") as f:
        f.write(f"Дата,Темы,Оценка сложности\n")
    with open(f"./data/{user}_dicts.csv", "w", encoding="utf-8") as f:
        f.write(f"Словари\n")
    with open(f"./data/users.csv", "a", encoding="utf-8") as f:
        f.write(f'{user}\n')

def get_users():
    users = []
    with open(f"./data/users.csv", "r", encoding="utf-8") as f:
        for line in f.readlines():
            users.append(line[:-1])
    return users


def add_lesson(user, date, thems, est):
    new_lesson_line = f"{date};{thems};{est}"
    with open(f"./data/{user}_lessons.csv", "r", encoding="utf-8") as f:
        existing_lessons = [l.strip("\n") for l in f.readlines()]
        title = existing_lessons[0]
        old_lessons = existing_lessons[1:]
    lessons_sorted = old_lessons + [new_lesson_line]
    lessons_sorted.sort()
    new_lessons = [title] + lessons_sorted
    with open(f"./data/{user}_lessons.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_lessons))

def add_material(user, name, link, est=' '):
    new_material_line = f"{name};{link};{est}"
    with open(f"./data/{user}_materials.csv", "r", encoding="utf-8") as f:
        existing_materials = [l.strip("\n") for l in f.readlines()]
        title = existing_materials[0]
        old_materials = existing_materials[1:]
    materials_sorted = old_materials + [new_material_line]
    materials_sorted.sort()
    new_materials = [title] + materials_sorted
    with open(f"./data/{user}_materials.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_materials))

def get_translte_word(user, not_reverse, dict, word):
    print(user, bool(int(not_reverse)), dict, word)
    with open(f"./data/{user}_{dict}.csv", "r", encoding="utf-8") as f:
        if bool(int(not_reverse)):
            for line in f.readlines()[1:]:
                if line.split(',')[0] == word:
                    return line.split(',')[1]
        else:
            print('jkb')
            for line in f.readlines()[1:]:
                if line.split(',')[1][:-1] == word:
                    return line.split(',')[0]
        return 'Такое слово не найдено'

def get_lessons(user):
    lessons = []
    with open(f"./data/{user}_lessons.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            date, thems, est = line.split(";")
            lessons.append([date, thems, est])
    return lessons

def get_materials(user):
    materials = []
    with open(f"./data/{user}_materials.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            name, link, est = line.split(";")
            materials.append([name, link, est])
    return materials




