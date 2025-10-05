#!/usr/bin/env python3
"""
Analisador de Dados de Vendas
Lê um CSV, processa e gera total de vendas por categoria.

Uso:
  python src/sales_analyzer.py --input data/sample_sales.csv
"""
import argparse
import sys
import pandas as pd
from pathlib import Path

def guess_column(df, candidates):
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    return None

def main():
    parser = argparse.ArgumentParser(description="Analisador de Dados de Vendas (total por categoria)")
    parser.add_argument("--input", "-i", required=True, help="Caminho do CSV de entrada")
    parser.add_argument("--sep", default=",", help="Separador do CSV (padrão: ,)")
    parser.add_argument("--encoding", default="utf-8", help="Encoding do CSV (padrão: utf-8)")
    parser.add_argument("--out-csv", default="reports/sales_by_category.csv", help="Caminho do CSV de saída")
    parser.add_argument("--out-md", default="reports/sales_by_category.md", help="Caminho do Markdown de saída")
    parser.add_argument("--low-memory", action="store_true", help="Usa low_memory=True no pandas")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input, sep=args.sep, encoding=args.encoding, low_memory=args.low_memory)
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o CSV: {e}", file=sys.stderr)
        sys.exit(1)

    if df.empty:
        print("[ERRO] CSV vazio.", file=sys.stderr)
        sys.exit(1)

    # Tenta detectar colunas
    col_category = guess_column(df, ["categoria", "category"])
    col_total    = guess_column(df, ["total", "amount", "revenue"])
    col_qty      = guess_column(df, ["quantidade", "quantity", "qty"])
    col_price    = guess_column(df, ["preco", "preço", "price", "unit_price"])

    if not col_category:
        print("[ERRO] Coluna de categoria não encontrada. Use nomes como 'categoria' ou 'category'.", file=sys.stderr)
        sys.exit(1)

    # Calcula total se necessário
    if not col_total:
        if col_qty and col_price:
            df["__total__"] = pd.to_numeric(df[col_qty], errors="coerce").fillna(0) * \
                              pd.to_numeric(df[col_price], errors="coerce").fillna(0)
            col_total = "__total__"
        else:
            print("[ERRO] Nenhuma coluna 'total' e não foi possível inferir a partir de quantidade*preço.", file=sys.stderr)
            sys.exit(1)

    # Limpa/normaliza
    df["_category_norm"] = df[col_category].astype(str).str.strip()
    df["_total_num"] = pd.to_numeric(df[col_total], errors="coerce").fillna(0.0)

    # Agrupa
    result = df.groupby("_category_norm", dropna=False)["_total_num"].sum().reset_index()
    result.columns = ["category", "total"]
    result["total"] = result["total"].round(2)

    # Ordena desc
    result = result.sort_values(by="total", ascending=False, ignore_index=True)

    # Garante diretório de saída
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)

    # Salva CSV
    try:
        result.to_csv(args.out_csv, index=False)
    except Exception as e:
        print(f"[ERRO] Falha ao salvar CSV de saída: {e}", file=sys.stderr)

    # Salva Markdown simples
    try:
        md_lines = []
        md_lines.append("| category | total |")
        md_lines.append("|---|---:|")
        for _, row in result.iterrows():
            md_lines.append(f"| {row['category']} | {row['total']:.2f} |")
        Path(args.out_md).write_text("\n".join(md_lines), encoding="utf-8")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar Markdown de saída: {e}", file=sys.stderr)

    # Imprime resumo
    print("Resumo por categoria:")
    print("---------------------")
    if result.empty:
        print("(sem dados)")
    else:
        width_cat = max(8, result['category'].astype(str).map(len).max())
        print(f"{'category'.ljust(width_cat)}  {'total':>12}")
        print("-"*(width_cat+14))
        for _, row in result.iterrows():
            print(f"{str(row['category']).ljust(width_cat)}  {row['total']:>12.2f}")
        print("\nArquivos de saída:")
        print(f" - CSV: {args.out_csv}")
        print(f" - MD : {args.out_md}")

if __name__ == "__main__":
    main()
