# Architecture Cleanup Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Melhorar a modularidade, legibilidade, testabilidade e documentação do projeto sem alterar a contribuição científica atual: uma plataforma reprodutível para priorização de alvos de exoplanetas com evidência calibrada, incerteza e validação externa.

**Architecture:** Preservar as interfaces públicas, os comandos de reprodução e os artefatos científicos, mas reduzir concentração de responsabilidades. A arquitetura alvo separa orquestração, modelos científicos, geração de candidatos, comparações experimentais, validação externa, escrita de artefatos, tabelas/figuras e documentação arquitetural.

**Tech Stack:** Python 3.11+, pandas, numpy, PyYAML, pytest, matplotlib/seaborn, React/Vite, Markdown, GitHub Actions.

---

## 1. O Que Queremos

Queremos preparar o repositório para um ciclo de publicação científica e manutenção colaborativa. A base atual já tem método científico, validação e pacote de reprodução; o próximo passo é deixar o código mais claro para revisores, coautores e futuros agentes de implementação.

O resultado esperado desta refatoração é:

- módulos pequenos com responsabilidade única;
- nomes explícitos para contratos científicos e artefatos;
- testes organizados pelo comportamento que protegem;
- documentação que explica a arquitetura antes de explicar comandos;
- política clara para artefatos gerados e arquivos grandes;
- histórico Git em commits pequenos, revisáveis e reversíveis.

## 2. Diagnóstico Arquitetural Atual

Esta revisão foi feita a partir da estrutura local do repositório em `/home/maiconkevyn/PycharmProjects/exoplanets_research`.

### Pontos Fortes

- O pacote principal já vive em `src/exoplanets_research/`, com domínios separados para `data`, `habitability`, `uncertainty`, `validation`, `paper` e `experiments`.
- A pipeline já expõe artefatos científicos importantes: ranking, incerteza, validação externa, tabelas e figuras.
- Existem testes cobrindo pipeline, scoring, modelos de zona habitável, incerteza e geração de artefatos.
- O projeto já tem documentação científica relevante em `docs/research/`, `docs/validation/`, `docs/architecture/` e `paper/`.

### Riscos De Manutenção

- `src/exoplanets_research/experiments/run_ablation.py` concentra muitas responsabilidades em um arquivo: manifesto, montagem de candidatos, comparações de zona habitável, baselines, sensibilidade de score, validação externa, checksums, escrita de inventário, geração de tabelas e CLI.
- `src/exoplanets_research/pipeline.py` mistura orquestração da pipeline com escrita de proveniência, JSON para frontend e acionamento de artefatos de paper.
- `src/exoplanets_research/paper/figures.py` mistura geração de figuras com serialização genérica de tabelas Markdown.
- `tests/test_pipeline_outputs.py` cresceu para cobrir muitos comportamentos diferentes, o que dificulta localizar falhas e entender intenção.
- Scripts exploratórios legados ainda vivem diretamente em `src/` com nomes como `01_initial_exploration.py`, fora do namespace do pacote.
- Artefatos grandes gerados, como amostras de incerteza e JSON do frontend, pressionam o histórico Git e precisam de política explícita.

## 3. Princípios Da Refatoração

- Preservar comportamento antes de mudar estrutura.
- Refatorar em commits pequenos, um eixo por commit.
- Não alterar fórmulas científicas junto com reorganização de código.
- Manter comandos públicos funcionando.
- Criar testes antes ou durante cada extração de módulo.
- Documentar decisões arquiteturais no mesmo PR/commit da mudança.
- Não remover artefatos científicos versionados sem uma política documentada e uma migração explícita.

## 4. Arquitetura Alvo

```text
src/exoplanets_research/
  data/
    archive.py
    cleaning.py
    outputs.py
  experiments/
    __init__.py
    artifacts.py
    candidates.py
    comparisons.py
    external_validation.py
    manifest.py
    run_ablation.py
  habitability/
    features.py
    habitable_zone.py
    hz_models.py
    scoring.py
  io/
    provenance.py
  paper/
    figures.py
    tables.py
  pipeline.py
  uncertainty/
    monte_carlo.py
  validation/
    baselines.py
    external_targets.py
```

`run_ablation.py` deve virar um orquestrador fino de CLI. `pipeline.py` deve continuar sendo a entrada principal de pipeline, mas sem conhecer detalhes de escrita de cada artefato.

## 5. Tarefas De Implementação

### Task 1: Documentar Fronteiras Arquiteturais

**Objetivo:** Criar uma referência curta e revisável sobre como os módulos devem se relacionar.

**Files:**
- Create: `docs/architecture/codebase_modularity_review.md`
- Modify: `README.md`

- [ ] Criar `docs/architecture/codebase_modularity_review.md` com estas seções:
  - mapa de fluxo: archive snapshot -> features -> scoring -> uncertainty -> validation -> paper artifacts -> frontend;
  - ownership por módulo;
  - entradas públicas de CLI;
  - artefatos versionados;
  - riscos conhecidos;
  - regras para futuras mudanças.
- [ ] Adicionar link para esse documento no `README.md`, na área de documentação ou reprodução.
- [ ] Validar que os links internos existem.

**Commands:**

```bash
test -f docs/architecture/codebase_modularity_review.md
rg -n "codebase_modularity_review|Arquitetura|Architecture" README.md docs/architecture
git diff -- README.md docs/architecture/codebase_modularity_review.md
```

**Expected Result:** O repositório passa a ter uma visão arquitetural voltada a manutenção, não apenas a reprodução científica.

**Commit:**

```bash
git add README.md docs/architecture/codebase_modularity_review.md
git commit -m "docs: document codebase modularity boundaries"
```

### Task 2: Dividir O Runner Experimental

**Objetivo:** Reduzir `src/exoplanets_research/experiments/run_ablation.py` para um orquestrador de CLI, com lógica movida para módulos especializados.

**Files:**
- Create: `src/exoplanets_research/experiments/manifest.py`
- Create: `src/exoplanets_research/experiments/candidates.py`
- Create: `src/exoplanets_research/experiments/comparisons.py`
- Create: `src/exoplanets_research/experiments/external_validation.py`
- Create: `src/exoplanets_research/experiments/artifacts.py`
- Modify: `src/exoplanets_research/experiments/run_ablation.py`
- Modify: `tests/test_experiment_runner_outputs.py`

- [ ] Mover carregamento de manifesto para `manifest.py`.
- [ ] Mover construção de candidatos, ranking e enriquecimento de features para `candidates.py`.
- [ ] Mover comparação de HZ, baselines e sensibilidade para `comparisons.py`.
- [ ] Mover validação externa, inventário e checksum para `external_validation.py`.
- [ ] Mover escrita de artefatos de paper para `artifacts.py`.
- [ ] Manter `run_ablation.py` como fachada com `main()` e funções públicas compatíveis, quando necessário.
- [ ] Atualizar imports dos testes sem alterar o comportamento esperado.

**Commands:**

```bash
.venv/bin/python -m pytest tests/test_experiment_runner_outputs.py -q
.venv/bin/python -m pytest -q
python -m exoplanets_research.experiments.run_ablation --help
```

**Expected Result:** A CLI continua respondendo, os testes passam e cada módulo novo tem responsabilidade clara.

**Commit:**

```bash
git add src/exoplanets_research/experiments tests/test_experiment_runner_outputs.py
git commit -m "refactor: split experiment runner responsibilities"
```

### Task 3: Separar Tabelas De Figuras No Pacote De Paper

**Objetivo:** Deixar `figures.py` apenas com plotagem e criar um módulo próprio para tabelas Markdown.

**Files:**
- Create: `src/exoplanets_research/paper/tables.py`
- Modify: `src/exoplanets_research/paper/figures.py`
- Modify: `src/exoplanets_research/experiments/artifacts.py`
- Create: `tests/test_paper_tables.py`
- Modify: `tests/test_paper_figures.py`

- [ ] Criar `write_markdown_table` em `paper/tables.py`.
- [ ] Criar `write_top_candidate_table` em `paper/tables.py` como API dedicada para a tabela de candidatos prioritários.
- [ ] Remover serialização de Markdown de `figures.py`.
- [ ] Garantir que `figures.py` só contenha funções de plotagem.
- [ ] Cobrir a saída Markdown em teste unitário dedicado.

**Commands:**

```bash
.venv/bin/python -m pytest tests/test_paper_figures.py tests/test_paper_tables.py -q
.venv/bin/python -m pytest -q
```

**Expected Result:** O pacote `paper` fica dividido por tipo de artefato: tabela em `tables.py`, visualização em `figures.py`.

**Commit:**

```bash
git add src/exoplanets_research/paper src/exoplanets_research/experiments tests/test_paper_figures.py tests/test_paper_tables.py
git commit -m "refactor: split paper tables from figures"
```

### Task 4: Isolar Escrita De Artefatos Da Pipeline

**Objetivo:** Transformar `pipeline.py` em orquestração, retirando detalhes de escrita de proveniência, frontend e artefatos.

**Files:**
- Create: `src/exoplanets_research/data/outputs.py`
- Create: `src/exoplanets_research/io/provenance.py`
- Modify: `src/exoplanets_research/pipeline.py`
- Modify: `tests/test_pipeline_outputs.py`

- [ ] Mover escrita de CSV/JSON/proveniência para funções nomeadas em `data/outputs.py` e `io/provenance.py`.
- [ ] Manter em `pipeline.py` apenas a ordem do fluxo e a composição das funções.
- [ ] Remover imports internos usados apenas para evitar acoplamento circular depois que os writers forem extraídos.
- [ ] Preservar nomes e localização dos artefatos gerados.
- [ ] Manter a assinatura pública de `run_pipeline` estável nesta task.

**Commands:**

```bash
.venv/bin/python -m pytest tests/test_pipeline_outputs.py -q
.venv/bin/python -m pytest -q
python -m exoplanets_research.pipeline --help
```

**Expected Result:** A pipeline fica mais legível, com efeitos colaterais localizados em módulos de IO.

**Commit:**

```bash
git add src/exoplanets_research/data src/exoplanets_research/io src/exoplanets_research/pipeline.py tests/test_pipeline_outputs.py
git commit -m "refactor: isolate pipeline artifact writers"
```

### Task 5: Reorganizar Testes Por Responsabilidade

**Objetivo:** Diminuir o custo cognitivo dos testes e tornar falhas mais fáceis de diagnosticar.

**Files:**
- Create: `tests/test_archive.py`
- Create: `tests/test_pipeline_smoke.py`
- Create: `tests/test_pipeline_uncertainty.py`
- Create: `tests/test_pipeline_paper_export.py`
- Modify: `tests/test_pipeline_outputs.py`

- [ ] Mover testes de carregamento/canonicidade de dados para `tests/test_archive.py`.
- [ ] Mover testes de execução mínima da pipeline para `tests/test_pipeline_smoke.py`.
- [ ] Mover testes de incerteza para `tests/test_pipeline_uncertainty.py`.
- [ ] Mover testes de exportação de paper para `tests/test_pipeline_paper_export.py`.
- [ ] Reduzir `tests/test_pipeline_outputs.py` para contratos agregados de saída, ou remover o arquivo quando todos os testes forem movidos.
- [ ] Não alterar fixtures nem asserts durante a movimentação, salvo imports.

**Commands:**

```bash
.venv/bin/python -m pytest tests/test_archive.py tests/test_pipeline_smoke.py tests/test_pipeline_uncertainty.py tests/test_pipeline_paper_export.py -q
.venv/bin/python -m pytest -q
```

**Expected Result:** A cobertura permanece equivalente, mas cada arquivo de teste comunica um contrato claro.

**Commit:**

```bash
git add tests
git commit -m "test: split pipeline coverage by responsibility"
```

### Task 6: Classificar Scripts Exploratórios Legados

**Objetivo:** Remover ambiguidade entre pacote de produção e scripts históricos.

**Files:**
- Create: `scripts/legacy/README.md`
- Move: `src/01_initial_exploration.py` -> `scripts/legacy/01_initial_exploration.py`
- Move: `src/02_exploratory_analysis.py` -> `scripts/legacy/02_exploratory_analysis.py`
- Move: `src/02_preprocessing.py` -> `scripts/legacy/02_preprocessing.py`
- Move: `src/03_habitability_analysis.py` -> `scripts/legacy/03_habitability_analysis.py`
- Move: `src/04_habitable_planet_analysis.py` -> `scripts/legacy/04_habitable_planet_analysis.py`
- Move: `src/05_habitability_scoring.py` -> `scripts/legacy/05_habitability_scoring.py`
- Modify: docs that still reference the old paths.

- [ ] Confirmar referências dos scripts em runtime e docs com `rg`.
- [ ] Mover os scripts com `git mv` para `scripts/legacy/`.
- [ ] Criar `scripts/legacy/README.md` explicando que esses scripts são histórico exploratório e que a pipeline oficial fica em `src/exoplanets_research/`.
- [ ] Atualizar links em documentação encontrados pelo `rg`.

**Commands:**

```bash
rg -n "01_initial_exploration|02_exploratory_analysis|02_preprocessing|03_habitability_analysis|04_habitable_planet_analysis|05_habitability_scoring" .
git mv src/01_initial_exploration.py scripts/legacy/01_initial_exploration.py
git mv src/02_exploratory_analysis.py scripts/legacy/02_exploratory_analysis.py
git mv src/02_preprocessing.py scripts/legacy/02_preprocessing.py
git mv src/03_habitability_analysis.py scripts/legacy/03_habitability_analysis.py
git mv src/04_habitable_planet_analysis.py scripts/legacy/04_habitable_planet_analysis.py
git mv src/05_habitability_scoring.py scripts/legacy/05_habitability_scoring.py
.venv/bin/python -m pytest -q
```

**Expected Result:** `src/` passa a conter apenas pacote ou código ativo, reduzindo confusão para revisores.

**Commit:**

```bash
git add src scripts docs tests
git commit -m "chore: move legacy exploratory scripts"
```

### Task 7: Definir Política Para Artefatos Gerados E Arquivos Grandes

**Objetivo:** Evitar crescimento descontrolado do repositório sem perder reprodutibilidade científica.

**Files:**
- Create: `docs/architecture/artifact_policy.md`
- Modify: `.gitignore`
- Modify: `paper/reproduce.sh`
- Modify: `configs/experiments/paper_v1.yml`

- [ ] Documentar classes de artefatos:
  - pequenos e versionados: tabelas finais, figuras finais, manifests, inventários;
  - reproduzíveis e não versionados: amostras de Monte Carlo, caches, arquivos intermediários;
  - externos e não versionados: catálogos baixados de fontes oficiais;
  - publicação: assets anexados a release, Zenodo ou outro DOI.
- [ ] Migrar a política de amostras completas de Monte Carlo para caminho intermediário não versionado.
- [ ] Manter versionados apenas resumos, tabelas finais, figuras finais, manifests e inventários.
- [ ] Atualizar `paper/reproduce.sh` e `configs/experiments/paper_v1.yml` para gerar amostras completas sob `data/outputs/experiments/paper_v1/intermediate/`.
- [ ] Remover `data/outputs/astrobiology_uncertainty_samples.csv` do índice Git com `git rm --cached`, mantendo o arquivo local quando ele existir.
- [ ] Garantir que `.gitignore` protege apenas novos intermediários e não esconde artefatos finais necessários para o paper.

**Commands:**

```bash
du -h data/outputs/* frontend/src/data/* 2>/dev/null | sort -h
git ls-files data/outputs frontend/src/data
rg -n "uncertainty_samples|astrobiology_ranked_candidates|data/outputs" README.md paper docs configs src tests
git rm --cached data/outputs/astrobiology_uncertainty_samples.csv
.venv/bin/python -m pytest -q
```

**Expected Result:** O projeto tem uma política explícita para artefatos, com reprodutibilidade mantida e menor risco de bloat.

**Commit:**

```bash
git add .gitignore docs/architecture/artifact_policy.md paper/reproduce.sh configs/experiments/paper_v1.yml data frontend src tests
git commit -m "docs: define generated artifact policy"
```

### Task 8: Melhorar Navegação E Documentação Para Revisores

**Objetivo:** Fazer o README apontar para os documentos certos de acordo com o papel do leitor: cientista, desenvolvedor, revisor ou usuário do dashboard.

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture/scientific_platform_architecture.md`
- Modify: `docs/validation/paper_readiness_audit.md`
- Create: `docs/development.md`

- [ ] Reorganizar o README com seções curtas:
  - visão científica;
  - reprodução do paper;
  - arquitetura do código;
  - desenvolvimento local;
  - dados e artefatos;
  - dashboard;
  - citações e limitações.
- [ ] Criar ou atualizar `docs/development.md` com comandos de teste, pipeline, frontend e convenções de commits.
- [ ] Linkar `codebase_modularity_review.md` e `artifact_policy.md`.
- [ ] Garantir que o README não vire uma duplicação longa dos docs internos.

**Commands:**

```bash
rg -n "codebase_modularity_review|artifact_policy|paper_readiness_audit|reproduce" README.md docs
.venv/bin/python -m pytest -q
npm --prefix frontend run build
```

**Expected Result:** O README fica mais legível e atua como índice de navegação para o projeto.

**Commit:**

```bash
git add README.md docs
git commit -m "docs: improve reviewer navigation"
```

### Task 9: Auditoria Final De Legibilidade

**Objetivo:** Confirmar que a refatoração realmente reduziu complexidade e não apenas moveu código.

**Files:**
- Modify: `docs/architecture/codebase_modularity_review.md`
- Modify: `docs/validation/validation_report.md`

- [ ] Gerar contagem de linhas por arquivo Python.
- [ ] Conferir se nenhum módulo novo virou concentração de responsabilidade.
- [ ] Conferir imports circulares.
- [ ] Conferir comandos de reprodução.
- [ ] Atualizar a seção "Post-refactor Review" em `docs/architecture/codebase_modularity_review.md`.
- [ ] Atualizar `docs/validation/validation_report.md` com o resultado da validação final e declarar se houve ou não mudança científica.

**Commands:**

```bash
find src tests -name "*.py" -print0 | xargs -0 wc -l | sort -n
.venv/bin/python -m pytest -q
UNCERTAINTY_RUNS=25 paper/reproduce.sh
npm --prefix frontend run build
git status --short
```

**Expected Result:** O projeto continua reproduzível, com módulos menores, testes passando e documentação alinhada.

**Commit:**

```bash
git add docs src tests README.md paper configs frontend .gitignore
git commit -m "docs: record architecture cleanup validation"
```

## 6. Checkpoints De Qualidade

Use estes checkpoints ao final de cada task:

- [ ] `git diff --check` sem erros.
- [ ] Testes unitários relevantes passando.
- [ ] Nenhum arquivo gerado pesado novo foi adicionado sem intenção.
- [ ] Imports públicos antigos foram preservados ou documentados.
- [ ] README e docs apontam para paths reais.
- [ ] O commit contém uma única ideia revisável.

## 7. Checkpoint Científico

Esta refatoração não deve alterar resultados científicos sem uma tarefa explícita. Para qualquer mudança que afete score, ranking, incerteza, validação externa ou tabelas do paper:

- [ ] comparar top candidatos antes e depois;
- [ ] registrar diffs de métricas;
- [ ] atualizar `docs/validation/validation_report.md`;
- [ ] explicar a mudança no método ou na limitação científica;
- [ ] rodar `UNCERTAINTY_RUNS=25 paper/reproduce.sh` no mínimo.

## 8. Validação Final

Ao concluir todas as tasks, executar:

```bash
git diff --check
.venv/bin/python -m pytest -q
UNCERTAINTY_RUNS=25 paper/reproduce.sh
npm --prefix frontend run build
git status --short
```

Se houver mudança em fórmulas, contratos de dados ou geração final de ranking, executar também uma reprodução completa com o número de rodadas definido em `configs/experiments/paper_v1.yml` e atualizar os artefatos científicos afetados.

## 9. Ordem Recomendada De Execução

1. Documentar fronteiras arquiteturais.
2. Dividir runner experimental.
3. Separar tabelas e figuras.
4. Isolar escrita de artefatos da pipeline.
5. Reorganizar testes.
6. Classificar scripts legados.
7. Definir política de artefatos.
8. Melhorar navegação da documentação.
9. Rodar auditoria final de legibilidade.

Essa ordem minimiza risco porque primeiro cria contexto, depois refatora os pontos de maior concentração, e só então mexe em documentação ampla e política de artefatos.
