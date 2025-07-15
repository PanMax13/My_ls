#!/usr/bin/env python3
import os
import sys
import argparse
import stat
import datetime

def list_dir(path, show_all=False, long_format=False):
    """
    Выводит содержимое директории.
    :param path: Путь к директории
    :param show_all: Показывать скрытые файлы (начинающиеся с '.')
    :param long_format: Показывать подробную информацию о файлах
    """
    try:
        entries = os.listdir(path)  # Получаем список файлов и папок в директории
    except Exception as e:
        print(f"Ошибка: {e}")      # Если не удалось открыть директорию — выводим ошибку
        return

    if not show_all:
        # Если не указан флаг -a, скрытые файлы (начинающиеся с .) не показываем
        entries = [e for e in entries if not e.startswith('.')]
    entries.sort()  # Сортируем по имени

    if long_format:
        # Длинный формат: выводим права, количество ссылок, размер, дату, имя
        for entry in entries:
            full_path = os.path.join(path, entry)  # Полный путь к файлу/папке
            try:
                st = os.stat(full_path)  # Получаем информацию о файле
                perms = stat.filemode(st.st_mode)  # Преобразуем режим в строку (например, -rw-r--r--)
                nlink = st.st_nlink  # Количество жёстких ссылок
                size = st.st_size    # Размер файла в байтах
                mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')  # Время последнего изменения
                print(f"{perms} {nlink:2} {size:8} {mtime} {entry}")  # Выводим информацию
            except Exception as e:
                print(f"Ошибка при получении информации о {entry}: {e}")  # Если не удалось получить инфо о файле
    else:
        # Краткий формат: просто имена файлов через два пробела
        print('  '.join(entries))

if __name__ == "__main__":
    # Создаём парсер аргументов командной строки с описанием программы
    parser = argparse.ArgumentParser(description="Аналог ls: выводит содержимое директории")
    # Добавляем позиционный аргумент 'directory' (путь к директории)
    # nargs="?" — аргумент необязательный
    # default="." — если не указано, используется текущая директория
    # help — текст для справки
    parser.add_argument("directory", nargs="?", default=".", help="Путь к директории (по умолчанию текущая)")
    # Добавляем флаг -a/--all для показа скрытых файлов
    # action="store_true" — если флаг указан, args.all будет True
    parser.add_argument("-a", "--all", action="store_true", help="Показывать скрытые файлы")
    # Добавляем флаг -l/--long для длинного формата вывода
    # action="store_true" — если флаг указан, args.long будет True
    parser.add_argument("-l", "--long", action="store_true", help="Длинный формат (разрешения, размер, дата)")
    # Парсим аргументы командной строки, результат сохраняется в args
    args = parser.parse_args()
    # Вызываем функцию вывода содержимого директории с учётом переданных опций
    list_dir(args.directory, show_all=args.all, long_format=args.long)
            
            
