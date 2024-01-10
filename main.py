# Создание экземпляра класса для работы с API сайтов с вакансиями
from HeadHunterAPI import HeadHunterAPI
from SuperJobAPI import SuperJobAPI
from Vacancy import Vacancy
from JSONSaver import JSONSaver


# Функция для взаимодействия с пользователем
def filter_vacancies(vacancies, filter_words):
    filtered_vacancies = []
    for vacancy in vacancies:
        for word in filter_words:
            if word in vacancy.name or word in vacancy.description:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(filtered_vacancies):
    return sorted(filtered_vacancies, reverse=True)


def get_top_vacancies(sorted_vacancies, top_n):
    if len(sorted_vacancies) <= top_n:
        return sorted_vacancies
    else:
        return sorted_vacancies[:top_n]


def print_vacancies(top_vacancies):
    n = 1
    for vacancy in top_vacancies:
        print(f"{n}. {vacancy}")
        n += 1


def user_interaction():
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()

    platforms = [hh_api, superjob_api]
    platform = -1
    while platform not in range(2):
        platform = int(input("Выберите площадку для поиска (Введите цифру 1 или 2):\n1. HeadHunter\n2. SuperJob\n")) - 1
        if platform != 0 and platform != 1:
            print("Нет такого варианта, попробуйте еще раз")
    curr_api = platforms[platform]
    search_query = input("Введите поисковый запрос: ")
    vacancies = curr_api.get_vacancies(search_query)
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
