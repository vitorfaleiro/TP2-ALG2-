
# Histórico de utilização de Inteligência Artificial

Este documento reúne os registros de utilização de ferramentas de Inteligência Artificial durante o desenvolvimento do Trabalho Prático 2 de Algoritmos 2.

O histórico foi organizado com auxílio do próprio ChatGPT ao longo do desenvolvimento, buscando documentar as solicitações, implementações, testes, decisões técnicas e refatorações realizadas.

Os registros descrevem as contribuições da IA e minha participação no desenvolvimento, sem atribuir decisões ou atividades que não tenham sido efetivamente realizadas.

## Registro 01 — Leitura de instâncias TSPLIB

**Status:** Implementação inicial concluída e validada.

### Assistência utilizada

Orientação conceitual e auxílio na implementação do leitor de instâncias TSPLIB.

### Contribuição da IA

- Apresentação das alternativas de representação das coordenadas por lista de tuplas ou dicionário.
- Sugestão de organização das coordenadas pelos identificadores das cidades.
- Proposição de validações e testes.
- Explicação das estruturas de dados e das decisões de implementação.

### Minha participação

- Escolha da lista de tuplas como estrutura de armazenamento, considerando simplicidade e consumo de memória.
- Discussão e compreensão da estratégia de indexação pelos identificadores.
- Execução dos testes com a instância eil51 e arquivos artificiais.
- Verificação dos resultados e identificação dos comportamentos esperados.

### Resultados

- Leitura correta do cabeçalho da instância eil51.
- Armazenamento das 51 coordenadas.
- Organização correta de cidades apresentadas fora de ordem.
- Detecção de IDs duplicados, ausentes e fora do intervalo permitido.

## Registro 02 — Auditoria e refatoração do leitor TSPLIB

**Status:** Primeira refatoração concluída e testes manuais executados.

### Problemas identificados

- Leitura do mesmo arquivo duas vezes.
- Ausência de validação para dimensão zero ou negativa.
- Mensagens genéricas para coordenadas não numéricas.
- Ausência de validação para valores não finitos.
- Ausência de restrição ao tipo de distância EUC_2D.
- Tratamento insuficiente de cabeçalhos incompletos.

### Contribuição da IA

- Identificação de possíveis limitações da implementação inicial.
- Apresentação de alternativas para reorganização do leitor.
- Sugestão de validações adicionais.
- Orientação para execução dos testes de regressão.

### Minha participação

- Escolha da arquitetura simplificada com duas funções.
- Substituição da implementação anterior pela versão refatorada.
- Execução dos testes antes e depois das alterações.
- Verificação das exceções e dos resultados apresentados.

### Alterações realizadas

- Substituição das leituras separadas por uma única passagem pelo arquivo.
- Criação de uma função responsável pela interpretação dos dados.
- Manutenção de uma função pública para leitura da instância.
- Inclusão de verificações para dimensões inválidas.
- Tratamento de erros de conversão numérica.
- Validação de coordenadas finitas.
- Restrição inicial ao formato de distância EUC_2D.

### Resultados observados

- Leitura correta da instância eil51 após a refatoração.
- Preservação da organização de IDs fora de ordem.
- Preservação da identificação de IDs duplicados e ausentes.
- Detecção de IDs fora do intervalo permitido.
- Rejeição de dimensão zero.
- Rejeição de coordenadas não numéricas e infinitas.
- Rejeição de tipos de distância incompatíveis.

### Limitações e próximas etapas

- Automatizar os testes atualmente executados de forma manual.
- Completar a validação de casos de cabeçalho malformado.
- Implementar a matriz de distâncias EUC_2D.
- Instrumentar as execuções para coleta de métricas.


## Registro 03 — Matriz de distâncias EUC_2D

**Status:** Implementação concluída e testes iniciais aprovados.

### Contribuição da IA

- Proposta de matriz simétrica para armazenar os custos.
- Sugestão de calcular apenas a metade superior da matriz.
- Criação dos testes automatizados com unittest.

### Minha participação

- Escolha anterior da matriz de distâncias como estrutura de armazenamento.
- Execução dos testes automatizados.
- Verificação dos resultados obtidos.

### Decisões técnicas

- Utilização de lista de listas para representar a matriz.
- Armazenamento de distâncias inteiras segundo EUC_2D.
- Aproveitamento da simetria para evitar cálculos repetidos.
- Consulta de distâncias em O(1).
- Complexidade O(N²) para construção e armazenamento.

### Resultados

Os quatro testes automatizados foram aprovados:
- Cálculo de distância conhecida.
- Arredondamento EUC_2D.
- Construção da matriz.
- Simetria da matriz da instância eil51.

Tempo total informado pelo unittest: 0,003 segundo.

### Próximas etapas

Implementar Nearest Neighbor e iniciar a instrumentação dos algoritmos.

## Registro 04 — Heurística do Vizinho Mais Próximo

**Status:** Implementação inicial concluída e testes aprovados.

### Contribuição da IA

- Proposta de utilização de uma lista para a rota e um conjunto para as cidades visitadas.
- Separação do cálculo de custo da rota em uma função reutilizável.
- Elaboração de testes automatizados.

### Minha participação

- Execução dos testes automatizados.
- Verificação da validade da rota produzida para a instância eil51.
- Registro e análise inicial dos resultados.

### Decisões técnicas

- Utilização da matriz de distâncias previamente construída.
- Uso de set para verificar cidades visitadas.
- Cidade inicial configurável, com índice zero como padrão.
- Critério determinístico de desempate pelo menor índice.
- Complexidade temporal O(N²) e memória auxiliar O(N).

### Resultados

- Oito testes automatizados aprovados.
- Instância utilizada: eil51.
- Rota válida contendo as 51 cidades e retorno à origem.
- Custo total encontrado pelo Nearest Neighbor: 511.

O valor encontrado representa uma solução viável,
não necessariamente a solução ótima.

### Próxima etapa

Implementação do Branch-and-Bound, com instrumentação
para medir tempo, nós expandidos, nós podados e efeito
das estratégias de warm-start.

## Registro 05 — Primeira implementação do Branch-and-Bound

**Status:** Implementação inicial executada; validação ampliada pendente.

### Contribuição da IA

- Proposta de busca DFS com backtracking.
- Utilização de limite inferior baseado em árvore geradora mínima.
- Integração com warm-start Nearest Neighbor.
- Inclusão de contadores e medição de tempo.

### Minha participação

- Execução do primeiro experimento instrumentado.
- Coleta e apresentação dos resultados.
- Acompanhamento da análise do comportamento do algoritmo.

### Resultados iniciais

Instância: teste_8
Dimensão: 8 cidades
Custo encontrado: 108
Status: OTIMO
Tempo total: 0,000288 s
Tempo do limite inferior: 0,000194 s
Nós expandidos: 47
Nós podados: 35
Rotas completas examinadas: 1

O custo ótimo de 108 também foi confirmado por uma
verificação independente utilizando força bruta.

O tempo dedicado ao cálculo do limite inferior representou
aproximadamente 67,3% do tempo total registrado.

Essa proporção é preliminar e precisará ser investigada
em execuções maiores e repetidas.

### Próximas etapas

- Validar o algoritmo em diferentes instâncias pequenas.
- Automatizar experimentos com tamanhos progressivos.
- Implementar medição de memória.
- Investigar gargalos do limite inferior.
- Comparar diferentes estratégias de warm-start.

## Registro 06 — Primeiros experimentos do Branch-and-Bound

**Status:** Primeiro lote experimental concluído.

### Contribuição da IA

- Proposta de execução progressiva com diferentes quantidades de cidades.
- Orientação para utilização de limites de tempo.
- Análise inicial dos resultados obtidos.

### Minha participação

- Execução dos experimentos.
- Coleta e disponibilização dos dados.
- Acompanhamento da análise dos resultados.
- Identificação dos próximos experimentos necessários.

### Configuração experimental

- Algoritmo: Branch-and-Bound com DFS.
- Warm-start: Nearest Neighbor.
- Lower bound: baseado em árvore geradora mínima.
- Instâncias: subconjuntos dos primeiros vértices da eil51.
- Dimensões: 10, 12, 14, 16, 18 e 20 cidades.
- Limite configurado: 10 segundos por execução.

### Resultados

Todas as seis execuções terminaram com status OTIMO.

O tempo variou de aproximadamente 0,0015 segundo,
para 10 cidades, a 0,9342 segundo, para 20 cidades.

Na instância com 20 cidades:
- Nós expandidos: 65.462.
- Nós podados: 58.775.
- Melhor custo: 243.
- Tempo do lower bound: aproximadamente 0,8329 segundo.

O cálculo do limite inferior representou aproximadamente
89,2% do tempo registrado nessa execução.

### Análise inicial

Os resultados indicam crescimento significativo do esforço
computacional conforme aumentamos a quantidade de cidades.

O cálculo repetido do limite inferior baseado em AGM surgiu
como possível gargalo de desempenho.

Essa observação ainda precisa ser confirmada com experimentos
adicionais e comparações entre diferentes implementações.

### Próximas etapas

- Executar novos testes com instâncias maiores.
- Medir o consumo de memória.
- Avaliar o impacto das estratégias de warm-start.
- Investigar possíveis otimizações no cálculo do lower bound.

## Registro 07 — Twice-around-the-tree

**Status:** Implementação inicial concluída e validada.

### Contribuição da IA
- Utilização do algoritmo de Prim para construir a AGM.
- Proposta de representação da árvore por lista de adjacência.
- Implementação do percurso DFS utilizando pilha.
- Elaboração dos testes automatizados.

### Minha participação
- Execução e validação dos testes automatizados.
- Execução da comparação com Nearest Neighbor na eil51.
- Coleta e análise inicial dos resultados.

### Resultados
Instância: eil51 (51 cidades).

Nearest Neighbor:
- Custo: 511.
- Tempo: 0,000107 s.

Twice-around-the-tree:
- Custo: 581.
- Tempo: 0,000364 s.

Os 16 testes automatizados disponíveis foram aprovados.

Na execução realizada, o Nearest Neighbor produziu uma
rota aproximadamente 12% menor que Twice-around-the-tree.

Os tempos foram obtidos em execuções individuais e ainda
não constituem uma comparação estatística de desempenho.

### Próximas etapas
- Instrumentar separadamente a construção da AGM.
- Realizar experimentos repetidos.
- Reutilizar a AGM na implementação de Christofides.
- Integrar Twice-around-the-tree como warm-start do Branch-and-Bound.

## Registro 08 — Implementação de Christofides

**Status:** Implementação inicial concluída e testes aprovados.

### Contribuição da IA
- Orientação sobre identificação dos vértices de grau ímpar.
- Utilização do NetworkX para matching perfeito de peso mínimo.
- Multigrafo e circuito euleriano.
- Proposta de instrumentação individual das etapas.

### Minha participação
- Instalação e configuração do NetworkX.
- Execução dos testes automatizados.
- Execução da comparação das três heurísticas.
- Coleta e análise dos resultados.

### Resultados — eil51

- Nearest Neighbor: custo 511.
- Twice-around-the-tree: custo 581.
- Christofides: custo 474.
- Vértices de grau ímpar: 24.
- Tempo total do Christofides: 0,007040 s.
- Tempo AGM: 0,000319 s.
- Tempo matching: 0,006651 s.
- Tempo circuito euleriano: 0,000033 s.
- Tempo atalhos: 0,000006 s.

Os 21 testes automatizados foram aprovados.

### Análise inicial

O Christofides encontrou a melhor rota entre as três
heurísticas na instância eil51.

O matching representou aproximadamente 94,5% do tempo
total medido, indicando uma possível concentração do
custo computacional nessa etapa.

O tempo de matching inclui a construção do grafo e a
execução da biblioteca NetworkX.

Os resultados são preliminares e precisam ser avaliados
em outras instâncias e execuções repetidas.

### Próximas etapas
- Refinar o profiling do matching.
- Implementar Convex Hull.
- Integrar as cinco estratégias de warm-start.

## Registro 09 — Convex Hull + Cheapest Insertion

**Status:** Implementação inicial concluída e comparação realizada.

### Contribuição da IA
- Orientação sobre utilização do produto vetorial.
- Proposta de utilização do Cheapest Insertion.
- Elaboração dos testes automatizados.

### Minha participação
- Compreensão das decisões geométricas e computacionais.
- Execução dos testes e comparação das heurísticas.
- Coleta e análise dos resultados.

### Resultados — eil51

- Nearest Neighbor: custo 511; tempo 0,000213 s.
- Twice-around-the-tree: custo 581; tempo 0,000456 s.
- Christofides: custo 474; tempo 0,007244 s.
- Convex Hull + Cheapest Insertion: custo 442; tempo 0,003525 s.

O Convex Hull apresentou a menor rota entre as quatro
heurísticas avaliadas nessa execução.

A redução de custo foi de aproximadamente:
- 13,50% em relação ao Nearest Neighbor.
- 6,75% em relação ao Christofides.
- 23,92% em relação ao Twice-around-the-tree.

Os resultados são preliminares e correspondem a execuções
individuais na instância eil51.

### Próximas etapas
- Integrar as heurísticas ao Branch-and-Bound.
- Comparar o efeito de cada warm-start na busca exata.
- Completar o profiling e os experimentos.


## Registro 10 — Integração das estratégias de warm-start

**Status:** Integração inicial concluída e testes automatizados aprovados.

### Assistência utilizada

Orientação para integração das diferentes estratégias de inicialização ao Branch-and-Bound.

### Contribuição da IA

- Orientação para modificar o Branch-and-Bound para receber diferentes soluções iniciais.
- Proposta de instrumentação dos tempos de inicialização, busca e execução total.
- Elaboração dos testes automatizados para validar a integração.

### Minha participação

- Implementação e integração dos módulos no projeto.
- Compreensão da separação entre geração da solução inicial e busca exata.
- Execução dos testes automatizados.
- Identificação e correção de divergências nos resultados esperados dos testes.

### Estratégias integradas

1. Cold Start.
2. Nearest Neighbor.
3. Convex Hull + Cheapest Insertion.
4. Twice-around-the-tree.
5. Christofides.

### Resultados

- Integração das cinco estratégias ao Branch-and-Bound.
- Validação da geração de rotas iniciais válidas.
- Verificação da compatibilidade das estratégias com a busca exata.
- 33 testes automatizados aprovados.

### Próximas etapas

- Implementar o executor experimental comparativo.
- Selecionar as instâncias TSPLIB para os experimentos oficiais.
- Realizar profiling de tempo e memória.
- Avaliar o impacto das estratégias na quantidade de nós expandidos e podados.
