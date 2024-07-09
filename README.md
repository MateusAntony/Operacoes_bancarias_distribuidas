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
Atualmente, grande parte dos clientes de bancos tem adotado a utilização de transações financeiras por dispositivos móveis. O Pix, por exemplo, simplifica todo o processo de movimentação financeira, além de proporcionar a inclusão de brasileiros sem cartão de crédito.

Nesse sentido, um governo de um país específico, que não possui banco central, busca desenvolver um sistema semelhante ao Pix, permitindo operações de transferências, pagamentos e depósitos, além de possibilitar a criação de contas bancárias. Assim, como não possui um banco central, não deve utilizar recursos centralizados para o controle das transações.

Sendo assim, esse consórcio bancário deve ser capaz de realizar transferências atômicas envolvendo contas de outros bancos, evitando problemas com os saldos das contas.
 
<a id="desenvolvimento"></a>
## 2. Desenvolvimento
No desenvolvimento da solução foi utilizado o framework Flask para a criação da API Restful. Além disso, foi utilizado o protocolo HTTP para comunicação entre os servidores dos bancos.

Foi elaborada uma API para cada banco durante o desenvolvimento do projeto. Foi analisada uma maneira melhor de simplificar a codificação e a utilização do Docker, por isso foram criados três arquivos de banco semelhantes com o intuito de simplificar os testes. Além disso, o projeto possui uma interface que executa no terminal para testar as funcionalidades.

Como meio de simplificar a comunicação entre os bancos, a solução foi elaborada com cada banco conhecendo os demais bancos e suas URLs. Dessa forma, ao executar a imagem do Docker, passamos os endereços de IP dos bancos.

<a id="gerenciamento-de-contas"></a>
## 2.1. Gerenciamento de contas

O sistema permite a criação de contas físicas, contas jurídicas e contas conjuntas. Vale ressaltar que só há possibilidade de criar uma conta por CPF cadastrado, exceto contas conjuntas. Ou seja, se você já tiver cadastrado uma conta com um determinado CPF e quiser criar outra com o mesmo CPF, só será possível criar uma conta conjunta.

O sistema realiza transferências, depósitos e pagamentos de maneira correta, incluindo a possibilidade de transferir para contas do mesmo banco e para contas de diferentes bancos. As transações são preparadas, confirmadas e, em caso de erro, são revertidas. Vale mencionar que as transações de pagamento e depósito são consideradas transferências, sendo utilizado o mesmo endpoint para lidar com essas transações.

<a id="processo-de-transferência-entre-diferentes-contas"></a>
## 2.2. Processo de transferência entre diferentes contas

O processo de transferência é realizado através da utilização do algoritmo Two-Phase Commit (2PC). Inicialmente, todas as contas que terão valores retirados são preparadas. Isso é feito analisando o tipo de banco ao qual a conta pertence. Se for do próprio banco local, as operações são tratadas diretamente. Se forem de bancos externos, são comparados os nomes dos bancos com uma lista de bancos disponíveis para recuperar a URL específica. Em seguida, é elaborado o payload e feita a requisição para a rota do banco que lida com a fase de preparo. Este processo é repetido na fase de confirmação para finalizar as retiradas dos valores.

<p align="center">
   <img src="https://github.com/MateusAntony/Operacoes_bancarias_distribuidas/assets/68971638/17be8930-e9d2-4421-9e9e-4132d1c946c0" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 1: Realizando transferencia envolvendo banco a, banco b e banco c. 
</p>

<p align="center">
   <img src="https://github.com/MateusAntony/Operacoes_bancarias_distribuidas/assets/68971638/196834f4-62da-40a5-9ac2-f0dcfd73de56" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 1: Analisando se os valores foram retirados corretamente
</p>


Ademais, observando o comportamento da solução, é evidenciado que o sistema cumpre o processo de transferência para diferentes contas, sejam elas do mesmo banco ou de bancos diferentes.

<a id="Comunicação_entre_servidores"></a>
## Comunicação entre servidores

O sistema utiliza do protocolo HTTP para comunicação entre os bancos.

<a id="Sincronização_em_um_único_servidor"></a>
## Sincronização em um único servidor

A concorrência em um único servidor é tratada com o uso de locks. Cada conta tem seu próprio lock, garantindo que apenas uma transação por vez possa modificar o saldo da conta. Dessa forma, se duas transações envolvendo contas diferentes chegarem ao servidor ao mesmo tempo, ambas serão realizadas simultaneamente. No entanto, se duas transações envolverem a mesma conta, uma delas será bloqueada até que a outra seja concluída.

<a id="algoritmo-de-concorrência-distribuída"></a>
## Algoritmo de concorrencia distribuída

Foi implementado o algoritmo Two-Phase Commit (2PC), que garante a consistência de dados em sistemas distribuídos, além de garantir atomicidade. Consiste em três processos: 

- Preparação: Bloqueio da conta e verificação se há saldo suficiente para realizar a transferência. Se houver saldo suficiente, a transação é registrada na lista de transações preparadas.
- Confirmação: Bloqueio da conta e verificação se a conta especificada está na lista de transações preparadas. Ao encontrar, ela é removida da lista e declarada como confirmada.
- Rollback: Desfaz as alterações temporárias se algum erro acontecer durante a transação, ou se alguma das contas não puder realizar a transação.

<a id="Confiabilidade"></a>
## Confiabilidade

OO sistema verifica o status dos bancos envolvidos na transação. Se um deles estiver desconectado, a transação não é realizada. Além disso, se o banco ao qual o usuário estiver conectado for desconectado, ele não conseguirá executar nenhuma funcionalidade até que retorne ao funcionamento normal.

<p align="center">
   <img src="https://github.com/MateusAntony/Operacoes_bancarias_distribuidas/assets/68971638/f59858f6-9a4c-4f0d-8f89-03d4e5584cbf" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 3: Verificação do status dos bancos envolvidos na transferência.
</p>

<p align="center">
   <img src="https://github.com/MateusAntony/Operacoes_bancarias_distribuidas/assets/68971638/258f2976-76b4-4bd6-bef9-72e1b29acefd" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 4: Função de verificação do status.
</p>

<a id="Conclusão"></a>
## Conclusão

Ao analisar a solução desenvolvida, observa-se que grande parte dos requisitos foi cumprida. Um sistema de bancos distribuídos funciona de maneira concorrente, utilizando containers Docker para conclusão do sistema.

<a id="Como_Usar"></a>
## Como Usar
1. Execute os arquivos do banco_a, banco_b e banco_c, passando os ip's para de cada banco externo, como mostrado no exemplo abaixo que é executado o banco_a:

`Docker run --network=host -it -e ipb=ip_banco_b ipc=ip_banco_c nome_da_imagem`

