# Relatório TP2 — Algoritmos II
**Universidade Federal de Minas Gerais (UFMG)**

**Aluno:** Vitor Faleiro Campos Alves
**Matrícula:** 2024005920
**Professor:** Renato Vimieiro
**Disciplina:** Algoritmos II

## 1. Organização dos arquivos

Esta pasta contém os arquivos necessários para visualizar, editar e compilar o artigo científico.

- `artigo.tex`: arquivo principal do relatório, contendo todo o texto e a estrutura do artigo.
- `sbc-template.sty`: arquivo de estilo responsável pela formatação do documento conforme o modelo SBC.
- `caption2.sty`: pacote auxiliar utilizado pelo template SBC para configurar a apresentação das legendas de figuras e tabelas.
- `figuras/`: gráficos utilizados no artigo.
- `dados/`: arquivos de dados utilizados na elaboração das tabelas, gráficos e análises apresentadas no relatório.

## 2. Organização dos dados

Os arquivos presentes na pasta `dados/` correspondem aos mesmos resultados gerados durante as análises experimentais do projeto, originalmente armazenados em `data/results/analise/`.

Esses arquivos foram copiados para a pasta do relatório com o objetivo de centralizar os materiais utilizados no artigo e facilitar sua consulta e reprodução, sem a necessidade de acessar a estrutura completa do projeto original.

Portanto, não representam uma nova execução dos experimentos nem uma base de resultados diferente.

## 3. Como compilar o artigo

O documento utiliza o template clássico da Sociedade Brasileira de Computação (SBC).

Para realizar a compilação, é necessário ter uma distribuição LaTeX instalada, como TeX Live ou MiKTeX, além dos pacotes utilizados pelo documento.

**Antes de compilar, verifique se os seguintes arquivos estão na mesma pasta:**

- `artigo.tex`
- `sbc-template.sty`
- `caption2.sty`

O arquivo `sbc-template.sty` contém as definições de formatação do artigo e utiliza o `caption2.sty` como dependência para configurar as legendas.

Com o terminal aberto no diretório do projeto, execute:

```bash
pdflatex artigo.tex
pdflatex artigo.tex
```

A segunda compilação permite atualizar referências, numeração de figuras, tabelas e demais elementos do documento.

## 4. Compilação pelo Overleaf

Também é possível compilar o projeto diretamente pelo Overleaf:

1. Acesse o Overleaf e crie um novo projeto.
2. Selecione a opção de upload de projeto e envie o arquivo ZIP contendo toda esta pasta.
3. Verifique se `artigo.tex` está definido como documento principal.
4. Selecione o compilador pdfLaTeX.
5. Clique em **Recompile** para gerar o PDF.

É importante preservar a estrutura dos diretórios `figuras/` e `dados/`, assim como manter os arquivos de estilo na pasta principal, para que todas as dependências sejam localizadas corretamente.

## 5. Observações finais

O arquivo `artigo.tex` é editável e contém o código-fonte completo do relatório.

A estrutura desta pasta foi preparada para permitir que o artigo seja consultado, editado e compilado independentemente da organização interna do repositório principal do projeto.