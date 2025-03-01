"""Для работы с файлами и директориями"""
import os

"""Предоставляет высокоуровневый интерфейс для параллельного выполнения задач - Для пула для параллельной обработки"""
from concurrent.futures import ThreadPoolExecutor

"""Быстро подсчитываем количество объектов(слов в тексте)"""
from collections import Counter

"""Для обработки изображений(Python Imaging Library)"""
from PIL import Image, ImageFilter

"""Таймер для подсчёта времени работы функций"""
from datetime import datetime

"""С помощью Lock мы потокобезопасно получаем доступ к консоли"""
"""Чтобы избежать взаимную блокировку при выводе в неё :) """
from threading import Lock

"""Т.е. Для более стабильного и последовательного вывода"""
print_lock = Lock()


def func(x):
    """Задача для параллелизации: вычисление квадратов чисел."""

    """Считаем начало и конец работы функции, так будет в каждой функции"""
    start_time = datetime.now()

    result = x * x

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    """Для более стабильного и последовательного вывода (только один поток может выводить данные в консоль в определённый момент времени)"""
    """Создаём строку, содержащую всю необходимую инфу, чтобы все сразу не выводились"""
    output = (
        f"➤ [START] Вычисление квадрата числа {x} началось в {start_time.strftime('%H:%M:%S.%f')}\n"
        f"✔ [END] Вычисление квадрата числа {x} завершилось в {end_time.strftime('%H:%M:%S.%f')}\n"
        f"   Время выполнения: {elapsed:.6f} сек.\n"
        f"   Результат: {result}\n"
    )
    with print_lock:
        print(output)
    return result



def process_file(file_path):
    """Функция для анализа текста в файле."""

    start_time = datetime.now()
    try:
        """Удобный и правилльный with(закрывает файл автоматически - нет утечки данных)"""
        """В режиме чтения - r, раскодируем в UTF-8"""
        with open(file_path, 'r', encoding='utf-8') as f:
            """Считаем частоту слов"""
            freq_dict = Counter()
            """Читаем построчно"""
            for line in f:
                words = line.split()
                """Апдейтим добавляя слова из текущей строчки"""
                freq_dict.update(words)

        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        """Аналогично всё в одну строчку для правильного вывода"""
        """Возвращаем словарь с частотой встречаемости слов в файле"""
        output = (
            f"➤ [START] Обработка файла '{file_path}' началась в {start_time.strftime('%H:%M:%S.%f')}\n"
            f"✔ [END] Обработка файла '{file_path}' завершилась в {end_time.strftime('%H:%M:%S.%f')}\n"
            f"   Время выполнения: {elapsed:.6f} сек.\n"
        )
        with print_lock:
            print(output)
        return freq_dict

    #Обработка ошибок, возвращаем None, пишем о ней
    except Exception as e:
        end_time = datetime.now()
        print(
            f"✖ [ERROR] Ошибка при обработке файла '{file_path}'\n"
            f"   Началось в {start_time.strftime('%H:%M:%S.%f')}, завершилось в {end_time.strftime('%H:%M:%S.%f')}\n"
            f"   Ошибка: {e}\n"
        )
        return None


def process_image(image_path):
    """Функция для обработки изображений: инверсия цветов и размытие."""
    start_time = datetime.now()
    try:
        """Опять with с автоматическим закрытием - без утечки ресурсов"""
        with Image.open(image_path) as img:
            """Проверяем целостность изображения, т.е. повреждено - исключение"""
            img.verify()
            """Открываем повторно, потому что verify мог изменить состояние img """
            img = Image.open(image_path)

            """Меняем режим на RGB, чтобы избежать проблем с обработкой дальнейшей"""
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGB")

            """Инверсия с помощью функции Image.eval(цвет пикселя меняется на 255-значение изначальное)"""
            inverted_img = Image.eval(img, lambda x: 255 - x)

            """Размываем по радиусу 2"""
            blurred_img = inverted_img.filter(ImageFilter.GaussianBlur(2))

            """Сохраняем обработанное изображение"""
            output_path = f"{os.path.splitext(image_path)[0]}_processed.jpg"
            blurred_img.save(output_path)

            """Всё аналогично"""
            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds()
            print(
                f"➤ [START] Обработка изображения '{image_path}' началась в {start_time.strftime('%H:%M:%S.%f')}\n"
                f"✔ [END] Обработка изображения '{image_path}' завершилась в {end_time.strftime('%H:%M:%S.%f')}\n"
                f"   Время выполнения: {elapsed:.6f} сек.\n"
                f"   Сохранено как '{output_path}'\n"
            )
            return output_path

    #Обрабатываем ошибки
    except Exception as e:
        end_time = datetime.now()
        print(
            f"✖ [ERROR] Ошибка при обработке изображения '{image_path}'\n"
            f"   Началось в {start_time.strftime('%H:%M:%S.%f')}, завершилось в {end_time.strftime('%H:%M:%S.%f')}\n"
            f"   Ошибка: {e}\n"
        )
        return None


def main():
    # Определяем корневую папку проекта
    project_root = os.getcwd()

    # Составляем список всех текстовых файлов в корневой папке
    text_files = [os.path.join(project_root, f) for f in os.listdir(project_root) if f.endswith('.txt')]

    # Составляем список всех изображений (JPEG и PNG)
    image_files = [os.path.join(project_root, f) for f in os.listdir(project_root) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not text_files and not image_files:
        print("Нет файлов для обработки.\n")
        return

    # Числа для вычисления квадратов
    numbers = list(range(1, 100))

    # Определяем оптимальное число потоков
    workers = min(5, os.cpu_count())

    # Параллельная обработка чисел
    print("=== Обрабатываем числа ===\n")
    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(func, numbers))

    print("Квадраты чисел:")
    print(results, end="\n\n")

    # Параллельная обработка текстовых файлов
    if text_files:
        print("=== Обрабатываем текстовые файлы ===\n")
        with ThreadPoolExecutor(workers) as pool:
            file_results = list(pool.map(process_file, text_files))

        print("\nЧастотные словари для файлов (по словам):")
        for file, freq_dict in zip(text_files, file_results):
            if freq_dict is not None:
                print(f"\nФайл: {file}")
                if sum(freq_dict.values()) == 0:
                    print(f"Файл пуст\n")
                else:
                    for word, count in freq_dict.items():
                        print(f"{word}: {count}")
            else:
                print(f"\nФайл '{file}' \nНе обработан из-за ошибок\n")

    # Параллельная обработка изображений
    if image_files:
        print("=== Обрабатываем изображения ===\n")
        with ThreadPoolExecutor(workers) as pool:
            list(pool.map(process_image, image_files))


if __name__ == "__main__":
    main()
