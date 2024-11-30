from app.model import Task, ValidTask
from app.task_manager import TaskManager

manager = TaskManager()
valid = ValidTask()


def prompt_user_input(prompt: str, exit_keyword: str = 'МЕНЮ') -> bool | str:
    """Универсальная функция для ввода с проверкой."""
    while True:
        user_input = input(prompt)
        if user_input == exit_keyword:
            return False
        if user_input:
            return user_input
        print('Поле не может быть пустым!')


def manager_add_task():
    """Функция добавления новой задачи."""
    print('Добавление новой задачи')

    task_val = {
        'title': 'Название задачи: ',
        'description': 'Описание задачи: ',
        'category': 'Категория: ',
    }
    while True:
        try:
            # Ввод title, description, category
            for key, value in task_val.items():
                val = prompt_user_input(value)
                if not val: # Выход
                    break
                task_val[key] = val
            else:
                due_date = get_date()
                if not due_date: # Выход
                    break

                priority = get_priority()
                if not priority: # Выход
                    break

                task = manager.add_task(
                    title=task_val['title'],
                    description=task_val['description'],
                    category=task_val['category'],
                    due_date=due_date,
                    priority=priority
                )
                print(f'Задача успешна создана!\n{task}')
            break
        except Exception as e:
            print(f'Ошибка при добавлении задачи: {e}')


def manager_delete_task():
    """Функция удаления задачи(Task)."""
    while True:
        id_task = get_id_task() # Получаем ID
        if not id_task:  # Выход в меню
            return

        task_info = manager.get_task_by_id(id_task)
        if not task_info:
            print('Задача не найдена!')
            continue

        you_sure = input(f'Вы уверены, что хотите удалить задачу: "{task_info}"? (Да/Нет)\n').lower()
        if you_sure == 'да':
            task = manager.delete_task(task_id=id_task)
            print(f'Задача "{task}" была успешно удалена!')
            break
        elif you_sure == 'нет':
            print('Удаление отменено.')
            break
        else:
            print('Введите "Да" или "Нет".')


def manager_update_status():
    """ Функция изменения статуса в задаче(Task)"""
    while True:
        id_task = get_id_task() # Получаем ID
        if not id_task:  # Выход в меню
            return

        task_info = manager.get_task_by_id(id_task)
        if not task_info:
            print('Задача не найдена!')
            continue

        task = manager.update_status_task(id_task)
        status = task.status
        print(f'\nЗадача "{task}"\nбыла успешно {status}!')
        break


def manager_display_task_category() -> None | bool | str:
    """ Функция показа задач(Task) по категориям. """
    while True:
        category = prompt_user_input('Напишите категорию: ')
        if not category:  # Выход в меню
            return

        answer = manager.display_tasks_category(category)

        if answer:
            return category
        else:
            print('\nИзвините категория пуста')
            break


def manager_remove_category():
    """ Функция удаление всей категории с задачами. """
    while True:
        category = manager_display_task_category() # Получаем категорию и вывод всех ее задач
        if not category:  # Выход в меню
            return

        you_sure = input('Вы уверены что хотите удалить все эти задачи и категорию?(Да/Нет)\n').lower()
        if you_sure == 'да':
            manager.delete_task_category(category.capitalize())
            print(f'Задачи "{category}" были успешно удалены!')
            break
        elif you_sure == 'нет':
            print('Удаление отменено.')
            break
        else:
            print('Введите "Да" или "Нет".')


def get_updated_task_values(task: Task) -> dict | None:
    """Получение обновленных значений для задачи."""
    updated_values = {}
    fields = ['title', 'description', 'category', 'due_date', 'priority']

    print('\nТекущие значения задачи:')
    print(task)

    for field in fields:
        prompt_message = f'Новое {field} (или нажмите Enter для пропуска): '
        new_value = input(prompt_message).strip()

        if new_value == 'МЕНЮ':  # Выход в меню
            return

        while True:  # Проверка валидности значений
            try:
                if field == 'due_date' and new_value:
                    valid.valid_date(new_value)
                    break
                elif field == 'priority' and new_value:
                    valid.valid_priority(new_value)
                    break
                else:
                    break
            except Exception as e:
                print(f'\nОшибка неверные данные:{e}')
                prompt_message = f'Новое {field} (или нажмите Enter для пропуска): '
                new_value = input(prompt_message).strip()

        if new_value:  # Если введено новое значение, добавляем в словарь
            updated_values[field] = new_value

    return updated_values


def manager_update_task():
    """Функция обновления задачи."""
    while True:
        task_id = get_id_task()  # Получение ID задачи для обновления
        if not task_id:  # Выход в меню
            return

        task = manager.get_task_by_id(task_id)  # Получение экземпляра задачи
        updated_values = get_updated_task_values(task)  # Получение обновленных значений

        if updated_values is None:  # Выход в меню
            return

        try:
            # Обновление задачи с учетом новых значений, если они предоставлены
            manager.update_task(
                task_id,
                title=updated_values.get('title', task.title),
                description=updated_values.get('description', task.description),
                category=updated_values.get('category', task.category),
                due_date=updated_values.get('due_date', task.due_date),
                priority=updated_values.get('priority', task.priority)
            )
            print('\nЗадача успешно обновлена!')
            break  # Выход из цикла после успешного обновления
        except Exception as e:
            print(f'\nОшибка при изменении задачи: {str(e)}.')


def manager_search_task():
    """Функция поиска задач по ключевым словам, категории и статусу."""
    print('Введите параметры для поиска задач:')
    keyword = input('Введите ключевое слово (или нажмите Enter для пропуска): ')
    category = input('Введите категорию (или нажмите Enter для пропуска): ')
    status = input('Cтатус задачи?(Выполнено/Не выполнено) (или нажмите Enter для пропуска): ')

    result = manager.search_tasks(keyword, category, status)
    if not result:
        print('\nИзвините, ничего не найдено. ')


def get_id_task() -> int | None:
    """Функция ввода id и проверки корректности id."""
    while True:
        input_id_task = input('Напишите индекс (номер) задачи:\n')

        if input_id_task.upper() == 'МЕНЮ':  # Выход в меню
            return

        if not input_id_task.isdigit():
            print(f'Неверно указан индекс! "{input_id_task}" не является числом!')
            continue

        id_task = int(input_id_task)  # Преобразовать к int после проверки

        # Проверка наличия задачи
        if manager.get_task_by_id(id_task):
            return id_task  # Вернуть ID задачи

        print(f'Индекс {input_id_task} отсутствует у нас в списках.\n'
              'Попробуйте ввести другой индекс и/или проверьте его в списках.')


def get_date() -> str | None:
    """Функция получения валидного значения 'due_date'."""
    while True:
        try:
            due_date = input('Срок выполнения (дд.мм.гггг): ')

            if not due_date:
                print('Поле не может быть пустым!')
                continue

            if due_date == 'МЕНЮ':  # Выход в меню
                return

            # Проверка даты
            if valid.valid_date(due_date):
                return due_date

        except Exception:
            print('\nДата указана неверно!\n'
                  'Дата должна быть с сегодняшнего дня по будущее и в формате "день.месяц.год".\n')


def get_priority() -> str | None:
    """Функция получения валидного значения 'priority'."""
    priority_val = {'1': 'низкий', '2': 'средний', '3': 'высокий'}

    while True:
        try:
            priority_input = input('Приоритет ((1)низкий, (2)средний, (3)высокий): ')

            if not priority_input:
                print('Поле не может быть пустым!')
                continue

            if priority_input == 'МЕНЮ':  # Выход в меню
                return

            # Проверка, если введено число
            if priority_input in priority_val:
                return priority_val[priority_input]

            # Проверка для текстового ввода
            if valid.valid_priority(priority_input):
                return priority_input

        except Exception:
            print('\nПриоритет указан неверно!\n'
                  'Приоритет может быть только "низкий", "средний", "высокий" или указан в виде числа от 1 до 3.\n')
