from API import Api
import requests

from JSONSaver import JSONSaver
from Vacancy import Vacancy


class SuperJobAPI(Api):
    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/"
        self.__key = "v3.r.128417607.2c7bec3e653621849a005aea2b418ad22ee8015f.ce3b2601d76af39e503e24cbc672b31386fdda2e"

    def get_vacancies(self, search_text):
        headers = {
            'X-Api-App-Id': self.__key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'keywords': search_text,
            'count': 100,
            'page': 0
        }
        req = requests.get(self.url + "vacancies", params=params, headers=headers)
        if req.status_code == 200:
            data = req.json()
            vacancies = []
            json_saver = JSONSaver()
            for parsed_vacancy in data['objects']:
                if parsed_vacancy['payment_from'] != 0 and parsed_vacancy['payment_to'] != 0:
                    salary = str(parsed_vacancy['payment_from']) + " - " + str(parsed_vacancy['payment_to']) + " " + parsed_vacancy['currency']
                elif parsed_vacancy['payment_from'] != 0 and parsed_vacancy['payment_to'] == 0:
                    salary = str(parsed_vacancy['payment_from']) + " " + parsed_vacancy['currency']
                elif parsed_vacancy['payment_from'] == 0 and parsed_vacancy['payment_to'] != 0:
                    salary = str(parsed_vacancy['payment_to']) + " " + parsed_vacancy['currency']
                else:
                    salary = "Не указано"
                requirements = parsed_vacancy['candidat']
                name = parsed_vacancy['profession']
                city = parsed_vacancy['address']
                url = parsed_vacancy['link']
                vacancy = {
                    'title': name,
                    'city': city,
                    'salary': salary,
                    'url': url,
                    'description': requirements
                }
                curr_vacancy = Vacancy(vacancy['title'],
                                       vacancy['url'],
                                       vacancy['salary'],
                                       vacancy['description'],
                                       vacancy['city'])
                vacancies.append(curr_vacancy)
                json_saver.add_vacancy(curr_vacancy)
            return vacancies
        else:
            print(f"Не удалось получить список вакансий. Код ошибки: {req.status_code}")
        req.close()
