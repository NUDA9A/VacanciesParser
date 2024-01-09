import json


class JSONSaver:
    file_path = "vacancies.json"

    def add_vacancy(self, vacancy):
        json_vacancy = {
            "name": vacancy.name,
            "city": vacancy.city,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }
        with open(self.file_path, 'r+', encoding="UTF-8") as file:
            line = file.readline()
            if len(line) == 0:
                file.write('[]')
        with open(self.file_path, 'r', encoding="UTF-8") as file:
            data = json.load(file)

        data.append(json_vacancy)

        with open(self.file_path, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_vacancies_by_salary(self, salary):
        print(f"Vacancies with {salary} salary")
        with open(self.file_path, 'r', encoding="UTF-8") as file:
            data = json.load(file)
        for vacancy in data:
            if vacancy.get('salary').split()[0] == salary.split()[0]:
                print(f"Title: {vacancy.get('name')}, url: {vacancy.get('url')}, salary: {vacancy.get('salary')}")

    def delete_vacancy(self, vacancy):
        vacancy_id = vacancy.url.split('/')[-1]
        with open(self.file_path, 'r+', encoding="UTF-8") as file:
            line = file.readline()
            if len(line) == 0:
                file.write('[]')
                return

        with open(self.file_path, 'r', encoding="UTF-8") as file:
            data = json.load(file)

        new_data = []

        for vacancies in data:
            if vacancies.get('url').split('/')[-1] != vacancy_id:
                new_data.append(vacancies)

        with open(self.file_path, 'w', encoding="UTF-8") as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)
