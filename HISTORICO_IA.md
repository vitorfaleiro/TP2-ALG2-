
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

- Fornecimento da implementação inicial do Nearest Neighbor.
- Proposta de utilização de uma lista para a rota e um conjunto para as cidades visitadas.
- Separação do cálculo de custo da rota em uma função reutilizável.
- Elaboração de testes automatizados.

### Minha participação

- Implementação local dos módulos propostos.
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