# Relatório Experimental: Comparação de Algoritmos de Ordenação

## 1. Introdução

Algoritmos de ordenação são utilizados para organizar elementos de uma coleção segundo determinado critério. Apesar de produzirem o mesmo resultado para uma mesma entrada, diferentes algoritmos podem apresentar custos computacionais significativamente distintos.

Este experimento compara a ordenação por inserção (*Insertion Sort*), a ordenação por intercalação (*Merge Sort*) e a função nativa `sorted()` da linguagem Python. A análise considera o tempo de execução e o número de comparações entre elementos, buscando compreender como essas métricas se comportam à medida que o tamanho das listas aumenta.

Além de avaliar o desempenho observado, o experimento permite relacionar os resultados práticos com a complexidade teórica dos algoritmos.

## 2. Objetivos

- Implementar a ordenação por inserção e a ordenação por intercalação.
- Medir o tempo médio de execução para diferentes tamanhos de entrada.
- Contabilizar o número médio de comparações entre elementos.
- Comparar os algoritmos implementados com `sorted()`.
- Construir gráficos e tabelas para facilitar a interpretação dos resultados.
- Investigar a relação entre o custo de execução e a quantidade de comparações.
- Avaliar a adequação de cada método conforme as características da entrada.

## 3. Metodologia

### 3.1. Tamanhos das entradas

Foram utilizados dez tamanhos de lista:

| Tamanho da entrada (\(n\)) |
|---:|
| 5 |
| 10 |
| 20 |
| 30 |
| 50 |
| 75 |
| 100 |
| 200 |
| 500 |
| 1000 |

Para cada tamanho, foram realizadas dez repetições. As listas foram geradas com valores inteiros aleatórios, utilizando uma semente fixa (`20261015`) para tornar a geração dos dados reproduzível.

A utilização dos mesmos dados de entrada para os três métodos torna a comparação mais consistente. Entretanto, a semente fixa não garante tempos idênticos em computadores diferentes, pois o desempenho também depende do ambiente de execução.

### 3.2. Métricas coletadas

**Tempo de execução.** Foi utilizado `time.perf_counter_ns()`, que permite medir intervalos de tempo em nanossegundos. Para cada tamanho e algoritmo, foi calculada a média dos dez resultados.

**Número de comparações.** As versões instrumentadas dos algoritmos contam as comparações entre elementos realizadas durante a ordenação. Para `sorted()`, foi utilizada uma classe com o método `__lt__` instrumentado para incrementar um contador.

**Referência teórica.** A expressão \(n\log_2(n)\) foi incluída como referência de crescimento para a análise das comparações. Ela não representa um limite superior exato para cada entrada, nem uma igualdade que o número observado precise obedecer.

### 3.3. Limitações metodológicas

O experimento utiliza listas aleatórias e dez repetições por tamanho. Portanto, seus resultados caracterizam esse cenário específico e não demonstram diretamente o comportamento de todas as entradas possíveis.

Os tempos incluem os custos da implementação executada, como criação de listas, cópias e chamadas recursivas. Por esse motivo, o tempo total não é determinado exclusivamente pela quantidade de comparações.

## 4. Resultados

### 4.1. Tempo médio de execução

Os valores a seguir estão expressos em nanossegundos. Valores menores indicam menor tempo médio observado.

| \(n\) | Inserção | Intercalação | `sorted()` |
|---:|---:|---:|---:|
| 5 | 3.510 | 8.780 | 6.920 |
| 10 | 7.820 | 19.540 | 19.980 |
| 20 | 22.030 | 48.130 | 69.420 |
| 30 | 49.000 | 78.620 | 74.200 |
| 50 | 97.090 | 113.960 | 115.830 |
| 75 | 232.330 | 188.440 | 210.210 |
| 100 | 363.360 | 235.750 | 284.020 |
| 200 | 1.472.610 | 536.590 | 702.100 |
| 500 | 9.918.260 | 1.502.770 | 2.340.190 |
| 1000 | 42.275.670 | 3.689.390 | 4.916.060 |

![Gráfico de tempos médios](dados/grafico_tempos.svg)

**Interpretação.** Nas entradas menores, a ordenação por inserção apresentou os menores tempos médios deste experimento. Isso é compatível com sua implementação simples e com a ausência do custo de divisão recursiva e intercalação.

A partir de \(n=75\), a ordenação por intercalação passou a apresentar menor tempo médio do que a ordenação por inserção. A diferença tornou-se mais expressiva nas listas maiores: para \(n=1000\), o tempo médio da inserção foi de aproximadamente 42,28 milhões de nanossegundos, enquanto o da intercalação foi de aproximadamente 3,69 milhões.

Esse comportamento é coerente com as complexidades esperadas: o custo da inserção cresce quadraticamente em entradas aleatórias, enquanto o Merge Sort apresenta crescimento da ordem de \(n\log n\).

### 4.2. Número médio de comparações

A tabela apresenta as médias de comparações registradas nas dez repetições. A coluna \(n\log_2(n)\) serve como referência de crescimento teórico.

| \(n\) | Inserção | Intercalação | `sorted()` | \(n\log_2(n)\) |
|---:|---:|---:|---:|---:|
| 5 | 7,5 | 7,0 | 9,0 | 11,6 |
| 10 | 26,8 | 22,8 | 24,4 | 33,2 |
| 20 | 109,2 | 63,0 | 64,5 | 86,4 |
| 30 | 254,7 | 111,8 | 111,5 | 147,2 |
| 50 | 627,1 | 223,2 | 219,0 | 282,2 |
| 75 | 1.519,6 | 378,2 | 373,2 | 467,2 |
| 100 | 2.494,7 | 540,8 | 536,2 | 664,4 |
| 200 | 10.234,0 | 1.281,6 | 1.270,7 | 1.528,8 |
| 500 | 62.735,8 | 3.855,3 | 3.828,9 | 4.482,9 |
| 1000 | 251.122,8 | 8.704,6 | 8.658,9 | 9.965,8 |

![Gráfico de comparações médias](dados/grafico_comparacoes.svg)

**Interpretação.** A ordenação por inserção apresentou crescimento acentuado no número de comparações. Nas listas maiores, sua contagem ficou muito acima da registrada pela intercalação.

A intercalação já realizou menos comparações no menor tamanho testado, \(n=5\), e manteve essa vantagem em todos os tamanhos apresentados. Isso mostra que a diferença no custo de comparação pode aparecer antes da diferença no tempo total.

A contagem de `sorted()` permaneceu próxima à da intercalação nas entradas maiores. Esse resultado é compatível com o comportamento de um algoritmo eficiente, mas não significa que ambos tenham a mesma implementação ou os mesmos custos internos.

## 5. Discussão dos resultados

### 5.1. A partir de qual tamanho a intercalação se torna mais rápida?

Neste experimento, a intercalação apresentou menor tempo médio do que a inserção a partir de **\(n=75\)**, considerando os tamanhos testados.

Esse valor não deve ser interpretado como um limite universal. O ponto de transição pode mudar conforme o computador, a implementação, os dados de entrada e o método de medição. O resultado indica apenas onde a vantagem apareceu nas condições deste experimento.

### 5.2. Os pontos de virada dos gráficos coincidem?

**Não.** Para o tempo de execução, a vantagem da intercalação apareceu a partir de \(n=75\). Para o número de comparações, ela já apareceu em \(n=5\), o menor tamanho avaliado.

A diferença acontece porque as métricas representam aspectos distintos do custo computacional. O contador registra comparações entre elementos, mas não mede diretamente todas as operações executadas. O tempo total também é influenciado por criação e cópia de listas, movimentação de elementos, recursão e custos da própria linguagem.

Assim, um algoritmo pode realizar menos comparações e, mesmo assim, levar mais tempo em entradas pequenas, quando os custos adicionais têm maior influência sobre o resultado.

### 5.3. Por que `sorted()` não determina qual dos dois algoritmos é melhor?

A função `sorted()` utiliza o Timsort, um algoritmo otimizado para a biblioteca padrão do Python. Sua implementação possui estratégias próprias e não é equivalente às implementações didáticas de inserção e intercalação utilizadas neste trabalho.

Além disso, a contagem feita por `__lt__` registra comparações realizadas por esse método, mas não inclui todos os custos internos da função. A medição de tempo e a contagem de comparações de `sorted()` também possuem características diferentes das versões instrumentadas dos outros algoritmos.

Portanto, `sorted()` funciona como uma referência prática útil, mas não deve ser utilizado isoladamente para determinar qual dos dois algoritmos implementados é superior em todos os cenários.

### 5.4. Por que a inserção ainda pode ser apropriada?

A ordenação por inserção continua sendo útil para listas pequenas e para entradas que já estão ordenadas ou quase ordenadas.

Sua implementação é simples, tem pouca sobrecarga e pode exigir poucas movimentações quando os elementos já estão próximos de suas posições finais. Em uma lista já ordenada, por exemplo, a quantidade de comparações pode crescer linearmente.

É importante observar que o experimento deste relatório utilizou listas aleatórias. Portanto, a vantagem em listas quase ordenadas é uma característica teórica do algoritmo, não uma conclusão medida diretamente pelos dados apresentados.

### 5.5. O resultado de `sorted()` respeita a referência \(n\log_2(n)\)?

A tabela apresenta \(n\log_2(n)\) como referência para o crescimento do número de comparações. Nas médias registradas, a contagem de `sorted()` ficou abaixo desse valor em todos os tamanhos apresentados.

Isso não deve ser tratado como uma prova de limite assintótico. A expressão \(n\log_2(n)\) é uma referência de ordem de crescimento, não um limite superior exato aplicável a qualquer tamanho e entrada. Além disso, o Timsort pode se beneficiar de padrões presentes nos dados, e o número efetivo de comparações depende da entrada e da implementação.

A instrumentação por `__lt__` permite observar comparações feitas por meio desse operador nos objetos encapsulados, mas não revela todos os detalhes do funcionamento interno do algoritmo.

## 6. Conclusão

O experimento evidencia que a escolha de um algoritmo de ordenação deve considerar tanto a complexidade teórica quanto o comportamento prático.

A ordenação por inserção apresentou melhor tempo médio nas entradas menores testadas, mas seu custo cresceu rapidamente à medida que o tamanho das listas aumentou. A ordenação por intercalação apresentou uma quantidade menor de comparações em todos os tamanhos avaliados e menor tempo médio a partir de \(n=75\).

Os resultados também demonstram que o número de comparações e o tempo de execução não são métricas equivalentes. A implementação, as operações auxiliares e o ambiente de execução podem alterar o desempenho observado.

Por fim, `sorted()` apresentou um desempenho competitivo, servindo como referência para uma solução da biblioteca padrão. A comparação reforça que algoritmos devem ser avaliados dentro do contexto em que serão utilizados, considerando o tamanho e as características dos dados, os custos envolvidos e os objetivos da aplicação.

## 7. Reprodutibilidade

Para executar novamente os testes:

```bash
python -m unittest teste.py
```

Para gerar novas medições, gráficos e tabelas:

```bash
python medir.py
```

O script utiliza a semente `20261015`, realiza dez repetições para cada tamanho e gera os arquivos de resultados automaticamente. Os valores e as conclusões deste relatório correspondem à execução registrada no repositório; após novas medições, é necessário revisar a análise conforme os resultados atualizados.