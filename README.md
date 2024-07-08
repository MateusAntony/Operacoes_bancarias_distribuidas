# Operações bancárias distribuidas
**Autor**:Mateus Antony Medeiros Carvalho

**Departamento de Tecnologia** – Universidade Estadual de Feira de Santana (UEFS) 44036–900 – Feira de Santana – Bahia

**Objetivo:** Projeto desenvolvido para disciplina de MI - CONCORRÊNCIA E CONECTIVIDADE (TP03) do curso de Engenharia de Computação. É um sistema de bancos distribuido onde ele permitirá fazer transações específicas de forma segura, gerenciamento de contas e tratar transações distribuidas de forma com concorrente.

## Índice
1. [Introdução](#introducao)
2. [Desenvolvimento](#desenvolvimento)
    - [ Gerenciamento de contas](#gerenciamento-de-contas)
    - [ Processo de transferência entre diferentes contas](#processo-de-transferência-entre-diferentes-contas)
    - [ Comunicação entre servidores](#comunicação-entre-servidores)
    - [ Sincronização em um único servidor](#sincronização-em-um-único-servidor)
    - [ Algoritmo de concorrência distribuída](#algoritmo-de-concorrência-distribuída)
    - [ Confiabilidade](#confiabilidade)
3. [Conclusão](#conclusão)
4. [Como Usar](#como-usar)



<a id="introducao"></a>
## 1. Introdução
Atualmente, grande parte dos clientes de bancos tem adotado a utilização de transações financeiras por dispositivos móveis. O pix, por exemplo, simplifica todo o processo de movimentação financeira, além de proporcionar a inclusão de brasileiro sem cartão de creditos.

Nesse sentido, um governo de um país específico, no qual não possui banco central, busca desenvolver um sistema que se assemelha ao pix, possibilitando as operações de tranferências, pagamentos e deposito,além depossibilitar a criação de contas bancárias. Assim, já que não possui um banco central, não deve utilizar recursos centralizados para o controle das transações.

Sendo assim, esse consórcio bancário deve ser capaz de realizar transferências atômicas envolvendo contas de outros bancos, evitando problemas com os dinheiros das contas.
 
<a id="desenvolvimento"></a>
## 2. Desenvolvimento

No desenvolvimento da solução foi utilizado o framework Flask para a crição da ApiRestful, junto com isso foi utilizado para comunicação entre os servidores dos bancos o protocolo HTTP.

Foi elaborado uma Api para cada banco durante o desenvovimento do projeto, foi analisado uma maneira melhor de simplificar a codificação e a utilização do docker, por isso foi criado três arquivos de banco semelhantes com intuito de simplificar no momento de teste. Além disso o projeto possui um interface que executa no terminal para testar as funcionalidades.

Como meio de simplificar a comunicação entre os bancos, foi elaborado a solução com cada banco conhecendo os demais bancos e suas urls, sendo assim, ao executar a imagem do docker passamos os endenreços de ip dos bancos. 

<a id="gerenciamento-de-contas"></a>
## 2.1. Gerenciamento de contas

O sistema permite a criação de contas físicas, contas jurídicas e contas conjuntas. Vale ressaltar que só há possibilidade de criar uma conta por CPF cadastrado, exceto conta conjunta, ou seja, se você já tiver cadastrado uma conta com um determinado CPF e quiser criar outra com o mesmo CPF, só será possível criar uma conta conjunta.

O sistema realiza transferência,deposito e pagamento de maneira correta, contendo a possibilidade de transferir para contas do mesmo banco e para contas de diferentes bancos. As transações são preparadas, confirmadas e em caso de erro são revertidas. Vale mencionar que as transações de pagamento e deposito são consideradas uma transferencias,  nesse sentido foi utilizado o mesmo endpoint para lidar com essas transações.

<a id="processo-de-transferência-entre-diferentes-contas"></a>
## 2.2. Processo de transferência entre diferentes contas

O processo de tranferência a feito através da utilização do algoritmo 2-Phase Commit (2PC). Nesse sentido, inicialmente iremos preparar todas as contas que irão ter valores retirados, isso é feito analisando o tipo de banco que pertence a conta especificada, se for do próprio banco local solucionaremos chamando os métodos do algoritmo 2PC, contudo se for de bancos externos iremos comparar o nome do banco com lista de bancos disponiveis para recuperar url específica. Por fim, elaboramos o payload e fazemos a requisição para rota do banco que lida com a fase do preparo. Isso é repetido na fase confirmação para finalizar as retiradas dos valores. Logo abaixo está uma imagem que mostra um pedido de transferência envolvendo três bancos diferentes.

<p align="center">
  <img src="https://github.com/MateusAntony/Operacoes_bancarias_distribuidas/raw/main/assets/68971638/f542ffb3-3ea6-4e9e-96f0-c0a0776522a8.png" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 2: Saída após fazer um transferência do envolvendo banco a, banco b e banco c. 
</p>

Ademais, observando o comportamento da solução é evidenciado que o sistema cumpre o processo de transferencia para diferentes contas, sejam eleas do mesmo banco ou de bancos diferentes.

<a id="Comunicação_entre_servidores"></a>
## Comunicação entre servidores

<a id="Sincronização_em_um_único_servidor"></a>
## Sincronização em um único servidor

<a id="Algoritmo_de_concorrencia_distribuída"></a>
## Algoritmo de concorrencia distribuída

<a id="Confiabilidade"></a>
## Confiabilidade

<a id="Conclusão"></a>
## Conclusão

<a id="Como_Usar"></a>
## Como Usar
