# Comparação de algoritmos

Projeto da disciplina de Estrutura de Dados Avançadas para comparar ordenação por inserção, ordenação por intercalação e `sorted()` do Python em listas aleatórias.

## Arquivos

- `ordenacao.py`: os dois algoritmos e versões que contam comparações.
- `teste.py`: testes dos casos vazio, unitário, todos iguais, já ordenado, invertido e aleatório.
- `medir.py`: refaz as medições e gera os artefatos dentro de `dados/` e o `RELATORIO.md`.
- `dados/`: contém `dados.cvs` e os gráficos `grafico_tempos.svg` e `grafico_comparacoes.svg`.
- `RELATORIO.md`: tabelas, gráficos e análise dos resultados.

## Como executar

Requer Python 3.8 ou superior. Não há dependências externas.

```text
python -m unittest teste.py
python medir.py
```

O comando `python medir.py` recria o CSV e os gráficos do zero dentro de `dados/`. A semente aleatória fixa torna o experimento reproduzível, embora os tempos possam variar conforme a máquina. A extensão `.cvs` do arquivo de dados é mantida conforme especificado no trabalho.
