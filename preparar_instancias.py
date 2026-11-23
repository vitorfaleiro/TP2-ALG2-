import csv
import shutil
from pathlib import Path
from urllib.request import Request, urlopen

from src.instancia import lerInstancia


URL_BASE = (
    "https://raw.githubusercontent.com/pdrozdowski/"
    "TSPLib.Net/master/TSPLIB95/tsp"
)

INSTANCIAS_ORIGINAIS = {
    "eil51": 51,
    "berlin52": 52,
    "st70": 70
}

INSTANCIAS_DERIVADAS = {
    "kroA100": 10,
    "kroB100": 12,
    "kroC100": 14,
    "kroD100": 16,
    "kroE100": 18,
    "rat99": 20,
    "rd100": 22,
    "lin105": 24,
    "pr124": 26,
    "bier127": 28,
    "ch130": 30,
    "ch150": 40
}

PASTA_INSTANCIAS = Path("data/instances")
PASTA_ORIGINAIS = PASTA_INSTANCIAS / "original"
PASTA_FONTES = PASTA_INSTANCIAS / "sources"
PASTA_DERIVADAS = PASTA_INSTANCIAS / "derived"
PASTA_RESULTADOS = Path("data/results")


def baixarArquivo(nome, destino):
    if destino.exists():
        return

    url = f"{URL_BASE}/{nome}.tsp"
    requisicao = Request(
        url,
        headers={"User-Agent": "TP2-ALG2-instance-preparation"}
    )

    try:
        with urlopen(requisicao, timeout=30) as resposta:
            conteudo = resposta.read().decode("utf-8")
    except Exception as erro:
        raise RuntimeError(
            f"Não foi possível baixar {nome} de {url}: {erro}"
        ) from erro

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def validarInstancia(caminhoArquivo, nomeEsperado=None, dimensaoEsperada=None):
    instancia = lerInstancia(caminhoArquivo)

    if instancia.tipoDistancia != "EUC_2D":
        raise ValueError(
            f"{caminhoArquivo}: tipo de distância "
            f"{instancia.tipoDistancia}, esperado EUC_2D."
        )

    if nomeEsperado is not None and instancia.nome.lower() != nomeEsperado.lower():
        raise ValueError(
            f"{caminhoArquivo}: nome encontrado {instancia.nome}, "
            f"esperado {nomeEsperado}."
        )

    if dimensaoEsperada is not None and instancia.dimensao != dimensaoEsperada:
        raise ValueError(
            f"{caminhoArquivo}: dimensão encontrada {instancia.dimensao}, "
            f"esperada {dimensaoEsperada}."
        )

    if len(instancia.coordenadas) != instancia.dimensao:
        raise ValueError(
            f"{caminhoArquivo}: quantidade de coordenadas incompatível."
        )

    return instancia


def distanciaQuadrada(cidadeA, cidadeB):
    diferencaX = cidadeA[0] - cidadeB[0]
    diferencaY = cidadeA[1] - cidadeB[1]

    return diferencaX ** 2 + diferencaY ** 2


def selecionarCidades(coordenadas, quantidade):
    totalCidades = len(coordenadas)

    if quantidade < 2 or quantidade > totalCidades:
        raise ValueError("Quantidade de cidades inválida para seleção.")

    centroX = sum(x for x, _ in coordenadas) / totalCidades
    centroY = sum(y for _, y in coordenadas) / totalCidades

    primeiraCidade = max(
        range(totalCidades),
        key=lambda indice: (
            distanciaQuadrada(
                coordenadas[indice],
                (centroX, centroY)
            ),
            -indice
        )
    )

    selecionadas = [primeiraCidade]
    distanciasMinimas = [
        distanciaQuadrada(coordenada, coordenadas[primeiraCidade])
        for coordenada in coordenadas
    ]

    while len(selecionadas) < quantidade:
        proximaCidade = max(
            (
                indice
                for indice in range(totalCidades)
                if indice not in selecionadas
            ),
            key=lambda indice: (distanciasMinimas[indice], -indice)
        )

        selecionadas.append(proximaCidade)

        for indice in range(totalCidades):
            distancia = distanciaQuadrada(
                coordenadas[indice],
                coordenadas[proximaCidade]
            )

            if distancia < distanciasMinimas[indice]:
                distanciasMinimas[indice] = distancia

    return sorted(selecionadas)


def formatarCoordenada(valor):
    return format(valor, ".15g")


def escreverInstanciaDerivada(
    caminhoArquivo,
    nome,
    coordenadas,
    nomeOrigem
):
    linhas = [
        f"NAME: {nome}",
        "TYPE: TSP",
        f"COMMENT: Derived from {nomeOrigem} using deterministic farthest-point sampling",
        f"DIMENSION: {len(coordenadas)}",
        "EDGE_WEIGHT_TYPE: EUC_2D",
        "NODE_COORD_SECTION"
    ]

    for identificador, (x, y) in enumerate(coordenadas, start=1):
        linhas.append(
            f"{identificador} "
            f"{formatarCoordenada(x)} "
            f"{formatarCoordenada(y)}"
        )

    linhas.append("EOF")

    caminhoArquivo.parent.mkdir(parents=True, exist_ok=True)
    caminhoArquivo.write_text(
        "\n".join(linhas) + "\n",
        encoding="utf-8"
    )


def prepararOriginais():
    PASTA_ORIGINAIS.mkdir(parents=True, exist_ok=True)

    caminhoAntigoEil51 = PASTA_INSTANCIAS / "eil51.tsp"
    caminhoNovoEil51 = PASTA_ORIGINAIS / "eil51.tsp"

    if caminhoAntigoEil51.exists() and not caminhoNovoEil51.exists():
        shutil.copy2(caminhoAntigoEil51, caminhoNovoEil51)

    registros = []

    for nome, dimensao in INSTANCIAS_ORIGINAIS.items():
        caminhoArquivo = PASTA_ORIGINAIS / f"{nome}.tsp"

        baixarArquivo(nome, caminhoArquivo)
        instancia = validarInstancia(
            caminhoArquivo,
            nomeEsperado=nome,
            dimensaoEsperada=dimensao
        )

        registros.append({
            "nome": instancia.nome,
            "tipo": "original",
            "dimensao": instancia.dimensao,
            "tipoDistancia": instancia.tipoDistancia,
            "origem": "TSPLIB",
            "arquivo": str(caminhoArquivo).replace("\\", "/")
        })

        print(
            f"[ORIGINAL] {instancia.nome}: "
            f"{instancia.dimensao} cidades, EUC_2D"
        )

    return registros


def prepararDerivadas():
    PASTA_FONTES.mkdir(parents=True, exist_ok=True)
    PASTA_DERIVADAS.mkdir(parents=True, exist_ok=True)

    registros = []

    for nomeOrigem, quantidadeDesejada in INSTANCIAS_DERIVADAS.items():
        caminhoFonte = PASTA_FONTES / f"{nomeOrigem}.tsp"

        baixarArquivo(nomeOrigem, caminhoFonte)
        instanciaFonte = validarInstancia(caminhoFonte)

        if quantidadeDesejada > instanciaFonte.dimensao:
            raise ValueError(
                f"{nomeOrigem}: dimensão derivada maior que a fonte."
            )

        indicesSelecionados = selecionarCidades(
            instanciaFonte.coordenadas,
            quantidadeDesejada
        )

        coordenadasSelecionadas = [
            instanciaFonte.coordenadas[indice]
            for indice in indicesSelecionados
        ]

        nomeDerivada = f"{nomeOrigem}_n{quantidadeDesejada}"
        caminhoDerivada = PASTA_DERIVADAS / f"{nomeDerivada}.tsp"

        escreverInstanciaDerivada(
            caminhoDerivada,
            nomeDerivada,
            coordenadasSelecionadas,
            instanciaFonte.nome
        )

        instanciaDerivada = validarInstancia(
            caminhoDerivada,
            nomeEsperado=nomeDerivada,
            dimensaoEsperada=quantidadeDesejada
        )

        idsOriginais = [
            indice + 1
            for indice in indicesSelecionados
        ]

        registros.append({
            "nome": instanciaDerivada.nome,
            "tipo": "derivada",
            "dimensao": instanciaDerivada.dimensao,
            "tipoDistancia": instanciaDerivada.tipoDistancia,
            "origem": instanciaFonte.nome,
            "arquivo": str(caminhoDerivada).replace("\\", "/"),
            "idsOriginaisSelecionados": ";".join(map(str, idsOriginais)),
            "criterioSelecao": "Farthest Point Sampling determinístico"
        })

        print(
            f"[DERIVADA] {nomeDerivada}: "
            f"{instanciaDerivada.dimensao} cidades "
            f"(origem: {instanciaFonte.nome})"
        )

    return registros


def salvarCatalogo(registros):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    caminhoCatalogo = PASTA_RESULTADOS / "catalogo_instancias.csv"

    campos = [
        "nome",
        "tipo",
        "dimensao",
        "tipoDistancia",
        "origem",
        "arquivo",
        "idsOriginaisSelecionados",
        "criterioSelecao"
    ]

    with open(
        caminhoCatalogo,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            extrasaction="ignore"
        )

        escritor.writeheader()
        escritor.writerows(registros)

    print(f"\nCatálogo salvo em: {caminhoCatalogo}")


def validarConjunto(registros):
    quantidadeTotal = len(registros)

    quantidadePrincipal = sum(
        registro["dimensao"] <= 40
        for registro in registros
    )

    quantidadeEstresse = sum(
        45 <= registro["dimensao"] <= 75
        for registro in registros
    )

    if quantidadeTotal != 15:
        raise ValueError(
            f"Esperadas 15 instâncias, encontradas {quantidadeTotal}."
        )

    if quantidadePrincipal != 12:
        raise ValueError(
            f"Esperadas 12 instâncias até 40 cidades, "
            f"encontradas {quantidadePrincipal}."
        )

    if quantidadeEstresse != 3:
        raise ValueError(
            f"Esperadas 3 instâncias entre 45 e 75 cidades, "
            f"encontradas {quantidadeEstresse}."
        )

    if any(
        registro["tipoDistancia"] != "EUC_2D"
        for registro in registros
    ):
        raise ValueError("Todas as instâncias devem utilizar EUC_2D.")

    print("\nCONJUNTO VALIDADO")
    print("Total de instâncias:", quantidadeTotal)
    print("Até 40 cidades:", quantidadePrincipal)
    print("Entre 45 e 75 cidades:", quantidadeEstresse)
    print("Tipo de distância: EUC_2D")


def main():
    print("PREPARAÇÃO DO CONJUNTO DE INSTÂNCIAS TSPLIB\n")

    registrosOriginais = prepararOriginais()
    registrosDerivados = prepararDerivadas()

    registros = registrosOriginais + registrosDerivados

    validarConjunto(registros)
    salvarCatalogo(registros)

    print("\nPreparação concluída.")
    print("Originais:", PASTA_ORIGINAIS)
    print("Fontes:", PASTA_FONTES)
    print("Derivadas:", PASTA_DERIVADAS)


if __name__ == "__main__":
    main()
