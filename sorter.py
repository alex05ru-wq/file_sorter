"""
Сортировщик файлов: раскладывает файлы из папки (например, «Загрузки»)
по подпапкам в зависимости от типа: Документы, Изображения, Видео и т.д.

Запуск:
    python sorter.py                    — показать, что будет сделано (ничего не трогает)
    python sorter.py --run              — выполнить сортировку
    python sorter.py "D:\\Папка" --run  — отсортировать другую папку
"""
import argparse
import shutil
from datetime import datetime
from pathlib import Path

# Какие расширения в какую папку класть. Легко дополнить своими.
CATEGORIES = {
    'Документы':   ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx',
                    '.csv', '.ppt', '.pptx', '.djvu', '.epub', '.fb2'],
    'Изображения': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.svg', '.tiff'],
    'Видео':       ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm', '.flv'],
    'Музыка':      ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Архивы':      ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Программы':   ['.exe', '.msi', '.apk', '.bat', '.cmd'],
    'Образы':      ['.iso', '.img'],
    'Торренты':    ['.torrent'],
}
OTHER = 'Прочее'

# Расширение -> папка (собираем один раз для быстрого поиска)
EXT_TO_FOLDER = {ext: folder for folder, exts in CATEGORIES.items() for ext in exts}


def target_folder(file):
    return EXT_TO_FOLDER.get(file.suffix.lower(), OTHER)


def unique_path(path):
    """Если файл с таким именем уже есть — добавляем (1), (2)... чтобы ничего не затереть."""
    if not path.exists():
        return path
    n = 1
    while True:
        candidate = path.with_name(f'{path.stem} ({n}){path.suffix}')
        if not candidate.exists():
            return candidate
        n += 1


def sort_folder(folder, run=False):
    folder = Path(folder).expanduser()
    if not folder.is_dir():
        print(f'Папка не найдена: {folder}')
        return

    files = [f for f in folder.iterdir()
             if f.is_file() and not f.name.startswith('.')
             and f.name != 'отчёт_сортировки.txt'
             and f.suffix.lower() not in ('.crdownload', '.part', '.tmp')]  # недокачанные не трогаем

    if not files:
        print('Сортировать нечего: в папке нет файлов.')
        return

    plan = {}
    for f in files:
        plan.setdefault(target_folder(f), []).append(f)

    mode = 'СОРТИРОВКА' if run else 'ПРОВЕРКА (ничего не перемещается)'
    print(f'{mode}: {folder}\n')
    report = [f'Сортировка папки {folder} — {datetime.now():%d.%m.%Y %H:%M}', '']

    moved = 0
    for name in sorted(plan):
        group = plan[name]
        print(f'📁 {name}: {len(group)} файл(ов)')
        report.append(f'{name}: {len(group)}')
        for f in sorted(group):
            print(f'    {f.name}')
            report.append(f'    {f.name}')
            if run:
                dest_dir = folder / name
                dest_dir.mkdir(exist_ok=True)
                dest = unique_path(dest_dir / f.name)
                shutil.move(str(f), str(dest))
                moved += 1

    print(f'\nВсего файлов: {len(files)}')
    if run:
        (folder / 'отчёт_сортировки.txt').write_text('\n'.join(report), encoding='utf-8')
        print(f'Перемещено: {moved}. Отчёт сохранён в «отчёт_сортировки.txt».')
    else:
        print('Чтобы выполнить сортировку, запустите с параметром --run')



def main():
    parser = argparse.ArgumentParser(description='Раскладывает файлы по папкам по типу.')
    parser.add_argument('folder', nargs='?', default=str(Path.home() / 'Downloads'),
                        help='какую папку сортировать (по умолчанию «Загрузки»)')
    parser.add_argument('--run', action='store_true', help='выполнить сортировку')
    args = parser.parse_args()
    sort_folder(args.folder, run=args.run)


if __name__ == '__main__':
    main()
