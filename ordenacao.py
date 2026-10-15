"""Algoritmos de ordenacao e suas versoes instrumentadas."""


def insercao(valores):
    """Ordena uma copia usando ordenacao por insercao."""
    return insercao_com_comparacoes(valores)[0]


def insercao_com_comparacoes(valores):
    """Retorna (lista ordenada, numero de comparacoes entre elementos)."""
    resultado = list(valores)
    comparacoes = 0
    for indice in range(1, len(resultado)):
        chave = resultado[indice]
        posicao = indice - 1
        while posicao >= 0:
            comparacoes += 1
            if resultado[posicao] <= chave:
                break
            resultado[posicao + 1] = resultado[posicao]
            posicao -= 1
        resultado[posicao + 1] = chave
    return resultado, comparacoes


def intercalacao(valores):
    """Ordena uma copia usando ordenacao por intercalacao (merge sort)."""
    return intercalacao_com_comparacoes(valores)[0]


def intercalacao_com_comparacoes(valores):
    """Retorna (lista ordenada, numero de comparacoes entre elementos)."""
    resultado, comparacoes = _intercalar(list(valores))
    return resultado, comparacoes


def _intercalar(valores):
    if len(valores) <= 1:
        return valores, 0

    meio = len(valores) // 2
    esquerda, comparacoes_esquerda = _intercalar(valores[:meio])
    direita, comparacoes_direita = _intercalar(valores[meio:])
    intercalada = []
    indice_esquerda = indice_direita = comparacoes = 0

    while indice_esquerda < len(esquerda) and indice_direita < len(direita):
        comparacoes += 1
        if esquerda[indice_esquerda] <= direita[indice_direita]:
            intercalada.append(esquerda[indice_esquerda])
            indice_esquerda += 1
        else:
            intercalada.append(direita[indice_direita])
            indice_direita += 1

    intercalada.extend(esquerda[indice_esquerda:])
    intercalada.extend(direita[indice_direita:])
    return intercalada, comparacoes_esquerda + comparacoes_direita + comparacoes