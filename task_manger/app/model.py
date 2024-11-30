from datetime import datetime


class ValidTask:
    """ Класс проверки значений для экземпляров класса Task. """

    @staticmethod
    def valid_values(value: str):
        """ Проверка на не пустое значение. """
        if not value:
            raise TypeError("Пустое значение не допускается.")
        return value

    def valid_date(self, value: str) -> str:
        """ Проверка даты на правильный формат и корректную дату. """
        self.valid_values(value)
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            value = f'{date.day:02d}.{date.month:02d}.{date.year}'

            if not (datetime.now() <= date):
                raise ValueError('Дата должна быть с сегодняшнего дня по будущее.')
        except ValueError:
            raise ValueError("Дата указана неверно.")
        except Exception:
            raise TypeError('Дата неверного формата!')
        return value

    def valid_priority(self, value: str) -> str:
        """ Проверка значения приоритета на корректность. """
        self.valid_values(value)

        if value.lower() not in ('низкий', 'средний', 'высокий'):
            raise ValueError("Приоритет указан неверно.")
        return value

    def valid_status(self, value: str) -> str:
        """ Проверка значения статуса на корректность. """
        self.valid_values(value)

        if value.lower() not in ('выполнена', 'не выполнена'):
            raise ValueError('Статус указан неверно.\nСтатус может быть только "выполнена", "не выполнена".')
        return value


class Task(ValidTask):
    """ Класс задач. """
    __ID = 0

    def __init__(self, title: str, description: str, due_date: str, category: str, priority: str,
                 status: str = 'Не выполнена'):
        self.title = title.capitalize()
        self.description = description
        self.due_date = due_date
        self.category = category.capitalize()
        self.priority = priority.capitalize()
        self.status = status.capitalize()

        Task.__ID += 1
        self.id = Task.__ID

    def __setattr__(self, key, value):
        if key == 'due_date':
            self.valid_date(value)
        elif key == 'priority':
            self.valid_priority(value)
        elif key == 'status':
            self.valid_status(value)
        elif key != 'id':
            self.valid_values(value)

        object.__setattr__(self, key, value)

    def to_dict(self) -> dict:
        """ Функция, создает словарь с атрибутами экземпляра. """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'due_date': self.due_date,
            'priority': self.priority,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: dict):
        task = Task(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            due_date=data['due_date'],
            priority=data['priority'],
            status=data['status'],
        )

        return task

    def __str__(self):
        status = "✓" if self.status == 'Выполнена' else "✗"
        return f"[{self.id}][{status}] {self.title} -- {self.description} | {self.due_date} | Категория: {self.category} | Приоритета: {self.priority}"
