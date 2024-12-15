users = []

instruments = [
    {'name': 'Гитара1', 'price': 15000, 'stock': 10, 'color': 'Красный', 'category': 'Гитара'},
    {'name': 'Пианино1', 'price': 50000, 'stock': 5, 'color': 'Черный', 'category': 'Пианино'},
    {'name': 'Ударная установка1', 'price': 35000, 'stock': 3, 'color': 'Синий', 'category': 'Ударные'},
    {'name': 'Синтезатор1', 'price': 20000, 'stock': 8, 'color': 'Белый', 'category': 'Синтезатор'},
    {'name': 'Гитара2', 'price': 30000, 'stock': 15, 'color': 'Зелёный', 'category': 'Гитара'}
]

current_user = None

purchase_history = {}

def register(username, password, role):
    if any(user['username'] == username for user in users):
        print("Пользователь с таким именем уже существует\n")
        return
    users.append({'username': username, 'password': password, 'role': role})
    purchase_history[username] = []  
    print("Пользователь успешно зарегистрирован\n")

def login(username, password):
    global current_user
    for user in users:
        if user['username'] == username and user['password'] == password:
            current_user = user
            print("Успешный вход в систему\n")
            return
    print("Неверное имя пользователя или пароль\n")

def admin_add_instrument(name, price, stock, color, category):
    if not isinstance(color, str) or not isinstance(category, str):
        print("Некорректный ввод. Цвет и категория должны быть строками\n")
        return
    instruments.append({'name': name, 'price': price, 'stock': stock, 'color': color, 'category': category})
    print("Инструмент успешно добавлен\n")

def admin_remove_instrument(name):
    global instruments
    for instrument in instruments:
        if instrument['name'].lower() == name.lower():  
            instruments.remove(instrument)
            print("Инструмент успешно удален\n")
            return
    print("Инструмент не найден\n")

def filter_instruments(instruments, category=None, color=None, price_range=None):
    if category:
        instruments = list(filter(lambda x: category.lower() in x['category'].lower(), instruments))
    if color:
        instruments = list(filter(lambda x: color.lower() in x['color'].lower(), instruments))
    if price_range:
        min_price, max_price = price_range
        instruments = list(filter(lambda x: min_price <= x['price'] <= max_price, instruments))
    return instruments

def sort_instruments(instruments, reverse=False):
    return sorted(instruments, key=lambda x: x['price'], reverse=reverse)  

def view_instruments(category=None, color=None, price_range=None, reverse=False):
    filtered_instruments = filter_instruments(instruments, category, color, price_range)
    sorted_instruments = sort_instruments(filtered_instruments, reverse)

    print("Список инструментов:\n")
    if sorted_instruments:
        for instrument in sorted_instruments:
            print(f"{instrument['name']} - {instrument['price']} (в наличии: {instrument['stock']}, цвет: {instrument['color']}, категория: {instrument['category']})")
    else:
        print("Инструменты не найдены\n")

def buy_instrument(name):
    for instrument in instruments:
        if instrument['name'].lower() == name.lower(): 
            if instrument['stock'] > 0:
                instrument['stock'] -= 1
                purchase_history[current_user['username']].append(instrument)
                print(f"Вы купили {instrument['name']}. Осталось в наличии: {instrument['stock']}\n")
            else:
                print("Извините, инструмент отсутствует на складе\n")
            return
    print("Инструмент не найден\n")

def search_instrument(name):
    for instrument in instruments:
        if instrument['name'].lower() == name.lower():  
            print(f"Найден инструмент: {instrument['name']} - {instrument['price']} (в наличии: {instrument['stock']}, цвет: {instrument['color']}, категория: {instrument['category']})\n")
            return
    print("Инструмент не найден\n")

def get_price_range():
    while True:
        price_filter = input("Введите диапазон цен (например, 10000-50000) или оставьте пустым для всех: ")
        if price_filter == "":
            return None
        try:
            min_price, max_price = map(float, price_filter.split('-'))
            return (min_price, max_price)
        except ValueError:
            print("Некорректный ввод. Попробуйте снова\n")

def view_purchase_history():
    username = current_user['username']
    if purchase_history[username]:
        print("История покупок:\n")
        for item in purchase_history[username]:
            print(f"{item['name']} - {item['price']} (цвет: {item['color']}, категория: {item['category']})\n")
    else:
        print("Вы пока ничего не купили\n")

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Некорректный ввод. Пожалуйста, выберите один из следующих вариантов: {', '.join(valid_options)}\n")

def main_menu():
    global current_user
    while True:
        if current_user is None:
            action = get_valid_input("\nВыберите действие:\n1.Вход\n2.Регистрация\n0.Выход\n ", ['1', '2', '0'])
            if action == '1':
                username = input("Имя пользователя: ")
                password = input("Пароль: ")
                login(username, password)
            elif action == '2':
                username = input("Имя пользователя: ")
                password = input("Пароль: ")
                role = get_valid_input("Роль (юзер/админ): ", ['юзер', 'админ'])
                register(username, password, role)
            elif action == '0':
                break
        else:
            if current_user['role'] == 'админ':
                action = get_valid_input("\nВыберите действие:\n1.Добавить инструмент\n2.Удалить инструмент\n3.Просмотреть инструменты\n4.Просмотреть пользователей\n0.Выйти\n", ['1', '2', '3', '4', '0'])
                if action == '1':
                    name = input("Название инструмента: ")
                    try:
                        price = float(input("Цена: "))
                        stock = int(input("Количество: "))
                        color = input("Цвет инструмента: ").strip()  
                        category = input("Категория инструмента (например, гитара, пианино): ").strip() 
                        if price < 0 or stock < 0:
                            print("Цена и количество должны быть неотрицательными\n")
                            continue
                        admin_add_instrument(name, price, stock, color, category)
                    except ValueError:
                        print("Некорректный ввод\n")
                elif action == '2':
                    while True:
                        name = input("Название инструмента для удаления: ")
                        if any(instrument['name'].lower() == name.lower() for instrument in instruments):
                            admin_remove_instrument(name)
                            break
                        else:
                            print("Инструмент не найден. Попробуйте снова\n")
                elif action == '3':
                    while True:
                        try:
                            category_filter = input("Введите категорию для фильтрации (или оставьте пустым для всех): ")
                            color_filter = input("Введите цвет для фильтрации (или оставьте пустым для всех): ")
                            price_range = get_price_range()
                            sort_order = get_valid_input("Сортировать по цене?\n1.по возрастанию\n2.по убыванию\n0.без сортировки\n ", ['1', '2', '0'])
                            reverse = sort_order == '2'
                            view_instruments(category=category_filter, color=color_filter, price_range=price_range, reverse=reverse)
                            break
                        except Exception as e:
                            print("Произошла ошибка\n ", str(e))
                            print("Попробуйте снова\n")
                elif action == '4':
                    print("Список пользователей:\n")
                    for user in users:
                        print(f"{user['username']} - {user['role']}\n")
                elif action == '0':
                    current_user = None  
                else:
                    print("Некорректный ввод.\n")
            else:
                action = get_valid_input("Выберите действие:\n1.Просмотреть инструменты\n2.Купить инструмент\n3.Поиск инструмента\n4.Просмотреть историю покупок\n0.Выйти\n ", ['1', '2', '3', '4', '0'])
                if action == '1':
                    while True:
                        try:
                            category_filter = input("Введите категорию для фильтрации (или оставьте пустым для всех):\n ")
                            color_filter = input("Введите цвет для фильтрации (или оставьте пустым для всех):\n ")
                            price_range = get_price_range()
                            sort_order = get_valid_input("Сортировать по цене?\n1.по возрастанию\n2.по убыванию\n0.без сортировки\n ", ['1', '2', '0'])
                            reverse = sort_order == '2'
                            view_instruments(category=category_filter, color=color_filter, price_range=price_range, reverse=reverse)
                            break
                        except Exception as e:
                            print("Произошла ошибка\n ", str(e))
                            print("Попробуйте снова\n")
                elif action == '2':
                    name = input("Введите название инструмента для покупки: ")
                    buy_instrument(name)
                elif action == '3':
                    search_name = input("Введите название инструмента для поиска: ")
                    search_instrument(search_name)
                elif action == '4':
                    view_purchase_history()
                elif action == '0':
                    current_user = None 
                else:
                    print("Некорректный ввод. Пожалуйста, попробуйте снова\n")

if __name__ == "__main__":
    main_menu()
