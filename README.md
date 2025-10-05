# Analisador de Dados de Vendas (Python)

Script para ler um arquivo **CSV**, processar os dados e **gerar um relatório com o total de vendas por categoria**.

> **Tecnologias**: Python (Pandas), Git, GitHub

## 🧩 O que o projeto faz
- Lê um CSV com colunas de vendas
- Normaliza automaticamente nomes comuns de colunas (ex.: `categoria`, `category`, `quantidade`, `quantity`)
- Calcula o **total de vendas por categoria**
- Gera um relatório em **CSV** e **Markdown** em `reports/`
- Exibe um resumo no terminal

## 🗂 Estrutura
```
sales-analyzer-python/
  data/
    sample_sales.csv          # Exemplo de dados
  reports/                    # Saída dos relatórios
  src/
    sales_analyzer.py         # Script principal (CLI)
  README.md
  requirements.txt
```

## ▶️ Como rodar
```bash
# 1) Criar e ativar venv (opcional, mas recomendado)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Instalar dependências
pip install -r requirements.txt

# 3) Executar com o CSV de exemplo
python src/sales_analyzer.py --input data/sample_sales.csv

# 4) (Opcional) Salvar relatórios em nomes específicos
python src/sales_analyzer.py --input data/sample_sales.csv --out-csv reports/meu_relatorio.csv --out-md reports/meu_relatorio.md
```

## 📥 Formato do CSV
O script tenta reconhecer automaticamente as seguintes colunas (em PT/EN), sem diferenciar maiúsculas/minúsculas:
- Categoria: `categoria`, `category`
- Quantidade: `quantidade`, `quantity`, `qty` *(opcional se houver `total`)*
- Preço unitário: `preco`, `preço`, `price`, `unit_price` *(opcional se houver `total`)*
- Total: `total`, `amount`, `revenue`

Se **não** houver coluna `total`, o script calcula `total = quantidade * preço_unitário`.

Veja `data/sample_sales.csv` como referência.

## 🧪 Exemplo de saída (terminal)
```
Resumo por categoria:
---------------------
category         total
----------------------
Bebidas        1530.00
Padaria        1210.50
Higiene         845.90
```

## 🧰 Dicas
- Para usar **outro separador**, passe `--sep ';'`.
- Para CSVs grandes, use `--low-memory`.
- Para ver mais opções: `python src/sales_analyzer.py -h`.

## 🗃️ Git (sugestão)
```bash
git init
git add .
git commit -m "feat: analisador de vendas inicial"
git branch -M main
git remote add origin https://github.com/tiagolm16/Analisador-de-Dados-de-Vendas-Python
git push -u origin main
```

## 📄 Licença
MIT
