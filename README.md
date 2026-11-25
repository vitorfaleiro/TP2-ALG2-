# TP2 — Algoritmos II
**Universidade Federal de Minas Gerais (UFMG)**

**Aluno:** Vitor Faleiro Campos Alves  
**Matrícula:** 2024005920  
**Professor:** Renato Vimieiro

## 1. Sobre o projeto

Este projeto apresenta a implementação e análise experimental de diferentes algoritmos para o Problema do Caixeiro Viajante (TSP — Traveling Salesperson Problem).

Foram desenvolvidas heurísticas construtivas e uma implementação exata baseada em Branch-and-Bound, com o objetivo de comparar a qualidade das soluções, o desempenho computacional e o comportamento dos algoritmos em diferentes instâncias.

## 2. Organização do repositório

- `src/`: implementações dos algoritmos e módulos auxiliares.
- `tests/`: testes automatizados das implementações.
- `data/instances/`: instâncias utilizadas nos experimentos, incluindo originais e derivadas.
- `data/results/`: resultados experimentais, características das instâncias e dados de profiling.
- `relatorio/`: artigo científico, PDF final, arquivos LaTeX, figuras e dados utilizados na elaboração do relatório.
- `analise_estatistica.py`: análises estatísticas e geração de tabelas e gráficos.
- `executar_experimento.py`: execução dos experimentos oficiais de Branch-and-Bound.
- `executar_heuristicas.py`: execução das heurísticas construtivas.
- `profiling_subrotinas.py`: instrumentação e análise das subrotinas.
- `integrar_resultados.py`: integração dos resultados experimentais.
- `preparar_instancias.py`: preparação das instâncias utilizadas.
- `gerar_caracteristicas.py`: extração das características das instâncias.
- `validar_conjunto.py`: validação do conjunto experimental.
- `requirements.txt`: dependências necessárias para execução do projeto.
- `HISTORICO_IA.md`: registro da utilização de ferramentas de inteligência artificial durante o desenvolvimento.

## 3. Como executar

Recomenda-se utilizar Python 3 e instalar as dependências do projeto:

```bash
pip install -r requirements.txt
```

Os scripts devem ser executados a partir do diretório raiz do repositório, respeitando a organização dos arquivos e diretórios de dados.

## 4. Testes automatizados

Para executar a suíte de testes:

```bash
python -m unittest discover -s tests -p "test*.py" -v
```

Na última execução registrada durante o desenvolvimento, os 33 testes automatizados foram aprovados.

## 5. Relatório

O artigo científico está disponível na pasta `relatorio/`, tanto em formato PDF quanto em seu código-fonte LaTeX.

As instruções para compilação, incluindo as dependências do template SBC, estão disponíveis em `relatorio/README.md`.

## 6. Histórico de desenvolvimento

O desenvolvimento, as decisões de implementação, a preparação das instâncias e os experimentos estão documentados nos arquivos do projeto e no histórico de utilização de IA.

Os resultados apresentados no artigo foram obtidos a partir das execuções experimentais registradas no repositório.