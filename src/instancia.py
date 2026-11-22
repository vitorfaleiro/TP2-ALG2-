from dataclasses import dataclass
from math import isfinite


@dataclass
class InstanciaTSP:
    nome: str
    dimensao: int
    tipoDistancia: str
    coordenadas: list[tuple[float, float]]


def interpretarArquivo(linhas):
    nome = None
    dimensao = None
    tipoDistancia = None
    coordenadas = None
    encontrouSecao = False

    for numeroLinha, linha in enumerate(linhas, start=1):
        linha = linha.strip()

        if linha == "NODE_COORD_SECTION":
            encontrouSecao = True

            if dimensao is None:
                raise ValueError("Dimensão da instância não informada.")

            if tipoDistancia != "EUC_2D":
                raise ValueError(
                    f"Tipo de distância não suportado: {tipoDistancia}."
                )

            continue

        if not encontrouSecao:
            if ":" not in linha:
                continue

            chave, valor = linha.split(":", 1)
            chave = chave.strip()
            valor = valor.strip()

            if chave == "NAME":
                nome = valor

            elif chave == "DIMENSION":
                try:
                    dimensao = int(valor)
                except ValueError:
                    raise ValueError(
                        f"Linha {numeroLinha}: dimensão inválida."
                    )

                if dimensao <= 0:
                    raise ValueError("A dimensão deve ser positiva.")

                coordenadas = [None] * dimensao

            elif chave == "EDGE_WEIGHT_TYPE":
                tipoDistancia = valor

            continue

        if linha == "EOF":
            break

        if not linha:
            continue

        partes = linha.split()

        if len(partes) != 3:
            raise ValueError(
                f"Linha {numeroLinha}: formato de coordenada inválido."
            )

        try:
            idCidade = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
        except ValueError:
            raise ValueError(
                f"Linha {numeroLinha}: ID ou coordenada inválida."
            )

        if idCidade < 1 or idCidade > dimensao:
            raise ValueError(f"ID de cidade inválido: {idCidade}.")

        if not isfinite(x) or not isfinite(y):
            raise ValueError(
                f"Linha {numeroLinha}: coordenadas devem ser finitas."
            )

        if coordenadas[idCidade - 1] is not None:
            raise ValueError(f"ID de cidade duplicado: {idCidade}.")

        coordenadas[idCidade - 1] = (x, y)

    if nome is None or dimensao is None or tipoDistancia is None:
        raise ValueError("Cabeçalho da instância incompleto.")

    if not encontrouSecao:
        raise ValueError("Seção de coordenadas não encontrada.")

    if any(coordenada is None for coordenada in coordenadas):
        raise ValueError("Existem IDs de cidades ausentes.")

    return InstanciaTSP(
        nome=nome,
        dimensao=dimensao,
        tipoDistancia=tipoDistancia,
        coordenadas=coordenadas
    )


def lerInstancia(caminhoArquivo):
    with open(caminhoArquivo, "r", encoding="utf-8") as arquivo:
        return interpretarArquivo(arquivo)