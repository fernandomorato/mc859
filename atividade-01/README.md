# MC859 - Atividade 1: MAX-SC-QBF

Este repositório contém o código-fonte e as instâncias da **Atividade 1** da disciplina MC859 - Tópicos em Otimização Combinatória (Unicamp, 2º Semestre de 2025).

O objetivo do projeto é modelar e resolver o problema de maximização de uma função quadrática binária com restrições de cobertura de conjuntos (MAX-SC-QBF). A solução foi implementada em Python utilizando o solver Gurobi.

## Estrutura do Repositório

* `generator.py`: Script responsável por gerar as 15 instâncias do problema, com diferentes tamanhos e padrões estruturais.
* `solver.py`: Script que implementa o modelo matemático de programação linear inteira, lê as instâncias e as resolve usando o Gurobi.
* `instances/`: Diretório onde as instâncias de teste (`.txt`) são salvas pelo gerador.
* `solutions/`: Diretório onde os resultados de cada execução (`.csv`) são salvos pelo solver.
* `relatorio.pdf`: O relatório final da atividade, contendo a descrição do problema, modelo, análise e conclusão.

## Pré-requisitos

Para executar este projeto, é necessário ter o seguinte software instalado e configurado no ambiente:

* **Python 3** (testado com a versão 3.10.12)
* **Gurobi Optimizer** (testado com a versão 12.0.3) e a licença correspondente (ex: acadêmica) devidamente configurada.
* **Pacote Gurobipy** para Python (`pip install gurobipy`).

## Como Executar o Projeto

Siga os passos abaixo para gerar as instâncias e resolver o problema.

### 1. Clonar o Repositório

Primeiro, clone este repositório para a sua máquina local e navegue até o diretório da atividade.

```bash
git clone [https://github.com/fernandomorato/mc859.git](https://github.com/fernandomorato/mc859.git)
cd mc859/atividade-01
````

### 2\. Gerar as Instâncias

Execute o script `generator.py` para criar as 15 instâncias de teste. Elas serão salvas no diretório `instances/`.

```bash
python3 generator.py
```

### 3\. Executar o Solver

Após a geração das instâncias, execute o script `solver.py`. Ele irá processar cada um dos 15 arquivos da pasta `instances/`, com um limite de tempo de 10 minutos por instância.

```bash
python3 solver.py
```

Os resultados de cada execução (valor da solução, gap de otimalidade e tempo de execução) serão salvos em arquivos `.csv` individuais no diretório `solutions/`.

## Autores

  * **Pietro Grazzioli Golfetto** - RA 223694
  * **Luiz Fernando Batista Morato** - RA 223406

<!-- end list -->
