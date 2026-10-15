"""Executa o experimento e gera os resultados na pasta dados."""

import csv
import math
import random
import time
from pathlib import Path

from ordenacao import insercao_com_comparacoes, intercalacao_com_comparacoes


TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 10
SEMENTE = 20261015
PASTA = Path(__file__).parent
PASTA_DADOS = PASTA / "dados"
CSV_PATH = PASTA_DADOS / "dados.cvs"


class ValorContado:
    comparacoes = 0

    def __init__(self, valor):
        self.valor = valor

    def __lt__(self, outro):
        type(self).comparacoes += 1
        return self.valor < outro.valor


def medir_algoritmo(algoritmo, valores):
    inicio = time.perf_counter_ns()
    ordenados, comparacoes = algoritmo(valores)
    tempo = time.perf_counter_ns() - inicio
    if ordenados != sorted(valores):
        raise AssertionError("o algoritmo produziu uma ordenacao incorreta")
    return tempo, comparacoes


def medir_sorted(valores):
    embrulhados = [ValorContado(valor) for valor in valores]
    ValorContado.comparacoes = 0
    inicio = time.perf_counter_ns()
    sorted(embrulhados)
    tempo = time.perf_counter_ns() - inicio
    return tempo, ValorContado.comparacoes


def executar():
    PASTA_DADOS.mkdir(exist_ok=True)
    aleatorio = random.Random(SEMENTE)
    linhas = []
    for tamanho in TAMANHOS:
        for repeticao in range(1, REPETICOES + 1):
            valores = [aleatorio.randrange(-10 * tamanho, 10 * tamanho + 1) for _ in range(tamanho)]
            for nome, algoritmo in (("insercao", insercao_com_comparacoes), ("intercalacao", intercalacao_com_comparacoes)):
                tempo, comparacoes = medir_algoritmo(algoritmo, valores)
                linhas.append([nome, tamanho, repeticao, tempo, comparacoes])
            tempo, comparacoes = medir_sorted(valores)
            linhas.append(["sorted", tamanho, repeticao, tempo, comparacoes])

    with CSV_PATH.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["algoritmo", "n", "repeticao", "tempo_ns", "comparacoes"])
        escritor.writerows(linhas)

    resumo = resumir(linhas)
    gerar_grafico(resumo, "tempo_ns", "Tempo medio (ns)", "grafico_tempos.svg", "Tempos medios de ordenacao")
    gerar_grafico(resumo, "comparacoes", "Comparacoes medias", "grafico_comparacoes.svg", "Comparacoes medias")
    gerar_relatorio(resumo)


def resumir(linhas):
    grupos = {}
    for algoritmo, tamanho, _repeticao, tempo, comparacoes in linhas:
        chave = (algoritmo, int(tamanho))
        grupos.setdefault(chave, []).append((int(tempo), int(comparacoes)))
    return {chave: (sum(item[0] for item in itens) / len(itens), sum(item[1] for item in itens) / len(itens)) for chave, itens in grupos.items()}


def gerar_grafico(resumo, campo, rotulo_y, nome, titulo):
    cores = {"insercao": "#c0392b", "intercalacao": "#176b87", "sorted": "#5b5b5b"}
    pontos = []
    maximo = 0
    for algoritmo in ("insercao", "intercalacao", "sorted"):
        valores = [(n, resumo[(algoritmo, n)][0 if campo == "tempo_ns" else 1]) for n in TAMANHOS]
        maximo = max(maximo, max(valor for _n, valor in valores))
        pontos.append((algoritmo, valores))
    largura, altura = 900, 520
    margem_esquerda, margem_superior = 75, 45
    area_largura, area_altura = 775, 390
    escala_y = area_altura / maximo if maximo else 1

    def ponto(n, valor):
        x = margem_esquerda + (TAMANHOS.index(n) / (len(TAMANHOS) - 1)) * area_largura
        y = margem_superior + area_altura - valor * escala_y
        return x, y

    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{largura / 2}" y="25" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="bold">{titulo}</text>', f'<line x1="{margem_esquerda}" y1="{margem_superior}" x2="{margem_esquerda}" y2="{margem_superior + area_altura}" stroke="#333"/><line x1="{margem_esquerda}" y1="{margem_superior + area_altura}" x2="850" y2="{margem_superior + area_altura}" stroke="#333"/>']
    for n in TAMANHOS:
        x, _ = ponto(n, 0)
        partes.append(f'<text x="{x}" y="{margem_superior + area_altura + 22}" text-anchor="middle" font-family="sans-serif" font-size="12">{n}</text>')
    partes.append(f'<text x="18" y="260" transform="rotate(-90 18 260)" text-anchor="middle" font-family="sans-serif" font-size="13">{rotulo_y}</text>')
    for algoritmo, valores in pontos:
        coordenadas = " ".join(f"{ponto(n, valor)[0]},{ponto(n, valor)[1]}" for n, valor in valores)
        partes.append(f'<polyline points="{coordenadas}" fill="none" stroke="{cores[algoritmo]}" stroke-width="3"/>')
        for n, valor in valores:
            x, y = ponto(n, valor)
            partes.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{cores[algoritmo]}"/>')
    for indice, algoritmo in enumerate(("insercao", "intercalacao", "sorted")):
        x = 620 + indice * 90
        partes.extend([f'<line x1="{x}" y1="490" x2="{x + 22}" y2="490" stroke="{cores[algoritmo]}" stroke-width="3"/>', f'<text x="{x + 27}" y="494" font-family="sans-serif" font-size="12">{algoritmo}</text>'])
    partes.append("</svg>")
    (PASTA_DADOS / nome).write_text("\n".join(partes), encoding="utf-8")


def gerar_relatorio(resumo):
    def media(algoritmo, n, indice):
        return resumo[(algoritmo, n)][indice]

    linhas_tempo = "\n".join(f"| {n} | {media('insercao', n, 0):.0f} | {media('intercalacao', n, 0):.0f} | {media('sorted', n, 0):.0f} |" for n in TAMANHOS)
    linhas_comp = "\n".join(f"| {n} | {media('insercao', n, 1):.1f} | {media('intercalacao', n, 1):.1f} | {media('sorted', n, 1):.1f} | {n * math.log2(n):.1f} |" for n in TAMANHOS)
    virada_tempo = next((n for n in TAMANHOS if media("intercalacao", n, 0) < media("insercao", n, 0)), "nao ocorreu")
    virada_comp = next((n for n in TAMANHOS if media("intercalacao", n, 1) < media("insercao", n, 1)), "nao ocorreu")
    texto = f'''# Relatorio: insercao e intercalacao

Experimento com listas aleatorias, semente `{SEMENTE}`, {REPETICOES} repeticoes por tamanho. Os tempos estao em nanossegundos e sao medias.

## Tempos

| n | Insercao | Intercalacao | sorted() |
|---:|---:|---:|---:|
{linhas_tempo}

![Tempos medios](dados/grafico_tempos.svg)

## Comparacoes

| n | Insercao | Intercalacao | sorted() | n log2(n) |
|---:|---:|---:|---:|---:|
{linhas_comp}

![Comparacoes medias](dados/grafico_comparacoes.svg)

## Analise

- Pelo tempo medido, a intercalacao passa a ser mais rapida a partir de **n = {virada_tempo}**.
- Pelas comparacoes, a intercalacao passa a fazer menos comparacoes a partir de **n = {virada_comp}**. Os pontos de virada dao o mesmo resultado? **{'sim' if virada_tempo == virada_comp else 'nao'}.** A diferenca, quando ocorre, e esperada: tempo inclui custo de alocacao, recursao, copias, movimentacoes e variacoes do sistema, enquanto comparacoes contam apenas uma operacao do algoritmo.
- `sorted()` nao serve para decidir entre os dois algoritmos porque e uma implementacao altamente otimizada da biblioteca padrao (Timsort), com constantes e estrategias diferentes. Ela e uma referencia pratica, nao uma comparacao isolada entre insercao e intercalacao.
- A insercao ainda e adequada para listas pequenas ou quase ordenadas: ela tem pouca sobrecarga, e simples e pode terminar com poucas movimentacoes quando os elementos ja estao perto do lugar certo.
- No `sorted()`, uma classe encapsula cada valor e incrementa um contador em `__lt__`. As comparacoes observadas permanecem na ordem de `n log n` e ficam abaixo do limite aproximado mostrado na tabela, embora o limite assintotico nao seja uma igualdade para cada entrada.
'''
    (PASTA / "RELATORIO.md").write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    executar()