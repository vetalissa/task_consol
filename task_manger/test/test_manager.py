import json
import os

import pytest

from app.task_manager import TaskManager


class TestTaskManager:
    @pytest.fixture
    def task_manager(self):
        filename = 'test_data.json'
        manager = TaskManager('test_data.json')

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
        yield manager

        # Удаляем файл после тестов
        if os.path.exists(filename):
            os.remove(filename)

    def test_add_task(self, task_manager):
        task = task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        assert task.title == 'Название'
        assert task.description == 'Описание'
        assert task.due_date == '12.12.2028'
        assert task.category == 'Работа'
        assert task.priority == 'Высокий'
        assert task.status == 'Не выполнена'
        assert task.id == 1

    def test_load_tasks(self, task_manager):
        task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        task_manager2 = TaskManager('test_data.json')  # Новый экземпляр, чтобы загрузить задачи
        loaded_tasks = task_manager2.tasks
        assert len(loaded_tasks) == 1
        assert loaded_tasks[0].title == 'Название'

    def test_delete_task(self, task_manager):
        task = task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        assert len(task_manager.tasks) == 1
        deleted_task = task_manager.delete_task(task.id)
        assert deleted_task.id == task.id
        assert len(task_manager.tasks) == 0

    def test_update_task_status(self, task_manager):
        task = task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        updated_task = task_manager.update_status_task(task.id)
        assert updated_task.status == 'Выполнена'

    def test_update_task(self, task_manager):
        task = task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        task_manager.update_task(task.id, title='Новое название', description='Новое описание')
        updated_task = task_manager.get_task_by_id(task.id)
        assert updated_task.title == 'Новое название'
        assert updated_task.description == 'Новое описание'

    def test_delete_task_category(self, task_manager):
        task_manager.add_task('Название 1', 'Описание 1', '12.12.2028', 'Работа', 'Высокий')
        task_manager.add_task('Название 2', 'Описание 2', '12.12.2028', 'Личное', 'Низкий')

        task_manager.delete_task_category('Работа')
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0].category == 'Личное'

    def test_search_tasks(self, task_manager):
        task_manager.add_task('Название 1', 'Описание 1', '12.12.2028', 'Работа', 'Высокий')
        task_manager.add_task('Название 2', 'Описание 2', '12.12.2028', 'Личное', 'Низкий')

        search_results = task_manager.search_tasks(keyword='Название ')
        assert search_results is True

        no_search_results = task_manager.search_tasks(keyword='pop')
        assert no_search_results is None

    def test_display_tasks(self, task_manager, capsys):
        task_manager.add_task('Название', 'Описание', '12.12.2028', 'Работа', 'Высокий')
        task_manager.display_tasks()
        captured = capsys.readouterr()
        assert 'Название' in captured.out
