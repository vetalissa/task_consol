import json

from app.model import Task


class TaskManager:
    """Класс для управления задачами."""

    def __init__(self, filename='json_data/data.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.categories = set()

    def load_tasks(self) -> list[Task]:
        """Загрузка задач из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Task.from_dict(task_data) for task_data in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Ошибка загрузки задач: {e}')
            return []

    def save_tasks(self) -> None:
        """Сохранение задач в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, due_date: str, category: str, priority: str,
                 status: str = 'Не выполнена') -> Task:
        """Добавление задачи."""
        new_task = Task(title, description, due_date, category, priority, status)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def delete_task(self, task_id: int) -> Task:
        """Удаление задачи по ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return task
        else:
            raise KeyError('Такого индекса не существует.')

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Поиск задачи по ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def delete_task_category(self, category: str) -> None:
        """Удаление всех задач в указанной категории."""
        self.tasks = [task for task in self.tasks if task.category.lower() != category.lower()]
        self.save_tasks()

    def update_status_task(self, task_id: int) -> Task:
        """Обновление статуса задачи."""
        task = self.get_task_by_id(task_id)

        if task:
            task.status = 'Выполнена' if task.status == 'Не выполнена' else 'Не выполнена'
            self.save_tasks()
            return task
        else:
            raise KeyError('Такого индекса не существует.')

    def update_task(self, task_id: int, title: str = None, description: str = None,
                    category: str = None, due_date: str = None, priority: str = None) -> None:
        """Обновление данных задачи."""
        task = self.get_task_by_id(task_id)

        if not task:
            raise KeyError('Такого индекса не существует.')

        if title:
            task.title = title.capitalize()
        if description:
            task.description = description
        if category:
            task.category = category.capitalize()
        if due_date:
            task.due_date = due_date
        if priority:
            task.priority = priority.capitalize()

        self.save_tasks()

    def search_tasks(self, keyword: str = None, category: str = None, status: str = None) -> None | bool:
        """Поиск задач по ключевому слову, категории и статусу."""
        results = [
            task for task in self.tasks if
            (keyword and (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower())) or
            (category and category.lower() == task.category.lower()) or
            (status and status.lower() == task.status.lower())
        ]

        if not results:
            return None

        for task in results:
            print(task)
        return True

    def display_tasks(self) -> None:
        """Вывод всех задач."""
        for task in self.tasks:
            print(task)

    def display_tasks_category(self, category: str):
        """Вывод всех задач в заданной категории."""
        category = category.capitalize()
        list_tasks = [task for task in self.tasks if task.category == category]
        if list_tasks:
            for task in list_tasks:
                print(task)
            return True
        return False
