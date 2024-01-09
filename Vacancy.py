class Vacancy:
    def __init__(self, name, url, salary, description, city=None):
        self.name = name
        self.salary = salary
        self.url = url
        self.city = city
        self.description = description
        if salary != "Не указано":
            splited_salary = salary.split()
            if len(splited_salary) == 2:
                self.__average_salary = int(splited_salary[0])
            else:
                self.__average_salary = (int(splited_salary[0]) + int(splited_salary[2])) / 2
        else:
            self.__average_salary = 0

    def __eq__(self, other):
        return self.__average_salary == other.__average_salary

    def __lt__(self, other):
        return self.__average_salary < other.__average_salary

    def __le__(self, other):
        return self.__average_salary <= other.__average_salary

    def __gt__(self, other):
        return self.__average_salary > other.__average_salary

    def __ge__(self, other):
        return self.__average_salary >= other.__average_salary
