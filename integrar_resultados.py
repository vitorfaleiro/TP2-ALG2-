
import csv
from pathlib import Path


pastaResultados = Path("data/results")

caminhoHeuristicas = pastaResultados / "heuristicas.csv"
caminhoExperimentos = pastaResultados / "experimentos_oficiais.csv"
caminhoCaracteristicas = pastaResultados / "caracteristicas_instancias.csv"
caminhoProfiling = pastaResultados / "profiling_subrotinas.csv"

caminhoResultadosIntegrados = (
    pastaResultados / "resultados_integrados.csv"
)

caminhoProfilingIntegrado = (
    pastaResultados / "profiling_integrado.csv"
)


def lerCsv(caminho):
    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    with open(
        caminho,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames is None:
            raise ValueError(
                f"Arquivo sem cabeçalho: {caminho}"
            )

        return list(leitor)


def validarColunas(registros, colunas, nomeArquivo):
    if not registros:
        raise ValueError(
            f"O arquivo {nomeArquivo} não possui registros."
        )

    colunasEncontradas = set(registros[0].keys())

    ausentes = set(colunas) - colunasEncontradas

    if ausentes:
        raise ValueError(
            f"Colunas ausentes em {nomeArquivo}: "
            f"{sorted(ausentes)}"
        )


def validarInstancias(registros, nomeArquivo):
    instancias = {
        registro["nome"]
        for registro in registros
    }

    if len(instancias) != len(registros):
        raise ValueError(
            f"Existem instâncias duplicadas em {nomeArquivo}."
        )

    return instancias


def escreverCsv(caminho, campos, registros):
    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            extrasaction="raise"
        )

        escritor.writeheader()
        escritor.writerows(registros)


def integrarResultados():
    print("=" * 65)
    print("INTEGRAÇÃO DAS BASES EXPERIMENTAIS")
    print("=" * 65)

    heuristicas = lerCsv(caminhoHeuristicas)
    experimentos = lerCsv(caminhoExperimentos)
    caracteristicas = lerCsv(caminhoCaracteristicas)
    profiling = lerCsv(caminhoProfiling)

    validarColunas(
        heuristicas,
        [
            "instancia",
            "tipo",
            "dimensao",
            "algoritmo",
            "custo",
            "tempoMediano",
            "tempoMedio",
            "desvioPadraoTempo"
        ],
        caminhoHeuristicas.name
    )

    validarColunas(
        experimentos,
        [
            "dataExecucao",
            "instancia",
            "tipoInstancia",
            "origem",
            "dimensao",
            "algoritmo",
            "warmStart",
            "tempoLimite",
            "tempoInicializacao",
            "tempoBusca",
            "tempoTotal",
            "tempoLowerBound",
            "memoriaPicoMB",
            "nosVisitados",
            "nosExpandidos",
            "nosCompletos",
            "nosPodados",
            "nosPodadosLimiteInferior",
            "nosPodadosCustoParcial",
            "profundidadeMaxima",
            "custoInicial",
            "melhorCusto",
            "status"
        ],
        caminhoExperimentos.name
    )

    validarColunas(
        caracteristicas,
        [
            "nome",
            "tipo",
            "origem",
            "dimensao",
            "aspectRatio",
            "proporcaoFechoConvexo",
            "entropiaEspacial",
            "grauMaximoAgm",
            "cvVizinhoMaisProximo"
        ],
        caminhoCaracteristicas.name
    )

    validarColunas(
        profiling,
        [
            "instancia",
            "dimensao",
            "subrotina",
            "repeticoes",
            "tempoMediano",
            "memoriaMedianaMB"
        ],
        caminhoProfiling.name
    )

    mapaCaracteristicas = {
        registro["nome"]: registro
        for registro in caracteristicas
    }

    instanciasCaracteristicas = validarInstancias(
        caracteristicas,
        caminhoCaracteristicas.name
    )

    instanciasHeuristicas = {
        registro["instancia"]
        for registro in heuristicas
    }

    instanciasExperimentos = {
        registro["instancia"]
        for registro in experimentos
    }

    instanciasProfiling = {
        registro["instancia"]
        for registro in profiling
    }

    todasInstancias = (
        instanciasHeuristicas
        | instanciasExperimentos
        | instanciasProfiling
    )

    instanciasAusentes = todasInstancias - instanciasCaracteristicas

    if instanciasAusentes:
        raise ValueError(
            "Existem instâncias sem características geométricas: "
            f"{sorted(instanciasAusentes)}"
        )

    instanciasSemHeuristicas = (
        instanciasCaracteristicas - instanciasHeuristicas
    )

    print("\nArquivos carregados:")
    print("Heurísticas:", len(heuristicas))
    print("Experimentos oficiais:", len(experimentos))
    print("Características:", len(caracteristicas))
    print("Profiling:", len(profiling))

    print("\nInstâncias sem heurísticas:", len(instanciasSemHeuristicas))

    if instanciasSemHeuristicas:
        print(sorted(instanciasSemHeuristicas))

    camposResultados = [
        "dataExecucao",
        "instancia",
        "tipoInstancia",
        "origem",
        "dimensao",
        "algoritmo",
        "warmStart",
        "cidadeInicial",
        "repeticoes",
        "tempoLimite",
        "tempoInicializacao",
        "tempoBusca",
        "tempoTotal",
        "tempoMedio",
        "desvioPadraoTempo",
        "tempoMinimo",
        "tempoMaximo",
        "tempoLowerBound",
        "memoriaPicoMB",
        "nosVisitados",
        "nosExpandidos",
        "nosCompletos",
        "nosPodados",
        "nosPodadosLimiteInferior",
        "nosPodadosCustoParcial",
        "profundidadeMaxima",
        "chamadasLimiteInferior",
        "custoInicial",
        "custo",
        "status",
        "aspectRatio",
        "proporcaoFechoConvexo",
        "entropiaEspacial",
        "grauMaximoAgm",
        "cvVizinhoMaisProximo"
    ]

    resultadosIntegrados = []

    for registro in heuristicas:
        caracteristica = mapaCaracteristicas[
            registro["instancia"]
        ]

        resultado = {
            "dataExecucao": "",
            "instancia": registro["instancia"],
            "tipoInstancia": registro["tipo"],
            "origem": caracteristica["origem"],
            "dimensao": registro["dimensao"],
            "algoritmo": registro["algoritmo"],
            "warmStart": "",
            "cidadeInicial": registro["cidadeInicial"],
            "repeticoes": registro["repeticoes"],
            "tempoLimite": "",
            "tempoInicializacao": "",
            "tempoBusca": "",
            "tempoTotal": registro["tempoMediano"],
            "tempoMedio": registro["tempoMedio"],
            "desvioPadraoTempo": registro["desvioPadraoTempo"],
            "tempoMinimo": registro["tempoMinimo"],
            "tempoMaximo": registro["tempoMaximo"],
            "tempoLowerBound": "",
            "memoriaPicoMB": "",
            "nosVisitados": "",
            "nosExpandidos": "",
            "nosCompletos": "",
            "nosPodados": "",
            "nosPodadosLimiteInferior": "",
            "nosPodadosCustoParcial": "",
            "profundidadeMaxima": "",
            "chamadasLimiteInferior": "",
            "custoInicial": "",
            "custo": registro["custo"],
            "status": "CONCLUIDO",
            "aspectRatio": caracteristica["aspectRatio"],
            "proporcaoFechoConvexo": caracteristica[
                "proporcaoFechoConvexo"
            ],
            "entropiaEspacial": caracteristica[
                "entropiaEspacial"
            ],
            "grauMaximoAgm": caracteristica["grauMaximoAgm"],
            "cvVizinhoMaisProximo": caracteristica[
                "cvVizinhoMaisProximo"
            ]
        }

        resultadosIntegrados.append(resultado)

    for registro in experimentos:
        caracteristica = mapaCaracteristicas[
            registro["instancia"]
        ]

        resultado = {
            "dataExecucao": registro["dataExecucao"],
            "instancia": registro["instancia"],
            "tipoInstancia": registro["tipoInstancia"],
            "origem": registro["origem"],
            "dimensao": registro["dimensao"],
            "algoritmo": registro["algoritmo"],
            "warmStart": registro["warmStart"],
            "cidadeInicial": "",
            "repeticoes": 1,
            "tempoLimite": registro["tempoLimite"],
            "tempoInicializacao": registro["tempoInicializacao"],
            "tempoBusca": registro["tempoBusca"],
            "tempoTotal": registro["tempoTotal"],
            "tempoMedio": "",
            "desvioPadraoTempo": "",
            "tempoMinimo": "",
            "tempoMaximo": "",
            "tempoLowerBound": registro["tempoLowerBound"],
            "memoriaPicoMB": registro["memoriaPicoMB"],
            "nosVisitados": registro["nosVisitados"],
            "nosExpandidos": registro["nosExpandidos"],
            "nosCompletos": registro["nosCompletos"],
            "nosPodados": registro["nosPodados"],
            "nosPodadosLimiteInferior": registro[
                "nosPodadosLimiteInferior"
            ],
            "nosPodadosCustoParcial": registro[
                "nosPodadosCustoParcial"
            ],
            "profundidadeMaxima": registro["profundidadeMaxima"],
            "chamadasLimiteInferior": "",
            "custoInicial": registro["custoInicial"],
            "custo": registro["melhorCusto"],
            "status": registro["status"],
            "aspectRatio": caracteristica["aspectRatio"],
            "proporcaoFechoConvexo": caracteristica[
                "proporcaoFechoConvexo"
            ],
            "entropiaEspacial": caracteristica[
                "entropiaEspacial"
            ],
            "grauMaximoAgm": caracteristica["grauMaximoAgm"],
            "cvVizinhoMaisProximo": caracteristica[
                "cvVizinhoMaisProximo"
            ]
        }

        resultadosIntegrados.append(resultado)

    camposProfiling = [
        "instancia",
        "dimensao",
        "subrotina",
        "repeticoes",
        "tempoMediano",
        "memoriaMedianaMB",
        "aspectRatio",
        "proporcaoFechoConvexo",
        "entropiaEspacial",
        "grauMaximoAgm",
        "cvVizinhoMaisProximo"
    ]

    profilingIntegrado = []

    for registro in profiling:
        caracteristica = mapaCaracteristicas[
            registro["instancia"]
        ]

        resultado = {
            "instancia": registro["instancia"],
            "dimensao": registro["dimensao"],
            "subrotina": registro["subrotina"],
            "repeticoes": registro["repeticoes"],
            "tempoMediano": registro["tempoMediano"],
            "memoriaMedianaMB": registro["memoriaMedianaMB"],
            "aspectRatio": caracteristica["aspectRatio"],
            "proporcaoFechoConvexo": caracteristica[
                "proporcaoFechoConvexo"
            ],
            "entropiaEspacial": caracteristica[
                "entropiaEspacial"
            ],
            "grauMaximoAgm": caracteristica["grauMaximoAgm"],
            "cvVizinhoMaisProximo": caracteristica[
                "cvVizinhoMaisProximo"
            ]
        }

        profilingIntegrado.append(resultado)

    escreverCsv(
        caminhoResultadosIntegrados,
        camposResultados,
        resultadosIntegrados
    )

    escreverCsv(
        caminhoProfilingIntegrado,
        camposProfiling,
        profilingIntegrado
    )

    print("\n" + "=" * 65)
    print("INTEGRAÇÃO CONCLUÍDA")
    print("=" * 65)

    print(
        "Resultados integrados:",
        len(resultadosIntegrados)
    )

    print(
        "Profiling integrado:",
        len(profilingIntegrado)
    )

    print(
        "Instâncias com características:",
        len(instanciasCaracteristicas)
    )

    print("\nArquivos gerados:")
    print(caminhoResultadosIntegrados)
    print(caminhoProfilingIntegrado)


if __name__ == "__main__":
    integrarResultados()
