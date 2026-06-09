import os
import pandas as pd
import streamlit as st

# Настраиваем страницу (делаем её широкой)
st.set_page_config(page_title="Steam History Helper", layout="wide")

st.title("🎮 Steam History Helper & Analytics")


# Кэшируем загрузку данных для каждого отдельного файла
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Словарь на случай, если где-то в файле проскочат текстовые месяцы
    months_ru_to_en = {
        "янв": "Jan",
        "фев": "Feb",
        "мар": "Mar",
        "апр": "Apr",
        "май": "May",
        "мая": "May",
        "июн": "Jun",
        "июл": "Jul",
        "авг": "Aug",
        "сен": "Sep",
        "окт": "Oct",
        "ноя": "Nov",
        "дек": "Dec",
    }

    # Надежно переводим обе колонки с датами в формат datetime
    for date_col in ["Listed On", "Acted On"]:
        if date_col in df.columns:
            s = df[date_col].astype(str).str.lower().str.strip()

            # 1. Удаляем мусорные разделители времени Steam, если они есть
            s = s.str.replace(" @ ", " ", regex=False)
            s = s.str.replace(" в ", " ", regex=False)
            s = s.str.replace(" at ", " ", regex=False)

            # 2. Переводим русские месяцы в английские (если они есть)
            for ru, en in months_ru_to_en.items():
                s = s.str.replace(ru, en, regex=False)

            # 3. Удаляем точки ТОЛЬКО после букв (например, "июн." -> "июн").
            s = s.str.replace(r"([a-zа-я])\.", r"\1", regex=True)

            s = s.replace(["nan", "none", "-", ""], None)

            # Превращаем в реальные даты. dayfirst=True критически важен для формата ДД.ММ.ГГГГ
            df[date_col] = pd.to_datetime(s, errors="coerce", dayfirst=True)

    return df


# --- ИЗМЕНЕНО: ЛОГИКА ПАПКИ ДАННЫХ ---
DATA_FOLDER = "data"

# Если папки 'data' почему-то нет, скрипт сам её создаст, а не упадёт с ошибкой
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Ищем файлы .csv конкретно внутри папки 'data'
csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
# -------------------------------------

# Проверяем наличие файлов
if not csv_files:
    st.error(
        f"📥 В папке '{DATA_FOLDER}' не найдено ни одного CSV-файла! "
        'Пожалуйста, закиньте туда файлы выгрузки истории Steam (например, "main_acc.csv").'
    )
else:
    # 2. Создаем названия для вкладок (отрезаем расширение ".csv")
    tab_names = [file_name[:-4] for file_name in csv_files]
    tabs = st.tabs(tab_names)

    # 3. Перебираем файлы и вкладки в цикле
    for tab, file_name in zip(tabs, csv_files):
        with tab:
            try:
                # ИЗМЕНЕНО: собираем правильный путь к файлу (например, "data/main_acc.csv")
                full_file_path = os.path.join(DATA_FOLDER, file_name)
                df = load_data(full_file_path)

                st.subheader(f"📊 Фильтры и аналитика для аккаунта: {file_name[:-4]}")

                # --- БЛОК ФИЛЬТРОВ ---
                row1_col1, row1_col2, row1_col3 = st.columns([2, 1, 1])

                with row1_col1:
                    search_query = st.text_input(
                        "🔍 Быстрый поиск (по тексту):",
                        "",
                        key=f"search_{file_name}",
                    )

                with row1_col2:
                    available_columns = ["Все колонки"] + list(df.columns)
                    filter_col = st.selectbox(
                        "Искать в конкретной колонке:",
                        available_columns,
                        key=f"filter_col_{file_name}",
                    )

                with row1_col3:
                    type_col = next(
                        (
                            col
                            for col in df.columns
                            if col.strip().lower() == "type"
                        ),
                        None,
                    )
                    if type_col:
                        unique_types = list(df[type_col].dropna().unique())
                        type_options = ["Все операции"] + unique_types
                        selected_type = st.selectbox(
                            "🛒 Тип операции (Type):",
                            type_options,
                            key=f"type_{file_name}",
                        )
                    else:
                        st.warning("⚠️ Колонка 'Type' не найдена.")
                        selected_type = "Все операции"

                # Вторая строка фильтров (Выбор дат и календарь)
                date_options = [
                    col for col in ["Acted On", "Listed On"] if col in df.columns
                ]
                selected_date_col = None
                selected_dates = None

                if date_options:
                    row2_col1, row2_col2 = st.columns(2)

                    with row2_col1:
                        selected_date_col = st.selectbox(
                            "📅 По какой колонке фильтровать даты?",
                            date_options,
                            key=f"date_col_{file_name}",
                        )

                    with row2_col2:
                        valid_dates = df[selected_date_col].dropna()

                        if not valid_dates.empty:
                            min_date = valid_dates.min().date()
                            max_date = valid_dates.max().date()

                            selected_dates = st.date_input(
                                "Укажите временной период (От и До):",
                                value=(min_date, max_date),
                                min_value=min_date,
                                max_value=max_date,
                                key=f"dates_{file_name}",
                            )
                        else:
                            st.info(
                                "В выбранной колонке нет доступных дат для фильтрации."
                            )
                else:
                    st.warning("⚠️ Колонки дат не найдены в файле.")

                # --- ЛОГИКА ФИЛЬТРАЦИИ ПРИ ПОМОЩИ PANDAS ---
                filtered_df = df.copy()

                if (
                    selected_date_col
                    and selected_dates
                    and len(selected_dates) == 2
                ):
                    start_date, end_date = selected_dates
                    start_ts = pd.Timestamp(start_date)
                    end_ts = (
                        pd.Timestamp(end_date)
                        + pd.Timedelta(days=1)
                        - pd.Timedelta(seconds=1)
                    )

                    filtered_df = filtered_df[
                        (filtered_df[selected_date_col] >= start_ts)
                        & (filtered_df[selected_date_col] <= end_ts)
                    ]

                if type_col and selected_type != "Все операции":
                    filtered_df = filtered_df[
                        filtered_df[type_col] == selected_type
                    ]

                if search_query:
                    if filter_col == "Все колонки":
                        mask = (
                            filtered_df.astype(str)
                            .apply(
                                lambda x: x.str.contains(
                                    search_query, case=False, na=False
                                )
                            )
                            .any(axis=1)
                        )
                        filtered_df = filtered_df[mask]
                    else:
                        filtered_df = filtered_df[
                            filtered_df[filter_col]
                            .astype(str)
                            .str.contains(search_query, case=False, na=False)
                        ]

                # --- АВТОМАТИЧЕСКАЯ СОРТИРОВКА (Новые сверху) ---
                sort_col = (
                    selected_date_col
                    if selected_date_col
                    else next(
                        (
                            col
                            for col in ["Acted On", "Listed On"]
                            if col in filtered_df.columns
                        ),
                        None,
                    )
                )
                if sort_col and sort_col in filtered_df.columns:
                    filtered_df = filtered_df.sort_values(
                        by=sort_col, ascending=False
                    )

                # --- БЛОК ДИНАМИЧЕСКОЙ СТАТИСТИКИ ---
                st.markdown("---")
                target_col = "Price in Cents"

                if target_col in filtered_df.columns:
                    if not filtered_df.empty:
                        total_items = filtered_df.shape[0]
                        mean_rubles = filtered_df[target_col].mean() / 100

                        col_stat1, col_stat2 = st.columns(2)
                        with col_stat1:
                            st.metric(
                                label="Количество предметов в серии",
                                value=f"{total_items} шт.",
                            )
                        with col_stat2:
                            st.metric(
                                label="Средняя цена предметов",
                                value=f"{mean_rubles:,.2f} ₽",
                            )
                    else:
                        st.info(
                            "Нет данных для расчета (таблица пустая после применения фильтров)."
                        )
                else:
                    st.error(f"⚠️ Столбец '{target_col}' не найден в вашем CSV.")

                # --- ВЫВОД ИНТЕРАКТИВНОЙ ТАБЛИЦЫ ---
                st.write(
                    f"Отображено строк: **{filtered_df.shape[0]}** из {df.shape[0]}"
                )

                column_configuration = {}
                if "Listed On" in filtered_df.columns:
                    column_configuration["Listed On"] = (
                        st.column_config.DatetimeColumn(
                            "Listed On", format="YYYY-MM-DD"
                        )
                    )
                if "Acted On" in filtered_df.columns:
                    column_configuration["Acted On"] = (
                        st.column_config.DatetimeColumn(
                            "Acted On", format="YYYY-MM-DD"
                        )
                    )

                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config=column_configuration,
                )

            except Exception as e:
                st.error(
                    f"⚠️ Не удалось обработать файл '{file_name}'. Ошибка: {e}"
                )