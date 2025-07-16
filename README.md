## Flappy Bird em Python com Pygame 
Um clone simples do clássico jogo Flappy Bird, desenvolvido em Python usando a biblioteca Pygame. Este projeto foi criado com foco no aprendizado de lógica de jogos, manipulação de sprites e gerenciamento de estados.

# Visão Geral 
Controle um pássaro (tucano) através de uma floresta cheia de árvores (canos) em movimento. O objetivo é voar o mais longe possível sem colidir com as árvores ou cair no chão. A velocidade do jogo aumenta à medida que sua pontuação cresce, tornando o desafio ainda maior!

# Como Jogar 
Pular: Pressione a barra de espaço para fazer o pássaro bater as asas e subir.

Movimento: O pássaro cai automaticamente devido à gravidade.

Objetivo: Passe pelos espaços entre as árvores para ganhar pontos.

Game Over: O jogo termina se o pássaro colidir com uma árvore ou tocar o chão.

Reiniciar: Após o "Game Over", pressione a barra de espaço novamente para começar uma nova partida.

# Funcionalidades
Pássaro Controlável: Movimento de queda por gravidade e pulo responsivo.

Geração de Árvores (Canos): Árvores (canos) que aparecem aleatoriamente e se movem da direita para a esquerda.

Colisão: Detecção precisa de colisão com as árvores e o chão.

Sistema de Pontuação: Acompanha os pontos do jogador.

Dificuldade Dinâmica: A velocidade das árvores aumenta gradualmente com a pontuação.

Gerenciamento de Estados: Transição entre os estados "Jogando" e "Game Over".

Reiniciar Jogo: Opção para reiniciar a partida após o "Game Over".

Gráficos Personalizados: Imagens para o tucano e os troncos de árvore.

Fundo Rolante: Imagem de fundo de floresta que se move para dar a sensação de progresso.

# Requisitos
Para executar este jogo, você precisará ter o Python instalado e a biblioteca Pygame.

Python 3.x

Pygame

# Como Executar
Clone o Repositório (se estiver em um):

`
git clone [URL_DO_SEU_REPOSITORIO]
cd [pasta_do_seu_projeto]
`

(Se você estiver apenas com o arquivo Python, pule esta etapa.)

# Instale o Pygame:
Abra seu terminal ou prompt de comando e execute:

`
pip install pygame
`

Organize os Ficheiros de Imagem:
Crie uma pasta chamada assets no mesmo diretório do seu ficheiro main.py (ou como você nomeou o seu script principal). Coloque as imagens tucano.jpg, arvore.jpg e fundo_floresta.jpg dentro desta pasta assets.

Sua estrutura de ficheiros deve ser assim:

`
jogo.py
    tucano.jpg
    arvore.jpg
    fundo_floresta.jpg
`

# Execute o Jogo:
No seu terminal ou prompt de comando, navegue até o diretório do seu ficheiro Python e execute:

python seu_jogo.py

(Substitua seu_jogo.py pelo nome real do seu ficheiro.)

Créditos
Desenvolvimento: [Gabriel]
