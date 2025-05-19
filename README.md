# Simulação do Algoritmo de Estado de Enlace com Docker e Python

## 📚 Sobre o Projeto

Este projeto é uma simulação de uma rede de computadores utilizando o algoritmo de **Estado de Enlace** (Link State Routing Algorithm).  
O sistema é composto por **hosts** e **roteadores**, implementados em **Python** e executados em containers separados com **Docker**.

Cada roteador:
- Mantém uma **Base de Dados de Estado de Enlace** (LSDB).
- Calcula as rotas mais curtas usando o **Algoritmo de Dijkstra**.
- Troca informações de estado de enlace com seus vizinhos usando **UDP**.

## ⚙️ Tecnologias Utilizadas

- Python 3.10
- Docker
- Docker Compose
- NetworkX (para grafos)
- Sistema de sockets UDP

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/DEVFlavioLima7/avalia--o_redesII_pronta
   
   cd avalia--o_redesII_pronta



2.Construa e execute os containers:

    docker-compose up --build


3. Verifique a comunicação:

   -Os hosts tentarão se comunicar entre si usando ping.

   -Os roteadores trocam pacotes de estado de enlace a cada 5 segundos.

    -As tabelas de roteamento são atualizadas automaticamente conforme novas informações são recebidas.


4- Para parar os containers:

    docker-compose down


##  Justificativa do Protocolo Utilizado (UDP)

    O protocolo UDP foi escolhido para a transmissão dos pacotes de estado de enlace devido às seguintes razões:

    - Menor sobrecarga em comparação ao TCP (não há necessidade de conexão ou confirmação de recebimento).

    - Ideal para envio periódico de atualizações, mesmo que eventuais perdas de pacotes possam ocorrer.

    - Adequado para sistemas de roteamento em tempo real, onde a velocidade de disseminação da informação é mais crítica do que a garantia de entrega de cada pacote.


## Como a Topologia foi Construída

    A rede é composta por:

    - 5 roteadores: router1,router2,router3,router4 e router5

    - 10 hosts: host1,host1b,host2,host2b,host3,host3b,host4,host4b,host5,host5b

    - Cada roteador é conectado a 2 hosts, formando uma subrede privada.

    - Os roteadores estão conectados entre si em uma rede backbone separada.
    -Redes privadas (subnetes) entre cada host e seu roteador

    - Uma topologia parcialmente conectada entre roteadores, simulando a necessidade de descobrir caminhos múltiplos



