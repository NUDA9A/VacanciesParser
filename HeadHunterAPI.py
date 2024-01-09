from API import Api
import requests
from JSONSaver import JSONSaver
from Vacancy import Vacancy


class HeadHunterAPI(Api):
    def __init__(self):
        self.url = "https://api.hh.ru/"

    def get_vacancies(self, search_text):
        headers = {
            "HH-User-Agent": "Vacancies_Parse"
        }

        params = {
            "per_page": 100,
            "area": 113,
            "text": search_text
        }

        req = requests.get(self.url + "vacancies", headers=headers, params=params)

        if req.status_code == 200:
            data = req.json()
            vacancies = []
            json_saver = JSONSaver()
            for parsed_vacancy in data['items']:
                if parsed_vacancy['salary']:
                    salary_from = parsed_vacancy['salary'].get('from', None)
                    salary_to = str(parsed_vacancy['salary'].get('to', None))
                    salary_currency = parsed_vacancy['salary'].get('currency')
                    if str(salary_from).isnumeric() and str(salary_to).isnumeric():
                        salary = str(salary_from) + " - " + str(salary_to) + " " + salary_currency
                    elif str(salary_from).isnumeric() and not str(salary_to).isnumeric():
                        salary = str(salary_from) + " " + salary_currency
                    elif str(salary_to).isnumeric() and not str(salary_from).isnumeric():
                        salary = str(salary_to) + " " + salary_currency
                else:
                    salary_from = None
                    salary_to = None
                    salary_currency = None
                    salary = "Не указано"
                if parsed_vacancy['snippet']['requirement']:
                    requirements = parsed_vacancy['snippet']['requirement']
                else:
                    requirements = "Не указано"
                vacancy = {
                    "title": parsed_vacancy.get('name'),
                    "city": parsed_vacancy['area'].get('name'),
                    "salary": salary,
                    "url": parsed_vacancy.get('alternate_url'),
                    "description": "Требования: " + requirements
                }
                vacancies.append(vacancy)
                curr_vacancy = Vacancy(vacancy['title'],
                                       vacancy['url'],
                                       vacancy['salary'],
                                       vacancy['description'],
                                       vacancy['city'])
                json_saver.add_vacancy(curr_vacancy)
            return vacancies
        else:
            print(f"Не удалось получить список вакансий. Код ошибки: {req.status_code}")
        req.close()
