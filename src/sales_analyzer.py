#!/usr/bin/env python3
"""Analisador bem simples de vendas por categoria."""

import csv
from pathlib import Path

CATEGORY_NAMES = ["categoria", "category"]
QUANTITY_NAMES = ["quantidade", "quantity", "qty"]
PRICE_NAMES = ["preco", "preço", "price", "unit_price"]
TOTAL_NAMES = ["total", "amount", "revenue"]


def ask_user_inputs():
    print("Analisador de vendas (versão básica)")
    print("-----------------------------------")
    csv_path = input("Informe o caminho do arquivo CSV (ex: data/sample_sales.csv): ").strip()
    if not csv_path:
        print("Nenhum caminho informado. Encerrando.")
        return None, None

    separator = input("Qual é o separador do arquivo? (padrão = ,): ").strip()
    if separator == "":
        separator = ","

    return csv_path, separator


def find_column(header, options):
    for column in header:
        if column is None:
            continue
        name = column.strip().lower()
        if name in options:
            return column
    return None


def to_float(value):
    if value is None:
        return 0.0
    text = str(value).strip().replace(",", ".")
    if text == "":
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_rows(csv_path, separator):
    try:
        with open(csv_path, encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=separator)
            if reader.fieldnames is None:
                print("Não encontrei o cabeçalho do CSV. Confira se o arquivo está correto.")
                return None, []
            rows = [row for row in reader]
            return reader.fieldnames, rows
    except FileNotFoundError:
        print("Arquivo não encontrado. Confira o caminho informado.")
    except OSError as error:
        print(f"Não consegui ler o arquivo: {error}")
    return None, []


def calculate_totals(rows, category_col, total_col, qty_col, price_col):
    totals = {}
    for row in rows:
        category_value = row.get(category_col, "") if category_col else ""
        category_name = category_value.strip() or "Sem categoria"

        if total_col:
            sale_total = to_float(row.get(total_col))
        else:
            quantity = to_float(row.get(qty_col))
            price = to_float(row.get(price_col))
            sale_total = quantity * price

        totals[category_name] = totals.get(category_name, 0.0) + sale_total

    ordered = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return ordered


def save_csv_report(path, totals):
    try:
        with open(path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["categoria", "total"])
            for category, value in totals:
                writer.writerow([category, f"{value:.2f}"])
        return True
    except OSError as error:
        print(f"Não foi possível salvar o CSV: {error}")
        return False


def save_markdown_report(path, totals):
    lines = ["| categoria | total |", "|-----------|------:|"]
    for category, value in totals:
        lines.append(f"| {category} | {value:.2f} |")
    try:
        Path(path).write_text("\n".join(lines), encoding="utf-8")
        return True
    except OSError as error:
        print(f"Não foi possível salvar o Markdown: {error}")
        return False


def print_summary(totals):
    if not totals:
        print("Não há dados para mostrar.")
        return

    largest_name = max(len(name) for name, _ in totals)
    print("\nResumo das vendas por categoria")
    print("-" * (largest_name + 15))
    header_name = "categoria".ljust(largest_name)
    print(f"{header_name} | total")
    print("-" * (largest_name + 15))
    for category, value in totals:
        print(f"{category.ljust(largest_name)} | {value:8.2f}")



def main():
    csv_path, separator = ask_user_inputs()
    if not csv_path:
        return

    header, rows = load_rows(csv_path, separator)
    if not header or not rows:
        return

    category_col = find_column(header, CATEGORY_NAMES)
    total_col = find_column(header, TOTAL_NAMES)
    quantity_col = find_column(header, QUANTITY_NAMES)
    price_col = find_column(header, PRICE_NAMES)

    if not category_col:
        print("Nenhuma coluna de categoria encontrada. Use nomes como 'categoria' ou 'category'.")
        return

    if not total_col and (not quantity_col or not price_col):
        print("Não encontrei coluna de total e não foi possível calcular usando quantidade e preço.")
        return

    totals = calculate_totals(rows, category_col, total_col, quantity_col, price_col)
    print_summary(totals)

    reports_folder = Path("reports")
    reports_folder.mkdir(parents=True, exist_ok=True)

    csv_report = reports_folder / "totais_por_categoria.csv"
    md_report = reports_folder / "totais_por_categoria.md"

    if save_csv_report(csv_report, totals):
        print(f"\nRelatório em CSV salvo em: {csv_report}")
    if save_markdown_report(md_report, totals):
        print(f"Relatório em Markdown salvo em: {md_report}")


if __name__ == "__main__":
    main()
