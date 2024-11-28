import requests
from colorama import Fore, Style, init

# Инициализация colorama для работы цветов на Windows
init(autoreset=True)

def check_beta_access(user_id: str, token: str) -> bool:
    """
    Проверяет, есть ли у пользователя доступ к бета-функции создания гильдий.

    :param user_id: Идентификатор пользователя Discord.
    :param token: Токен для авторизации (бота).
    :return: True, если доступ есть, иначе False.
    """
    url = f"https://discord.com/api/v10/users/{user_id}"  # URL для запроса
    headers = {
        "Authorization": f"Bot {token}",  # Используем токен бота для авторизации
        "Content-Type": "application/json",
    }
    
    print(f"{Fore.CYAN}[ + ] Отправляем запрос к Discord API...")
    
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            print(f"{Fore.RED}[ + ] Ошибка: Неверный токен или недостаточно прав для выполнения запроса.")
            return False
        elif not response.ok:
            print(f"{Fore.RED}[ + ] Ошибка запроса: {response.status_code} - {response.text}")
            return False

        data = response.json()
        # Логика проверки: доступ к бета-функции
        has_beta_access = "beta_flags" in data and data["beta_flags"] > 0
        return has_beta_access

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ + ] Ошибка запроса: {e}")
        return False

def main():
    """
    Основная функция программы. Запрашивает токен и ID пользователя, проверяет доступ к бета-функции.
    """
    print(f"{Fore.CYAN}[ + ] === Discord Beta Checker ===")
    
    # Запрашиваем токен у пользователя
    token = input(f"{Fore.CYAN}[ + ] Введите ваш Discord токен (бота): ").strip()

    if not token:
        print(f"{Fore.RED}[ + ] Ошибка: Токен не может быть пустым.")
        input(f"{Fore.CYAN}[ + ] Нажмите Enter для выхода.")
        return

    user_id = input(f"{Fore.CYAN}[ + ] Введите ID пользователя Discord для проверки: ").strip()

    if not user_id.isdigit():
        print(f"{Fore.RED}[ + ] Ошибка: ID пользователя должен быть числовым.")
        input(f"{Fore.CYAN}[ + ] Нажмите Enter для выхода.")
        return

    # Проверяем доступ к бета-функции
    has_access = check_beta_access(user_id, token)
    
    if has_access:
        print(f"{Fore.GREEN}[ + ] Удачно: Пользователь с ID {user_id} имеет доступ к бета-функции!")
    else:
        print(f"{Fore.RED}[ + ] Ошибка: У пользователя с ID {user_id} нет доступа к бета-функции.")
    
    input(f"{Fore.CYAN}[ + ] Нажмите Enter для выхода.")

if __name__ == "__main__":
    main()
