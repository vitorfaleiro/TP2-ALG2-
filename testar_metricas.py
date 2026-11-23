
from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.branch_and_bound import branchAndBound


instancia = lerInstancia("tests/instancias/teste_8.tsp")
matriz = construirMatrizDistancias(instancia)

resultado = branchAndBound(
    matriz,
    tempoLimite=30,
    warmStart="nearest"
)

print("=" * 45)
print("RESULTADOS DA INSTRUMENTAÇÃO")
print("=" * 45)

print("Instância:", instancia.nome)
print("Status:", resultado.status)

print("\nTempos:")
print("Inicialização:", f"{resultado.tempoWarmStart:.6f} s")
print("Busca:", f"{resultado.tempoBusca:.6f} s")
print("Lower bound:", f"{resultado.tempoLimiteInferior:.6f} s")
print("Total:", f"{resultado.tempo:.6f} s")

print("\nMemória:")
print("Pico de memória Python:", f"{resultado.memoriaPicoMB:.6f} MB")

print("\nNós:")
print("Visitados:", resultado.nosVisitados)
print("Expandidos:", resultado.nosExpandidos)
print("Completos:", resultado.nosCompletos)
print("Podados:", resultado.nosPodados)

print("\nDetalhamento das podas:")
print("Lower bound:", resultado.nosPodadosLimiteInferior)
print("Custo parcial:", resultado.nosPodadosCustoParcial)

print("\nProfundidade máxima:")
print(resultado.profundidadeMaxima)

print("\nValidação dos contadores:")

validacaoVisitas = (
    resultado.nosVisitados
    == resultado.nosExpandidos
    + resultado.nosCompletos
    + resultado.nosPodadosLimiteInferior
)

validacaoPodas = (
    resultado.nosPodados
    == resultado.nosPodadosLimiteInferior
    + resultado.nosPodadosCustoParcial
)

print("Contagem de nós:", validacaoVisitas)
print("Contagem de podas:", validacaoPodas)
print("Memória positiva:", resultado.memoriaPicoMB > 0)

print("=" * 45)
