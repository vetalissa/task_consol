from app import view


def start():
    command = '''Список команд:
        Добавить новую задачу: "1"
        Список всех задач: "2"
        Список всех задач определенной категории: "3"
        Удалить одну задачу: "4"
        Удалить всю категорию и все задачи в ней: "5"
        Изменить статус задачи: "6"
        Изменить данные задачи: "7"
        Найти задачи: "8"
        Для выхода в главное меню напишите: "МЕНЮ" обязательно капсом!
        Для выхода из приложения напишите: "ВЫХОД" обязательно капсом!'''

    while True:
        print('_' * 100)
        print(command)
        print('_' * 100)
        command_text = input("Введите команду: ")
        while True:

            if command_text.lower() == '1':
                view.manager_add_task()
                break
            elif command_text.lower() == '2':
                view.manager.display_tasks()
                break
            elif command_text.lower() == '3':
                view.manager_display_task_category()
                break
            elif command_text.lower() == '4':
                view.manager_delete_task()
                break
            elif command_text.lower() == '5':
                view.manager_remove_category()
                break
            elif command_text.lower() == '6':
                view.manager_update_status()
                break
            elif command_text.lower() == '7':
                view.manager_update_task()
                break
            elif command_text.lower() == '8':
                view.manager_search_task()
                break
            elif command_text in ('МЕНЮ', 'ВЫХОД'):
                print('\n' * 50)
                break

            else:
                print("Такой команды не существует.")
                break

        if command_text == 'ВЫХОД':
            # Команда для выхода и закрытия приложения

            answer = input('Вы уверены что хотите выйти из Библиотеки?(ДА/НЕТ)')
            if answer == 'ДА':
                print('До свидания!')
                break


if __name__ == "__main__":
    start()

# import json
# from app.model import Task
# from app.task_manager import TaskManager
#
#
# def display_menu():
#     print("\n=== Управление задачами ===")
#     print("1. Добавить задачу")
#     print("2. Просмотреть все задачи")
#     print("3. Обновить задачу")
#     print("4. Удалить задачу")
#     print("5. Поиск задач")
#     print("6. Обновить статус задачи")
#     print("7. Удалить задачи по категории")
#     print("0. Выход")
#
#
# def main():
#     task_manager = TaskManager()
#
#     while True:
#         display_menu()
#         choice = input("Выберите действие: ")
#
#         if choice == '1':
#             title = input("Введите заголовок задачи: ")
#             description = input("Введите описание задачи: ")
#             due_date = input("Введите дату выполнения (гггг-мм-дд): ")
#             category = input("Введите категорию: ")
#             priority = input("Введите приоритет: ")
#             task_manager.add_task(title, description, due_date, category, priority)
#             print("Задача добавлена.")
#
#         elif choice == '2':
#             task_manager.display_tasks()
#
#         elif choice == '3':
#             task_id = int(input("Введите ID задачи для обновления: "))
#             title = input("Введите новый заголовок (или оставьте пустым для пропуска): ")
#             description = input("Введите новое описание (или оставьте пустым для пропуска): ")
#             category = input("Введите новую категорию (или оставьте пустым для пропуска): ")
#             due_date = input("Введите новую дату (или оставьте пустым для пропуска): ")
#             priority = input("Введите новый приоритет (или оставьте пустым для пропуска): ")
#             task_manager.update_task(task_id, title or None, description or None, category or None, due_date or None,
#                                      priority or None)
#             print("Задача обновлена.")
#
#         elif choice == '4':
#             task_id = int(input("Введите ID задачи для удаления: "))
#             try:
#                 task_manager.delete_task(task_id)
#                 print("Задача удалена.")
#             except KeyError as e:
#                 print(e)
#
#         elif choice == '5':
#             keyword = input("Введите ключевое слово для поиска (или оставьте пустым для пропуска): ")
#             category = input("Введите категорию для поиска (или оставьте пустым для пропуска): ")
#             status = input("Введите статус для поиска (или оставьте пустым для пропуска): ")
#             results = task_manager.search_tasks(keyword or None, category or None, status or None)
#             if results:
#                 print("\nНайденные задачи:")
#                 for task in results:
#                     print(task)
#             else:
#                 print("Задачи не найдены.")
#
#         elif choice == '6':
#             task_id = int(input("Введите ID задачи для обновления статуса: "))
#             try:
#                 updated_task = task_manager.update_status_task(task_id)
#                 print(f"Статус задачи обновлен на: {updated_task.status}")
#             except KeyError as e:
#                 print(e)
#
#         elif choice == '7':
#             category = input("Введите категорию задач для удаления: ")
#             task_manager.delete_task_category(category)
#             print(f"Все задачи в категории '{category}' удалены.")
#
#         elif choice == '0':
#             print("Выход...")
#             break
#
#         else:
#             print("Неверный выбор. Пожалуйста, попробуйте снова.")
#
#
# if __name__ == '__main__':
#     main()
