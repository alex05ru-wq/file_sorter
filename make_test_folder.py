"""
Создаёт на рабочем столе папку «Тест_сортировки» с пустыми файлами-примерами,
чтобы безопасно попробовать сортировщик и сделать скриншоты «до/после».
"""
from pathlib import Path

# Рабочий стол может лежать в OneDrive — проверяем оба варианта
candidates = [Path.home() / 'OneDrive' / 'Рабочий стол', Path.home() / 'OneDrive' / 'Desktop',
              Path.home() / 'Desktop']
desktop = next((p for p in candidates if p.is_dir()), Path.home())
folder = desktop / 'Тест_сортировки'
folder.mkdir(exist_ok=True)

names = ['Договор аренды.pdf', 'Отчёт за сентябрь.docx', 'Бюджет 2026.xlsx', 'Презентация.pptx',
         'Отпуск на море.jpg', 'Скриншот экрана.png', 'Аватарка.webp', 'Видео с праздника.mp4',
         'Любимая песня.mp3', 'Фото с телефона.zip', 'Документы.rar', 'setup_chrome.exe',
         'telegram_installer.msi', 'windows11.iso', 'Резюме.pdf', 'Чек из магазина.jpg',
         'Список покупок.txt', 'неизвестный_файл.xyz']
for name in names:
    (folder / name).touch()

print(f'Создана папка с {len(names)} файлами: {folder}')
print(f'Теперь запустите:  python sorter.py "{folder}"')
