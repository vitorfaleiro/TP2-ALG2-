
import csv
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import (
    friedmanchisquare,
    wilcoxon,
    spearmanr
)


pastaResultados = Path("data/results")
pastaAnalise = pastaResultados / "analise"

caminhoResultados = (
    pastaResultados / "resultados_integrados.csv"
)

caminhoProfiling = (
    pastaResultados / "profiling_integrado.csv"
)

algoritmos = [
    "Nearest Neighbor",
    "Twice-around-the-tree",
    "Christofides",
    "Convex Hull + Cheapest Insertion"
]

caracteristicas = [
    "aspectRatio",
    "proporcaoFechoConvexo",
    "entropiaEspacial",
    "grauMaximoAgm",
    "cvVizinhoMaisProximo"
]


def prepararPastas():
    pastaAnalise.mkdir(
        parents=True,
        exist_ok=True
    )


def carregarDados():
    if not caminhoResultados.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminhoResultados}"
        )

    if not caminhoProfiling.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminhoProfiling}"
        )

    dados = pd.read_csv(caminhoResultados)
    profiling = pd.read_csv(caminhoProfiling)

    colunasResultados = [
        "instancia",
        "dimensao",
        "algoritmo",
        "custo",
        "tempoTotal",
        "status"
    ]

    colunasProfiling = [
        "instancia",
        "dimensao",
        "subrotina",
        "tempoMediano",
        "memoriaMedianaMB"
    ]

    if not set(colunasResultados).issubset(dados.columns):
        raise ValueError(
            "O arquivo de resultados integrados "
            "não possui todas as colunas necessárias."
        )

    if not set(colunasProfiling).issubset(profiling.columns):
        raise ValueError(
            "O arquivo de profiling integrado "
            "não possui todas as colunas necessárias."
        )

    for coluna in [
        "dimensao",
        "custo",
        "tempoTotal"
    ] + caracteristicas:
        if coluna in dados.columns:
            dados[coluna] = pd.to_numeric(
                dados[coluna],
                errors="coerce"
            )

    for coluna in [
        "dimensao",
        "tempoMediano",
        "memoriaMedianaMB"
    ]:
        profiling[coluna] = pd.to_numeric(
            profiling[coluna],
            errors="coerce"
        )

    return dados, profiling


def salvarTabela(tabela, nomeArquivo):
    caminho = pastaAnalise / nomeArquivo

    tabela.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print("Tabela gerada:", caminho)


def salvarGrafico(nomeArquivo):
    caminho = pastaAnalise / nomeArquivo

    plt.tight_layout()
    plt.savefig(
        caminho,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Gráfico gerado:", caminho)


def calcularQualidade(dados):
    resultados = dados[
        (dados["algoritmo"].isin(algoritmos))
        & (dados["status"] == "CONCLUIDO")
    ].copy()

    resultados = resultados.dropna(
        subset=["instancia", "custo", "dimensao"]
    )

    if resultados.empty:
        raise ValueError(
            "Não existem resultados válidos das heurísticas."
        )

    duplicados = resultados.duplicated(
        subset=["instancia", "algoritmo"]
    )

    if duplicados.any():
        raise ValueError(
            "Existem resultados duplicados para "
            "a mesma instância e algoritmo."
        )

    custos = resultados.pivot(
        index="instancia",
        columns="algoritmo",
        values="custo"
    )

    custos = custos.dropna(
        subset=algoritmos
    )

    if len(custos) < 3:
        raise ValueError(
            "São necessárias pelo menos três instâncias "
            "com resultados completos."
        )

    melhorCusto = custos[algoritmos].min(axis=1)

    gaps = (
        custos[algoritmos]
        .div(melhorCusto, axis=0)
        .sub(1)
        .mul(100)
    )

    ranking = custos[algoritmos].rank(
        axis=1,
        method="average",
        ascending=True
    )

    resumo = pd.DataFrame({
        "algoritmo": algoritmos,
        "vitorias": [
            int((custos[algoritmo] == melhorCusto).sum())
            for algoritmo in algoritmos
        ],
        "gapMedioPercentual": [
            gaps[algoritmo].mean()
            for algoritmo in algoritmos
        ],
        "gapMedianoPercentual": [
            gaps[algoritmo].median()
            for algoritmo in algoritmos
        ],
        "rankingMedio": [
            ranking[algoritmo].mean()
            for algoritmo in algoritmos
        ]
    })

    resumo = resumo.sort_values(
        ["rankingMedio", "gapMedioPercentual"]
    )

    salvarTabela(
        resumo,
        "resumo_qualidade_heuristicas.csv"
    )

    tabelaGaps = gaps.reset_index()

    salvarTabela(
        tabelaGaps,
        "gaps_heuristicas.csv"
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        resumo["algoritmo"],
        resumo["gapMedioPercentual"]
    )

    plt.ylabel("Gap médio em relação à melhor heurística (%)")
    plt.xlabel("Algoritmo")
    plt.title("Qualidade relativa das heurísticas")
    plt.xticks(rotation=20, ha="right")

    salvarGrafico("qualidade_heuristicas.png")

    return custos, gaps, resumo


def ajustarHolm(valoresP):
    valoresP = np.asarray(valoresP, dtype=float)

    ajustados = np.full(len(valoresP), np.nan)

    indicesValidos = np.where(np.isfinite(valoresP))[0]

    if len(indicesValidos) == 0:
        return ajustados

    valoresValidos = valoresP[indicesValidos]

    ordem = np.argsort(valoresValidos)

    quantidade = len(valoresValidos)
    menorAnterior = 0.0

    for posicao, indiceOrdenado in enumerate(ordem):
        indiceOriginal = indicesValidos[indiceOrdenado]

        valorAjustado = valoresValidos[indiceOrdenado] * (
            quantidade - posicao
        )

        valorAjustado = min(1.0, valorAjustado)
        valorAjustado = max(menorAnterior, valorAjustado)

        ajustados[indiceOriginal] = valorAjustado

        menorAnterior = valorAjustado

    return ajustados


def compararEstatisticamente(custos):
    registros = []

    dadosCompletos = custos[algoritmos].dropna()

    if len(dadosCompletos) < 2:
        raise ValueError(
            "Não existem instâncias suficientes para a análise estatística."
        )

    estatistica, valorP = friedmanchisquare(
        *(dadosCompletos[algoritmo] for algoritmo in algoritmos)
    )

    registros.append({
        "teste": "Friedman",
        "comparacao": "Quatro algoritmos",
        "quantidadeInstancias": len(dadosCompletos),
        "estatistica": estatistica,
        "valorP": valorP,
        "significativo_0_05": valorP < 0.05
    })

    comparacoes = []

    for algoritmoA, algoritmoB in combinations(algoritmos, 2):
        pares = custos[[algoritmoA, algoritmoB]].dropna()

        if len(pares) == 0:
            continue

        valoresA = pares[algoritmoA]
        valoresB = pares[algoritmoB]

        if np.all(valoresA.to_numpy() == valoresB.to_numpy()):
            estatistica = 0.0
            valorP = 1.0

        else:
            resultado = wilcoxon(
                valoresA,
                valoresB,
                alternative="two-sided"
            )

            estatistica = resultado.statistic
            valorP = resultado.pvalue

        comparacoes.append({
            "teste": "Wilcoxon",
            "comparacao": f"{algoritmoA} vs {algoritmoB}",
            "quantidadeInstancias": len(pares),
            "estatistica": estatistica,
            "valorP": valorP
        })

    valoresP = [
        registro["valorP"]
        for registro in comparacoes
    ]

    valoresAjustados = ajustarHolm(valoresP)

    for registro, valorAjustado in zip(
        comparacoes,
        valoresAjustados
    ):
        registro["valorPAjustadoHolm"] = valorAjustado

        registro["significativo_0_05"] = (
            valorAjustado < 0.05
        )

        registros.append(registro)

    tabela = pd.DataFrame(registros)

    salvarTabela(
        tabela,
        "testes_estatisticos.csv"
    )

    return tabela



def analisarTempos(dados):
    resultados = dados[
        (dados["algoritmo"].isin(algoritmos))
        & (dados["status"] == "CONCLUIDO")
    ].copy()

    resumo = (
        resultados
        .groupby("algoritmo")
        .agg(
            quantidade=("tempoTotal", "count"),
            tempoMediano=("tempoTotal", "median"),
            tempoMedio=("tempoTotal", "mean"),
            desvioPadrao=("tempoTotal", "std"),
            tempoMinimo=("tempoTotal", "min"),
            tempoMaximo=("tempoTotal", "max")
        )
        .reset_index()
    )

    salvarTabela(
        resumo,
        "resumo_tempos_heuristicas.csv"
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        resumo["algoritmo"],
        resumo["tempoMediano"]
    )

    plt.ylabel("Tempo mediano (segundos)")
    plt.xlabel("Algoritmo")
    plt.title("Tempo de execução das heurísticas")
    plt.xticks(rotation=20, ha="right")

    salvarGrafico("tempos_heuristicas.png")

    return resumo


def calcularRegressao(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    valido = (
        np.isfinite(x)
        & np.isfinite(y)
    )

    x = x[valido]
    y = y[valido]

    if len(x) < 3 or len(np.unique(x)) < 2:
        return None

    coeficientes = np.polyfit(x, y, 1)

    previsoes = np.polyval(
        coeficientes,
        x
    )

    residuos = y - previsoes

    somaQuadradosResiduos = np.sum(residuos ** 2)

    somaQuadradosTotal = np.sum(
        (y - np.mean(y)) ** 2
    )

    if somaQuadradosTotal == 0:
        r2 = np.nan
    else:
        r2 = 1 - (
            somaQuadradosResiduos
            / somaQuadradosTotal
        )

    rmse = np.sqrt(
        np.mean(residuos ** 2)
    )

    return {
        "coeficienteAngular": coeficientes[0],
        "intercepto": coeficientes[1],
        "r2": r2,
        "rmse": rmse,
        "quantidadeInstancias": len(x)
    }


def analisarEscalabilidade(dados):
    resultados = dados[
        (dados["algoritmo"].isin(algoritmos))
        & (dados["status"] == "CONCLUIDO")
    ].copy()

    registros = []

    for algoritmo in algoritmos:
        grupo = resultados[
            resultados["algoritmo"] == algoritmo
        ].dropna(
            subset=["dimensao", "tempoTotal"]
        )

        x = grupo["dimensao"].to_numpy()
        y = grupo["tempoTotal"].to_numpy()

        regressaoLinear = calcularRegressao(x, y)

        if regressaoLinear is not None:
            registros.append({
                "algoritmo": algoritmo,
                "modelo": "Linear",
                **regressaoLinear
            })

        positivos = (x > 0) & (y > 0)

        if positivos.sum() >= 3:
            regressaoPotencia = calcularRegressao(
                np.log(x[positivos]),
                np.log(y[positivos])
            )

            if regressaoPotencia is not None:
                expoente = regressaoPotencia[
                    "coeficienteAngular"
                ]

                registros.append({
                    "algoritmo": algoritmo,
                    "modelo": "Potencia (log-log)",
                    "expoenteEstimado": expoente,
                    **regressaoPotencia
                })

        if regressaoLinear is not None:
            previsoes = (
                regressaoLinear["coeficienteAngular"] * x
                + regressaoLinear["intercepto"]
            )

            ordem = np.argsort(x)

            plt.figure(figsize=(8, 5))

            plt.scatter(
                x,
                y,
                label="Medições"
            )

            plt.plot(
                x[ordem],
                previsoes[ordem],
                label="Regressão linear"
            )

            plt.xlabel("Número de cidades (N)")
            plt.ylabel("Tempo (segundos)")
            plt.title(
                f"Escalabilidade temporal - {algoritmo}"
            )

            plt.legend()

            nome = (
                algoritmo.lower()
                .replace(" ", "_")
                .replace("+", "mais")
                .replace("-", "_")
            )

            salvarGrafico(
                f"regressao_tempo_{nome}.png"
            )

    tabela = pd.DataFrame(registros)

    salvarTabela(
        tabela,
        "regressoes_escalabilidade.csv"
    )

    return tabela



def analisarCaracteristicas(dados):
    resultados = dados[
        (dados["algoritmo"].isin(algoritmos))
        & (dados["status"] == "CONCLUIDO")
    ].copy()

    registros = []

    for algoritmo in algoritmos:
        grupo = resultados[
            resultados["algoritmo"] == algoritmo
        ].copy()

        grupo = grupo.dropna(
            subset=["custo", "tempoTotal"]
        )

        if grupo.empty:
            continue

        melhorPorInstancia = (
            resultados
            .groupby("instancia")["custo"]
            .min()
        )

        grupo["gapPercentual"] = grupo.apply(
            lambda linha: (
                linha["custo"]
                / melhorPorInstancia[linha["instancia"]]
                - 1
            ) * 100,
            axis=1
        )

        for caracteristica in caracteristicas:
            if caracteristica not in grupo.columns:
                continue

            for metrica in [
                "tempoTotal",
                "gapPercentual"
            ]:
                pares = grupo[
                    [caracteristica, metrica]
                ].dropna()

                if (
                    len(pares) < 4
                    or pares[caracteristica].nunique() < 2
                    or pares[metrica].nunique() < 2
                ):
                    continue

                resultado = spearmanr(
                    pares[caracteristica],
                    pares[metrica]
                )

                registros.append({
                    "algoritmo": algoritmo,
                    "caracteristica": caracteristica,
                    "metrica": metrica,
                    "quantidadeInstancias": len(pares),
                    "correlacaoSpearman": resultado.statistic,
                    "valorP": resultado.pvalue
                })

    tabela = pd.DataFrame(registros)

    if not tabela.empty:
        tabela["valorPAjustadoHolm"] = ajustarHolm(
            tabela["valorP"].to_numpy()
        )

        tabela["significativo_0_05"] = (
            tabela["valorPAjustadoHolm"] < 0.05
        )

        tabela = tabela.sort_values(
            ["valorPAjustadoHolm", "valorP"]
        )

    salvarTabela(
        tabela,
        "correlacoes_geometricas.csv"
    )

    return tabela




def analisarProfiling(profiling):
    profiling = profiling.copy()

    profiling["grupo"] = profiling["subrotina"].map(
        lambda nome: (
            "Christofides completo"
            if nome == "ChristofidesCompleto"
            else "Branch-and-Bound"
            if nome == "LowerBoundRaiz"
            else "Componentes do Christofides"
        )
    )

    resumo = (
        profiling
        .groupby(["grupo", "subrotina"])
        .agg(
            quantidade=("instancia", "count"),
            tempoMediano=("tempoMediano", "median"),
            tempoMedio=("tempoMediano", "mean"),
            desvioPadraoTempo=("tempoMediano", "std"),
            memoriaMedianaMB=("memoriaMedianaMB", "median"),
            memoriaMediaMB=("memoriaMedianaMB", "mean")
        )
        .reset_index()
        .sort_values(
            ["grupo", "tempoMedio"],
            ascending=[True, False]
        )
    )

    salvarTabela(
        resumo,
        "resumo_profiling.csv"
    )

    componentes = resumo[
        resumo["grupo"] == "Componentes do Christofides"
    ].copy()

    if not componentes.empty:
        plt.figure(figsize=(10, 6))

        plt.bar(
            componentes["subrotina"],
            componentes["tempoMedio"]
        )

        plt.xlabel("Subrotina")
        plt.ylabel("Tempo médio (segundos)")
        plt.title("Tempo de execução dos componentes do Christofides")
        plt.xticks(rotation=25, ha="right")

        salvarGrafico(
            "profiling_componentes_tempos.png"
        )

        plt.figure(figsize=(10, 6))

        plt.bar(
            componentes["subrotina"],
            componentes["memoriaMediaMB"]
        )

        plt.xlabel("Subrotina")
        plt.ylabel("Memória média (MB)")
        plt.title("Consumo de memória dos componentes do Christofides")
        plt.xticks(rotation=25, ha="right")

        salvarGrafico(
            "profiling_componentes_memoria.png"
        )

        salvarTabela(
            componentes,
            "resumo_profiling_componentes.csv"
        )

    visaoGeral = resumo[
        resumo["grupo"] != "Componentes do Christofides"
    ].copy()

    salvarTabela(
        visaoGeral,
        "resumo_profiling_algoritmos_completos.csv"
    )

    return resumo


def analisarEscalabilidadeProfiling(profiling):
    registros = []

    for subrotina in profiling["subrotina"].unique():
        grupo = profiling[
            profiling["subrotina"] == subrotina
        ].dropna(
            subset=[
                "dimensao",
                "tempoMediano",
                "memoriaMedianaMB"
            ]
        )

        for metrica in [
            "tempoMediano",
            "memoriaMedianaMB"
        ]:
            regressao = calcularRegressao(
                grupo["dimensao"],
                grupo[metrica]
            )

            if regressao is None:
                continue

            registros.append({
                "subrotina": subrotina,
                "metrica": metrica,
                **regressao
            })

            plt.figure(figsize=(8, 5))

            plt.scatter(
                grupo["dimensao"],
                grupo[metrica]
            )

            x = grupo["dimensao"].to_numpy()
            y = grupo[metrica].to_numpy()

            coeficientes = np.polyfit(x, y, 1)

            ordem = np.argsort(x)

            plt.plot(
                x[ordem],
                np.polyval(coeficientes, x[ordem])
            )

            plt.xlabel("Número de cidades (N)")
            plt.ylabel(metrica)
            plt.title(
                f"{metrica} - {subrotina}"
            )

            nome = (
                subrotina.lower()
                .replace(" ", "_")
            )

            salvarGrafico(
                f"regressao_profiling_{metrica}_{nome}.png"
            )

    tabela = pd.DataFrame(registros)

    salvarTabela(
        tabela,
        "regressoes_profiling.csv"
    )

    return tabela



def analisarBranchAndBound(dados):
    resultados = dados[
        dados["algoritmo"] == "Branch-and-Bound DFS"
    ].copy()

    if resultados.empty:
        print(
            "\nNenhum resultado de Branch-and-Bound disponível."
        )
        return pd.DataFrame()

    colunas = [
        "instancia",
        "dimensao",
        "warmStart",
        "status",
        "custoInicial",
        "custo",
        "tempoTotal",
        "tempoBusca",
        "tempoLowerBound",
        "memoriaPicoMB",
        "nosVisitados",
        "nosExpandidos",
        "nosCompletos",
        "nosPodados",
        "nosPodadosLimiteInferior",
        "nosPodadosCustoParcial",
        "profundidadeMaxima",
        "chamadasLimiteInferior"
    ]

    colunasDisponiveis = [
        coluna
        for coluna in colunas
        if coluna in resultados.columns
    ]

    resumo = resultados[colunasDisponiveis].copy()

    colunasNumericas = [
        "dimensao",
        "custoInicial",
        "custo",
        "tempoTotal",
        "tempoBusca",
        "tempoLowerBound",
        "memoriaPicoMB",
        "nosVisitados",
        "nosExpandidos",
        "nosCompletos",
        "nosPodados",
        "nosPodadosLimiteInferior",
        "nosPodadosCustoParcial",
        "profundidadeMaxima",
        "chamadasLimiteInferior"
    ]

    for coluna in colunasNumericas:
        if coluna in resumo.columns:
            resumo[coluna] = pd.to_numeric(
                resumo[coluna],
                errors="coerce"
            )

    if {"custoInicial", "custo"}.issubset(resumo.columns):
        resumo["reducaoCustoPercentual"] = np.where(
            resumo["custoInicial"] > 0,
            (
                (
                    resumo["custoInicial"] - resumo["custo"]
                )
                / resumo["custoInicial"]
            ) * 100,
            np.nan
        )

    salvarTabela(
        resumo,
        "resultados_branch_and_bound.csv"
    )

    if "warmStart" in resumo.columns:
        agrupadores = ["warmStart"]

        if "instancia" in resumo.columns:
            agrupadores.append("instancia")

        agregacoes = {
            "quantidadeExecucoes": ("status", "count"),
            "tempoMediano": ("tempoTotal", "median"),
            "custoMediano": ("custo", "median"),
            "custoInicialMediano": ("custoInicial", "median"),
            "reducaoCustoMedia": (
                "reducaoCustoPercentual",
                "mean"
            )
        }

        if "nosVisitados" in resumo.columns:
            agregacoes["nosVisitadosMediana"] = (
                "nosVisitados",
                "median"
            )

        if "nosExpandidos" in resumo.columns:
            agregacoes["nosExpandidosMediana"] = (
                "nosExpandidos",
                "median"
            )

        if "nosPodados" in resumo.columns:
            agregacoes["nosPodadosMediana"] = (
                "nosPodados",
                "median"
            )

        estatisticas = (
            resumo
            .groupby(agrupadores, dropna=False)
            .agg(**agregacoes)
            .reset_index()
        )

        status = (
            resumo
            .groupby(agrupadores + ["status"], dropna=False)
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        estatisticas = estatisticas.merge(
            status,
            on=agrupadores,
            how="left"
        )

        salvarTabela(
            estatisticas,
            "resumo_branch_and_bound.csv"
        )

    return resumo



def executarAnalise():
    prepararPastas()

    print("=" * 65)
    print("ANÁLISE ESTATÍSTICA DOS EXPERIMENTOS")
    print("=" * 65)

    dados, profiling = carregarDados()

    print("\nDados carregados:")
    print("Resultados:", len(dados))
    print("Profiling:", len(profiling))

    print("\n1. Análise da qualidade das heurísticas")

    custos, gaps, qualidade = calcularQualidade(dados)

    print("\nRanking médio:")
    print(
        qualidade[
            [
                "algoritmo",
                "vitorias",
                "gapMedioPercentual",
                "rankingMedio"
            ]
        ].to_string(index=False)
    )

    print("\n2. Testes estatísticos")

    testes = compararEstatisticamente(custos)

    print(
        testes[
            [
                "teste",
                "comparacao",
                "valorP"
            ]
        ].to_string(index=False)
    )

    print("\n3. Análise dos tempos")

    tempos = analisarTempos(dados)

    print(
        tempos[
            [
                "algoritmo",
                "tempoMediano",
                "tempoMedio",
                "desvioPadrao"
            ]
        ].to_string(index=False)
    )

    print("\n4. Regressões de escalabilidade")

    regressoes = analisarEscalabilidade(dados)

    print(regressoes.to_string(index=False))

    print("\n5. Correlações geométricas")

    correlacoes = analisarCaracteristicas(dados)

    print(
        correlacoes.head(20).to_string(index=False)
    )

    print("\n6. Profiling")

    resumoProfiling = analisarProfiling(profiling)
    print("\nRegressões do profiling")

    regressoesProfiling = analisarEscalabilidadeProfiling(
    profiling
    )

    print(regressoesProfiling.to_string(index=False))

    print(
        resumoProfiling.to_string(index=False)
    )

    print("\n7. Branch-and-Bound")

    resumoBranchAndBound = analisarBranchAndBound(dados)

    if not resumoBranchAndBound.empty:
        print(
            resumoBranchAndBound.to_string(index=False)
        )

    print("\n" + "=" * 65)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 65)

    print("Resultados salvos em:", pastaAnalise)


if __name__ == "__main__":
    executarAnalise()
