import os
import textwrap

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 7)

# ==========================================
# ПАПКА ДЛЯ РЕЗУЛЬТАТОВ
# ==========================================

output_dir = "niokr_plots"
os.makedirs(output_dir, exist_ok=True)

# ==========================================
# ЗАГРУЗКА ДАННЫХ
# ==========================================

file_name = "niokr.csv"

df = pd.read_csv(file_name)

print("Столбцы датасета:")
print(df.columns.tolist())

# ==========================================
# СТОЛБЦЫ
# ==========================================

title_col = "Наименование НИОКР"
org_col = "Организация"
year_col = "Год начала"
type_col = "Тип работы"
direction_col = "Направление"
cost_col = "Стоимость"

# ==========================================
# ОЧИСТКА
# ==========================================

df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce").fillna(0)

df = df.dropna(subset=[org_col, year_col])

print(f"\nВсего записей: {len(df)}")

# ==========================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# ==========================================

def wrap_labels(labels, width=35):
    return [
        "\n".join(textwrap.wrap(str(x), width=width))
        for x in labels
    ]

# ==========================================
# ГРАФИК 1
# ТОП-10 ОРГАНИЗАЦИЙ
# ==========================================

top_orgs = (
    df[org_col]
    .value_counts()
    .head(10)
    .reset_index()
)

top_orgs.columns = ["Организация", "Количество"]

plt.figure(figsize=(12, 7))

ax = sns.barplot(
    data=top_orgs,
    x="Количество",
    y="Организация",
    hue="Организация",
    legend=False,
    palette="Blues_r"
)

plt.title(
    "Топ-10 организаций по количеству НИОКР",
    fontsize=14
)

plt.xlabel("Количество проектов")
plt.ylabel("")

for i, value in enumerate(top_orgs["Количество"]):
    ax.text(value + 1, i, str(value), va="center")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "01_top_organizations.png"),
    dpi=300
)

plt.close()

# ==========================================
# ГРАФИК 2
# ТОП НАПРАВЛЕНИЙ ПО ФИНАНСИРОВАНИЮ
# ==========================================

direction_budget = (
    df.groupby(direction_col)[cost_col]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

direction_budget.columns = [
    "Направление",
    "Стоимость"
]

direction_budget["Стоимость (млн руб.)"] = (
    direction_budget["Стоимость"] / 1_000_000
)

plt.figure(figsize=(12, 7))

ax = sns.barplot(
    data=direction_budget,
    x="Стоимость (млн руб.)",
    y="Направление",
    hue="Направление",
    legend=False,
    palette="Greens_r"
)

plt.title(
    "Топ направлений по суммарному финансированию",
    fontsize=14
)

plt.xlabel("Млн руб.")
plt.ylabel("")

for i, value in enumerate(
    direction_budget["Стоимость (млн руб.)"]
):
    ax.text(value + 1, i, f"{value:.1f}")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "02_top_directions_budget.png"),
    dpi=300
)

plt.close()

# ==========================================
# ГРАФИК 3
# СТРУКТУРА ТИПОВ РАБОТ
# ==========================================

type_stats = (
    df[type_col]
    .value_counts()
)

plt.figure(figsize=(10, 8))

plt.pie(
    type_stats.values,
    labels=type_stats.index,
    autopct="%1.1f%%",
    startangle=140
)

plt.title(
    "Структура НИОКР по типам работ",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "03_types_structure.png"),
    dpi=300
)

plt.close()

# ==========================================
# ДОПОЛНИТЕЛЬНО:
# ДИНАМИКА ПО ГОДАМ
# ==========================================

year_stats = (
    df[year_col]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    x=year_stats.index,
    y=year_stats.values,
    marker="o"
)

plt.title(
    "Количество НИОКР по годам",
    fontsize=14
)

plt.xlabel("Год")
plt.ylabel("Количество проектов")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "04_year_dynamics.png"),
    dpi=300
)

plt.close()

# ==========================================
# ОТЧЕТ
# ==========================================

total_projects = len(df)

leader_org = top_orgs.iloc[0]["Организация"]
leader_org_count = top_orgs.iloc[0]["Количество"]

leader_direction = direction_budget.iloc[0]["Направление"]
leader_direction_budget = (
    direction_budget.iloc[0]["Стоимость"] / 1_000_000
)

most_common_type = type_stats.index[0]
most_common_type_count = type_stats.iloc[0]

report = f"""
# Аналитический отчет по НИОКР

## Общая информация

Всего проектов:
{total_projects}

## Лидер среди организаций

Организация:
{leader_org}

Количество проектов:
{leader_org_count}

## Наиболее финансируемое направление

Направление:
{leader_direction}

Объем финансирования:
{leader_direction_budget:.2f} млн руб.

## Самый распространенный тип работ

Тип:
{most_common_type}

Количество:
{most_common_type_count}

## Построенные визуализации

1. 01_top_organizations.png
2. 02_top_directions_budget.png
3. 03_types_structure.png
4. 04_year_dynamics.png
"""

with open(
    "niokr_report.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print("\nГотово!")
print(f"Графики сохранены в папке: {output_dir}")
print("Отчет сохранен: niokr_report.md")