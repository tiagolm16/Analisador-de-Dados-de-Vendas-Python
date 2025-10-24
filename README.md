# Analisador de Dados de Vendas (versão estudante)

Oi! Este projetinho lê um arquivo CSV com informações de vendas e soma quanto foi vendido em cada categoria.
Tentei fazer tudo usando apenas recursos básicos do Python, porque ainda estou no começo do curso e isso me ajuda a entender melhor como as coisas funcionam.

## Como usar
1. Garanta que você tenha o Python 3 instalado.
2. Abra o terminal na pasta do projeto.
3. Rode o comando abaixo e siga as perguntas do programa:
   ```bash
   python src/sales_analyzer.py
   ```
4. Informe o caminho do arquivo CSV (existe um exemplo em `data/sample_sales.csv`).
5. Se o separador do seu arquivo for vírgula, é só apertar Enter. Caso seja ponto e vírgula ou outro símbolo, digite ele quando o programa perguntar.
6. Quando terminar, veja o resumo direto no terminal. Também são criados dois arquivos dentro da pasta `reports/`:
   - `totais_por_categoria.csv`
   - `totais_por_categoria.md`

## Sobre o arquivo CSV
O script procura por nomes simples de colunas. Ele aceita, por exemplo:
- Categoria: `categoria` ou `category`
- Quantidade: `quantidade`, `quantity` ou `qty`
- Preço: `preco`, `preço`, `price` ou `unit_price`
- Total: `total`, `amount` ou `revenue`

Se a coluna `total` não existir, o programa tenta multiplicar `quantidade * preço` para descobrir o valor de cada linha.

## Saída esperada
Usando o arquivo de exemplo, o terminal mostra algo parecido com isto:
```
Resumo das vendas por categoria
-------------------------------
categoria | total
-------------------------------
Bebidas   |   135.00
Padaria   |   160.50
Higiene   |   387.90
```

## Por que esse projeto é legal pra mim
- Pratiquei leitura de arquivos CSV sem depender de bibliotecas externas.
- Aprendi a trabalhar com dicionários e laços para acumular valores.
- Reforcei a importância de validar entradas do usuário e tratar erros simples.

Se tiver sugestões de melhorias simples, me avise! Estou aprendendo e adoraria deixar o código melhor com o tempo.
