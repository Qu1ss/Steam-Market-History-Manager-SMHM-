# 🎮 Steam Market History Manager (SMHM)

[Русский](#русский) | [English](#english)

---

## Русский

Удобный локальный менеджер для визуализации, фильтрации и детального анализа истории ваших транзакций на Торговой площадке Steam. 

> **Примечание:** Скрипт автоматического запуска заточен под пользователей Windows 10/11.

### 🚀 Функционал

* **Полный доступ к истории:** Удобный просмотр всех операций в едином интерактивном интерфейсе.
* **Умные фильтры поиска:**
  * Быстрый поиск по ключевым словам (как по всей таблице, так и по конкретно выбранной колонке).
  * Фильтрация по типу операции (`sale` — продажа / `purchase` — покупка).
* **Гибкая работа с датами:**
  * Автоматическая сортировка «новые сделки сверху» без багов кодировки.
  * Выбор диапазона дат через удобный встроенный календарь («От» и «До»).
  * Возможность переключать логику фильтра: по дате выставления (`Listed on`) или по дате завершения сделки (`Acted on`).
* **Мгновенная аналитика:** Автоматический подсчет количества предметов в выборке и их средней стоимости (идеально, чтобы узнать, сколько вы потратили или заработали на определенных кейсах/скинах за конкретный месяц).

### 🛠️ Технологический стек

* **Python 3.8+**
* **Streamlit** (для современного, легкого и быстрого Web-UI)
* **Pandas** (для эффективной обработки и фильтрации больших массивов данных)

### 📦 Как начать работу?

1. **Установите Python:** Скачайте и установите актуальную версию Python 3 с [официального сайта](https://www.python.org/) (не забудьте поставить галочку *«Add Python to PATH»* при установке).
2. **Установите библиотеки:** Откройте терминал (командную строку) и введите команду:
```bash
   pip install streamlit pandas
   ```
3. **Выгрузите данные из Steam:** Установите в браузере расширение **Steam Inventory Helper**. Скачайте историю ваших сделок в формате CSV, обязательно выбрав в настройках параметр `Exclude non-transaction`.
4. **Подготовьте файл:** Перенесите скачанный CSV-файл в папку с проектом *Steam Market History Manager* и переименуйте его строго в `data.csv`.
5. **Запустите приложение:** Кликните дважды по файлу `Запуск.bat`. В браузере автоматически откроется вкладка с вашей аналитикой!

### 📄 Лицензия

Этот проект распространяется под **лицензией MIT**. Вы можете свободно использовать, модифицировать, копировать и распространять данный код как в личных, так и в коммерческих целях.

---

## English

A convenient local manager for visualizing, filtering, and deeply analyzing your Steam Community Market transaction history. 

> **Note:** The automatic launch script is tailored for Windows 10/11 users.

### 🚀 Features

* **Full History Access:** View and manage all your market operations within a clean, interactive user interface.
* **Smart Search Filters:**
  * Quick keyword search (either across the entire table or restricted to a specific column).
  * Filter transactions by operation type (`sale` or `purchase`).
* **Flexible Date Management:**
  * Automatic "newest transactions on top" sorting with no localized date encoding bugs.
  * Date range selection via an intuitive built-in calendar ("From" and "To").
  * Toggleable filter logic: filter either by the listing date (`Listed on`) or the transaction completion date (`Acted on`).
* **Instant Analytics:** Automatically calculates the total number of items in your current selection and their average price (perfect for finding out exactly how much you spent or earned on specific cases/skins over a given month).

### 🛠️ Tech Stack

* **Python 3.8+**
* **Streamlit** (for a modern, lightweight, and fast Web-UI)
* **Pandas** (for efficient data processing and filtering of large datasets)

### 📦 Getting Started

1. **Install Python:** Download and install the latest version of Python 3 from the [official website](https://www.python.org/) (make sure to check the **"Add Python to PATH"** box during installation).
2. **Install Libraries:** Open your terminal (Command Prompt) and run the following command:
```bash
   pip install streamlit pandas
   ```
3. **Export Your Steam Data:** Install the **Steam Inventory helper** browser extension. Download your market history as a CSV file, making sure to enable the `Exclude non-transaction` option in the extension settings.
4. **Prepare the File:** Move the downloaded CSV file into the *Steam Market History Manager* project folder and rename it exactly to `data.csv`.
5. **Launch the App:** Double-click your `.bat` startup file. A new tab will automatically open in your browser displaying your analytics dashboard!

### 📄 License

This project is licensed under the **MIT License**. You are completely free to use, modify, copy, and distribute this code for both personal and commercial purposes.
