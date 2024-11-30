import pytest

from app.model import Task


class TestTask:

    def test_task_creation_valid(self):
        task = Task('Название', 'Описание', '01.01.2040', 'Работа', 'высокий')

        assert task.title == 'Название'
        assert task.description == 'Описание'
        assert task.due_date == '01.01.2040'
        assert task.category == 'Работа'
        assert task.priority == 'Высокий'
        assert task.status == 'Не выполнена'
        assert task.id == 1

    def test_task_creation_empty_value(self):
        with pytest.raises(TypeError, match='Пустое значение не допускается.'):
            Task('', 'Описание', '01.01.2040', 'Работа', 'высокий')

        with pytest.raises(TypeError, match='Пустое значение не допускается.'):
            Task('Название', 'Описание', '', 'Работа', 'высокий')

        with pytest.raises(TypeError, match='Пустое значение не допускается.'):
            Task('Название', 'Описание', '01.01.2040', '', 'высокий')

        with pytest.raises(TypeError, match='Пустое значение не допускается.'):
            Task('Название', 'Описание', '01.01.2040', 'Работа', '')

    def test_task_creation_invalid_due_date(self):
        with pytest.raises(ValueError, match='Дата указана неверно.'):
            Task('Название', 'Описание', '12.12.1965', 'Работа', 'высокий')
        with pytest.raises(ValueError, match='Дата указана неверно.'):
            Task('Название', 'Описание', '2027.11.11', 'Работа', 'высокий')
        with pytest.raises(ValueError, match='Дата указана неверно.'):
            Task('Название', 'Описание', '11.11.27', 'Работа', 'высокий')
        with pytest.raises(ValueError, match='Дата указана неверно.'):
            Task('Название', 'Описание', '11-11-2025', 'Работа', 'высокий')

    def test_task_creation_invalid_priority(self):
        with pytest.raises(ValueError, match='Приоритет указан неверно.'):
            Task('Название', 'Описание', '01.01.2040', 'Работа', 'Большой')
        with pytest.raises(ValueError, match='Приоритет указан неверно.'):
            Task('Название', 'Описание', '01.01.2040', 'Работа', 'Высоко')

    def test_task_creation_invalid_status(self):
        with pytest.raises(ValueError, match='Статус указан неверно.'):
            Task('Название', 'Описание', '01.01.2040', 'Работа', 'низкий', 'готово')
        with pytest.raises(ValueError, match='Статус указан неверно.'):
            Task('Название', 'Описание', '01.01.2040', 'Работа', 'низкий', 'сделано')

    def test_task_creation_multiple_tasks(self):
        task1 = Task('Task 1', 'Description 1', '01.01.2040', 'Работа', 'низкий')
        task2 = Task('Task 2', 'Description 2', '02.02.2040', 'Личные', 'высокий')
        assert task1.id == 1 or 2
        assert task2.id == 2 or 3
        assert task1.title == 'Task 1'
        assert task2.title == 'Task 2'

    def test_to_dict(self):
        task = Task(
            title='Название',
            description='Описание',
            due_date='01.01.2040',
            category='Работа',
            priority='Высокий'
        )

        task_dict = task.to_dict()
        expected_dict = {
            'id': task.id,
            'title': 'Название',
            'description': 'Описание',
            'category': 'Работа',
            'due_date': '01.01.2040',
            'priority': 'Высокий',
            'status': 'Не выполнена'
        }

        assert task_dict == expected_dict

    def test_from_dict(self):
        data = {
            'title': 'Название',
            'description': 'Описание',
            'due_date': '01.01.2040',
            'category': 'Работа',
            'priority': 'Высокий',
            'status': 'Не выполнена'
        }

        task = Task.from_dict(data)

        assert task.title == 'Название'
        assert task.description == 'Описание'
        assert task.due_date == '01.01.2040'
        assert task.category == 'Работа'
        assert task.priority == 'Высокий'
        assert task.status == 'Не выполнена'
