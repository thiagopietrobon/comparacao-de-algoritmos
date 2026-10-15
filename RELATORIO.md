# Relatorio: insercao e intercalacao

Experimento com listas aleatorias, semente `20261015`, 10 repeticoes por tamanho. Os tempos estao em nanossegundos e sao medias.

## Tempos

| n | Insercao | Intercalacao | sorted() |
|---:|---:|---:|---:|
| 5 | 3510 | 8780 | 6920 |
| 10 | 7820 | 19540 | 19980 |
| 20 | 22030 | 48130 | 69420 |
| 30 | 49000 | 78620 | 74200 |
| 50 | 97090 | 113960 | 115830 |
| 75 | 232330 | 188440 | 210210 |
| 100 | 363360 | 235750 | 284020 |
| 200 | 1472610 | 536590 | 702100 |
| 500 | 9918260 | 1502770 | 2340190 |
| 1000 | 42275670 | 3689390 | 4916060 |

![Tempos medios](dados/grafico_tempos.svg)

## Comparacoes

| n | Insercao | Intercalacao | sorted() | n log2(n) |
|---:|---:|---:|---:|---:|
| 5 | 7.5 | 7.0 | 9.0 | 11.6 |
| 10 | 26.8 | 22.8 | 24.4 | 33.2 |
| 20 | 109.2 | 63.0 | 64.5 | 86.4 |
| 30 | 254.7 | 111.8 | 111.5 | 147.2 |
| 50 | 627.1 | 223.2 | 219.0 | 282.2 |
| 75 | 1519.6 | 378.2 | 373.2 | 467.2 |
| 100 | 2494.7 | 540.8 | 536.2 | 664.4 |
| 200 | 10234.0 | 1281.6 | 1270.7 | 1528.8 |
| 500 | 62735.8 | 3855.3 | 3828.9 | 4482.9 |
| 1000 | 251122.8 | 8704.6 | 8658.9 | 9965.8 |

![Comparacoes medias](dados/grafico_comparacoes.svg)

## Analise

- Pelo tempo medido, a intercalacao passa a ser mais rapida a partir de **n = 75**.
- Pelas comparacoes, a intercalacao passa a fazer menos comparacoes a partir de **n = 5**. Os pontos de virada dao o mesmo resultado? **nao.** A diferenca, quando ocorre, e esperada: tempo inclui custo de alocacao, recursao, copias, movimentacoes e variacoes do sistema, enquanto comparacoes contam apenas uma operacao do algoritmo.
- `sorted()` nao serve para decidir entre os dois algoritmos porque e uma implementacao altamente otimizada da biblioteca padrao (Timsort), com constantes e estrategias diferentes. Ela e uma referencia pratica, nao uma comparacao isolada entre insercao e intercalacao.
- A insercao ainda e adequada para listas pequenas ou quase ordenadas: ela tem pouca sobrecarga, e simples e pode terminar com poucas movimentacoes quando os elementos ja estao perto do lugar certo.
- No `sorted()`, uma classe encapsula cada valor e incrementa um contador em `__lt__`. As comparacoes observadas permanecem na ordem de `n log n` e ficam abaixo do limite aproximado mostrado na tabela, embora o limite assintotico nao seja uma igualdade para cada entrada.
