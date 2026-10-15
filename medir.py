
"""Executa os experimentos de ordenacao e gera CSV e graficos."""

import csv
import random
import time
from pathlib import Path

from ordenacao import (
    insercao_com_comparacoes,
    intercalacao_com_comparacoes,
)


# Configuracoes do experimento
TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 10
SEMENTE = 20261015

PASTA = Path(__file__).parent
PASTA_DADOS = PASTA / "dados"
CSV_PATH = PASTA_DADOS / "dados.csv"

ALGORITMOS = {
    "insercao": insercao_com_comparacoes,
    "intercalacao": intercalacao_com_comparacoes,
}


class ValorContado:
    """Encapsula um numero e conta as comparacoes feitas pelo sorted()."""

    comparacoes = 0

    def __init__(self, valor):
        self.valor = valor

    def __lt__(self, outro):
        type(self).comparacoes += 1
        return self.valor < outro.valor


def medir_algoritmo(algoritmo, valores):
    """Retorna o tempo em nanossegundos e o numero de comparacoes."""

    inicio = time.perf_counter_ns()
    resultado, comparacoes = algoritmo(valores)
    tempo = time.perf_counter_ns() - inicio

    # A verificacao ocorre fora do intervalo cronometrado.
    if resultado != sorted(valores):
        raise AssertionError("O algoritmo produziu uma ordenacao incorreta.")

    return tempo, comparacoes


def medir_sorted(valores):
    """Mede sorted() e conta suas comparacoes usando __lt__."""

    embrulhados = [ValorContado(valor) for valor in valores]
    ValorContado.comparacoes = 0

    inicio = time.perf_counter_ns()
    resultado = sorted(embrulhados)
    tempo = time.perf_counter_ns() - inicio

    comparacoes = ValorContado.comparacoes

    # Confere o resultado sem incluir essa verificacao no tempo medido.
    valores_ordenados = [item.valor for item in resultado]

    if valores_ordenados != sorted(valores):
        raise AssertionError("sorted() produziu uma ordenacao incorreta.")

    return tempo, comparacoes


def gerar_dados():
    """Executa as repeticoes e retorna todos os resultados individuais."""

    gerador = random.Random(SEMENTE)
    linhas = []

    for tamanho in TAMANHOS:
        for repeticao in range(1, REPETICOES + 1):
            valores = [
                gerador.randrange(-10 * tamanho, 10 * tamanho + 1)
                for _ in range(tamanho)
            ]

            # Mede os algoritmos implementados no projeto.
            for nome, algoritmo in ALGORITMOS.items():
                tempo, comparacoes = medir_algoritmo(
                    algoritmo, valores
                )

                linhas.append([
                    nome,
                    tamanho,
                    repeticao,
                    tempo,
                    comparacoes,
                ])

            # Mede a funcao de ordenacao da biblioteca padrao.
            tempo, comparacoes = medir_sorted(valores)

            linhas.append([
                "sorted",
                tamanho,
                repeticao,
                tempo,
                comparacoes,
            ])

    return linhas


def salvar_csv(linhas):
    """Salva os resultados individuais no arquivo CSV."""

    PASTA_DADOS.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "algoritmo",
            "n",
            "repeticao",
            "tempo_ns",
            "comparacoes",
        ])

        escritor.writerows(linhas)


def calcular_medias(linhas):
    """Calcula as medias de tempo e comparacoes por algoritmo e tamanho."""

    grupos = {}

    for nome, tamanho, repeticao, tempo, comparacoes in linhas:
        chave = (nome, tamanho)

        if chave not in grupos:
            grupos[chave] = {
                "tempos": [],
                "comparacoes": [],
            }

        grupos[chave]["tempos"].append(tempo)
        grupos[chave]["comparacoes"].append(comparacoes)

    medias = {}

    for chave, valores in grupos.items():
        tempos = valores["tempos"]
        comparacoes = valores["comparacoes"]

        medias[chave] = {
            "tempo": sum(tempos) / len(tempos),
            "comparacoes": (
                sum(comparacoes) / len(comparacoes)
            ),
        }

    return medias


def gerar_grafico(medias, metrica, titulo, nome_arquivo):
    """Gera um grafico SVG com escalas numericas proporcionais."""

    cores = {
        "insercao": "#c0392b",
        "intercalacao": "#176b87",
        "sorted": "#5b5b5b",
    }

    largura = 1000
    altura = 560

    margem_esquerda = 100
    margem_direita = 40
    margem_superior = 70
    margem_inferior = 100

    area_largura = largura - margem_esquerda - margem_direita
    area_altura = altura - margem_superior - margem_inferior

    algoritmos = ["insercao", "intercalacao", "sorted"]

    maior_valor = max(
        medias[(algoritmo, tamanho)][metrica]
        for algoritmo in algoritmos
        for tamanho in TAMANHOS
    )

    # Evita divisao por zero na escala vertical.
    if maior_valor == 0:
        maior_valor = 1

    # Escala horizontal proporcional ao tamanho real da entrada.
    maior_tamanho = max(TAMANHOS) or 1

    def coordenada_x(tamanho):
        return (
            margem_esquerda
            + tamanho * area_largura / maior_tamanho
        )

    def coordenada_y(valor):
        return (
            margem_superior
            + area_altura
            - valor * area_altura / maior_valor
        )

    partes = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{largura}" height="{altura}" '
            f'viewBox="0 0 {largura} {altura}">'
        ),
        '<rect width="100%" height="100%" fill="white"/>',
        (
            f'<text x="{largura / 2}" y="35" '
            'text-anchor="middle" font-family="sans-serif" '
            'font-size="22" font-weight="bold">'
            f'{titulo}</text>'
        ),
    ]

    # Linhas horizontais de referencia e escala vertical.
    quantidade_linhas = 5

    for indice in range(quantidade_linhas + 1):
        fracao = indice / quantidade_linhas
        y = margem_superior + fracao * area_altura
        valor = maior_valor * (1 - fracao)

        partes.append(
            f'<line x1="{margem_esquerda}" y1="{y:.2f}" '
            f'x2="{largura - margem_direita}" y2="{y:.2f}" '
            'stroke="#dddddd" stroke-width="1"/>'
        )

        partes.append(
            f'<text x="{margem_esquerda - 12}" y="{y + 4:.2f}" '
            'text-anchor="end" font-family="sans-serif" '
            f'font-size="12">{valor:.0f}</text>'
        )

    # Eixos do grafico.
    partes.append(
        f'<line x1="{margem_esquerda}" y1="{margem_superior}" '
        f'x2="{margem_esquerda}" '
        f'y2="{altura - margem_inferior}" stroke="#333333"/>'
    )

    partes.append(
        f'<line x1="{margem_esquerda}" '
        f'y1="{altura - margem_inferior}" '
        f'x2="{largura - margem_direita}" '
        f'y2="{altura - margem_inferior}" stroke="#333333"/>'
    )

    # Marcas regulares do eixo horizontal.
    quantidade_marcas_x = 5

    for indice in range(quantidade_marcas_x + 1):
        tamanho_marca = maior_tamanho * indice / quantidade_marcas_x
        x = coordenada_x(tamanho_marca)

        partes.append(
            f'<line x1="{x:.2f}" y1="{margem_superior}" '
            f'x2="{x:.2f}" y2="{altura - margem_inferior}" '
            'stroke="#eeeeee" stroke-width="1"/>'
        )

        partes.append(
            f'<text x="{x:.2f}" '
            f'y="{altura - margem_inferior + 25}" '
            'text-anchor="middle" font-family="sans-serif" '
            f'font-size="12">{tamanho_marca:.0f}</text>'
        )

    # Rotulos dos eixos.
    partes.append(
        f'<text x="{margem_esquerda + area_largura / 2}" '
        f'y="{altura - 25}" text-anchor="middle" '
        'font-family="sans-serif" font-size="15">'
        'Tamanho da entrada (n)</text>'
    )

    rotulo_y = (
        "Tempo medio (ns)"
        if metrica == "tempo"
        else "Comparacoes medias"
    )

    partes.append(
        f'<text x="25" y="{margem_superior + area_altura / 2}" '
        f'transform="rotate(-90 25 '
        f'{margem_superior + area_altura / 2})" '
        'text-anchor="middle" font-family="sans-serif" '
        f'font-size="15">{rotulo_y}</text>'
    )

    # Linhas e pontos de cada algoritmo.
    for algoritmo in algoritmos:
        pontos = []

        for tamanho in TAMANHOS:
            valor = medias[(algoritmo, tamanho)][metrica]
            x = coordenada_x(tamanho)
            y = coordenada_y(valor)
            pontos.append((x, y))

        coordenadas = " ".join(
            f"{x:.2f},{y:.2f}" for x, y in pontos
        )

        partes.append(
            f'<polyline points="{coordenadas}" fill="none" '
            f'stroke="{cores[algoritmo]}" stroke-width="3" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
        )

        for x, y in pontos:
            partes.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" '
                f'fill="{cores[algoritmo]}"/>'
            )

    # Legenda.
    posicao_legenda = margem_esquerda

    for algoritmo in algoritmos:
        partes.append(
            f'<line x1="{posicao_legenda}" y1="{altura - 55}" '
            f'x2="{posicao_legenda + 25}" y2="{altura - 55}" '
            f'stroke="{cores[algoritmo]}" stroke-width="3"/>'
        )

        partes.append(
            f'<text x="{posicao_legenda + 32}" '
            f'y="{altura - 50}" font-family="sans-serif" '
            f'font-size="14">{algoritmo}</text>'
        )

        posicao_legenda += 180

    partes.append("</svg>")

    caminho = PASTA_DADOS / nome_arquivo
    caminho.write_text("\n".join(partes), encoding="utf-8")


def executar():
    """Coordena o experimento sem modificar o relatorio."""

    print("Iniciando as medicoes...")

    linhas = gerar_dados()
    salvar_csv(linhas)

    medias = calcular_medias(linhas)

    gerar_grafico(
        medias,
        "tempo",
        "Comparacao dos tempos de ordenacao",
        "grafico_tempos.svg",
    )

    gerar_grafico(
        medias,
        "comparacoes",
        "Comparacao do numero de comparacoes",
        "grafico_comparacoes.svg",
    )

    print(f"Experimento concluido: {CSV_PATH}")
    print(f"Graficos salvos em: {PASTA_DADOS}")
    print("O arquivo RELATORIO.md nao foi alterado.")


if __name__ == "__main__":
    executar()
