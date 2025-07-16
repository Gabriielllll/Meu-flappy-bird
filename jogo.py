import pygame
import random
import os


#Resolução
largura_tela = 800
altura_tela = 600


pygame.init()
pygame.font.init()
#onde acontece o que há na tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
#Nome da janela
pygame.display.set_caption(" Meu Flappy Bird")


#Dimensões passaro
Largura_passaro = 68
Altura_passaro = 48
Cor_passaro = (255, 165, 0)

#Cano
Largura_cano = 75
Altura_espaço = 150

Cor_cano = (139,69,19)

#Céu
Cor_de_fundo = (126, 140, 84)
imagem_fundo = None
fundo_x = 0 # Posição X inicial do fundo para rolagem
try:
    # Carrega a imagem real do fundo da floresta
    fundo_original = pygame.image.load(os.path.join('fundo_floresta.jpg')).convert() # Não precisa de alpha se não tiver transparência
    # Redimensiona o fundo para preencher a tela
    imagem_fundo = pygame.transform.scale(fundo_original, (largura_tela, altura_tela))
except pygame.error as e:
    print(f"Erro ao carregar imagem de fundo: {e}")
    # Se a imagem não carregar, 'imagem_fundo' permanecerá None


#Variáveis de movimentação
#Gravidade
velocidade_y = 0
gravidade = 0.25
força_de_pulo = -5


#Controle de gráficos e processamento de eventos
FPS = 30
clock = pygame.time.Clock()

#Velocidade dos canos(inicial e máxima)
Velocidade_cano_inicial = 5
Velocidade_cano_max = 15
velocidade_cano_atual = Velocidade_cano_inicial

#Constantes de espaçamen to horizontal dinâmico
Min_espaçamento_horizontal = 250
Max_espaçamento_horizontal = 400

#Faixa de Y para o centro do espaço do cano
Y_min_gap_center = 200
Y_max_gap_center = 500
Y_mid_gap_center = (Y_min_gap_center + Y_max_gap_center) / 2



imagem_tucano = None
try:
    # Carrega a imagem real do tucano
    imagem_tucano_original = pygame.image.load(os.path.join('tucano.jpg')).convert_alpha()
    imagem_tucano = pygame.transform.scale(imagem_tucano_original, (Largura_passaro, Altura_passaro))
except pygame.error as e:
    print(f"Erro ao carregar imagem do tucano: {e}")
    # Se a imagem não carregar, 'imagem_tucano' permanecerá None

#Carregamento e redimensionamento da árvore
imagem_arvore_original = None
try:
    # Carrega a imagem real da árvore
    imagem_arvore_original = pygame.image.load(os.path.join('tronco.jpg')).convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar imagem da árvore: {e}")
    # Se a imagem não carregar, 'imagem_arvore_original' permanecerá None

#Objeto rect do passaro, e sua localização inicial
passaro_x = 50
passaro_y = 300
if imagem_tucano:
    Passaro_rect = imagem_tucano.get_rect(topleft=(passaro_x, passaro_y))
else:
    Passaro_rect = pygame.Rect(passaro_x, passaro_y, Largura_passaro, Altura_passaro)

#Lista para inserção de canos
canos = []

#Variáveis do jogo
Jogando = 0 
Game_over = 1
estado_jogo = Jogando

#Sistema de pontos
pontuação = 0


#Função dos canos
def criar_cano():
    #Espaço entre a posição Y e o centro do espaço entre os canos
    y_centro_espaço = random.randint(Y_min_gap_center, Y_max_gap_center)

    #Calculo da dimensão do Arvore de cima
    #Começa em Y = 0 e vai até a parte superior do espaço
    cano_cima_altura = y_centro_espaço - (Altura_espaço/2)
    cano_cima_rect = pygame.Rect(largura_tela, 0, Largura_cano, cano_cima_altura)

    #Redimensionamento da imagem para cada cano UMA VEZ
    imagem_cano_cima = None
    if imagem_arvore_original:
        # Certifique-se de que a altura seja um inteiro positivo
        altura_redimensionada = max(1, int(cano_cima_altura)) 
        imagem_cano_cima = pygame.transform.scale(imagem_arvore_original, (Largura_cano, altura_redimensionada)).convert_alpha()
    #calculo do cano de baixo, começa na parte inferior e vai até o chão da tela


    cano_baixo_y = y_centro_espaço + (Altura_espaço/2)
    cano_baixo_altura = altura_tela - cano_baixo_y
    cano_baixo_rect = pygame.Rect (largura_tela, cano_baixo_y, Largura_cano, cano_baixo_altura)

    imagem_cano_baixo = None
    if imagem_arvore_original:
        # Certifique-se de que a altura seja um inteiro positivo
        altura_redimensionada = max(1, int(cano_baixo_altura))
        imagem_cano_baixo = pygame.transform.scale(imagem_arvore_original, (Largura_cano, altura_redimensionada)).convert_alpha()

    #Calculo de espaçamento horizontal para o próximo cano
    diff_from_mid = abs(y_centro_espaço - Y_mid_gap_center)
    normalized_diff = (diff_from_mid/ (Y_max_gap_center - Y_mid_gap_center))

    proximo_espaçamento_horizontal = int(Min_espaçamento_horizontal + (Max_espaçamento_horizontal - Min_espaçamento_horizontal) * normalized_diff)


    #Retorna os dois objetos Rect, e um flag indicando que ainda não foi pontuado
    return cano_cima_rect, cano_baixo_rect, False, proximo_espaçamento_horizontal, imagem_cano_cima, imagem_cano_baixo #Adicionado flag foi 'pontuado'

def Reiniciar_jogo():
    global Passaro_rect, velocidade_y, canos, estado_jogo, pontuação, velocidade_cano_atual
    if imagem_tucano:
        Passaro_rect = imagem_tucano.get_rect(topleft=(passaro_x, passaro_y))
    else:
        Passaro_rect.y = passaro_y
    Passaro_rect.y = passaro_y
    velocidade_y = 0
    canos.clear()
    canos.append(criar_cano())
    pontuação = 0
    velocidade_cano_atual = Velocidade_cano_inicial
    estado_jogo = Jogando

fonte_game_over = pygame.font.Font(None, 74)
fonte_pontuação = pygame.font.Font(None, 50)

#Adiciona o primeiro par de canos para iniciar o jogo
canos.append(criar_cano())



#Loop do jogo
rodando =  True #Variável de controle para verificar se o jogo está rodando

while rodando:
    #Processamento de eventos
    #   Itera sobre todos os eventos que ocorrem (cliques, teclas pressionadas)
    for evento in pygame.event.get():
        #Para o usuário fechar a janela e encerrar o loop
        if evento.type == pygame.QUIT:
            rodando = False
        #Tecla de evento pressionada
        if evento.type == pygame.KEYDOWN:
            #Verifica se é a tecla de espaço
            if evento.key == pygame.K_SPACE:
                #sendo espaço ele vai aplicar força de pulo
                velocidade_y = força_de_pulo
                #Enquanto o jogo estiver ativo espaço fara pular    
                if estado_jogo == Jogando:
                    velocidade_y = força_de_pulo
                #Se o jogo estiver no fim, o espaço fara o jogo reiniciar
                elif estado_jogo == Game_over:
                    Reiniciar_jogo()

    if estado_jogo == Jogando:
#Aplicação de gravidade ao pássaro para cair
        velocidade_y += gravidade

#Atualização da posição Y com base na velocidade vertical
        Passaro_rect.y += velocidade_y

# Limitação do pássaro para dentro da tela
        if Passaro_rect.y < 0:
            Passaro_rect.y = 0 # Coloca o pássaro de volta na borda superior
            velocidade_y = 0 #Para a velocidade vertical para cima
#Restringir movimento do pássaro
    #Limite inferiror, se ele tenta sair da tela o colocará na base do chão
        if Passaro_rect.y + Altura_passaro > altura_tela:
            Passaro_rect.y = altura_tela - Altura_passaro
            velocidade_y = 0
        #Se o pássaro cair no chão é game over
            estado_jogo = Game_over
            velocidade_y = 0 #Para o pássaro após a colisão 

#Movimento do cano
#Itera sobre cada par de canos na lista 'canos'
#Possível erro
        canos_para_remover = []
        #Usado enumerate para poder atualizar a tupla da lista
        for i, (cano_cima, cano_baixo, foi_pontuado, proximo_espaçamento_horizontal, imagem_cano_cima, imagem_cano_baixo) in enumerate(canos):
            #Move cada cano para esquerda
            cano_cima.x -= velocidade_cano_atual
            cano_baixo.x -= velocidade_cano_atual

            #Detecção de colisão
            if Passaro_rect.colliderect(cano_cima) or Passaro_rect.colliderect(cano_baixo):
                estado_jogo = Game_over
                velocidade_y = 0


            if not foi_pontuado and cano_cima.right < Passaro_rect.left:
                pontuação += 1
                #Atualiza a flag de pontuação para este cano
                canos [i] = (cano_cima, cano_baixo, True, proximo_espaçamento_horizontal, imagem_cano_cima, imagem_cano_baixo)
                #Aumenta a velocidade do cano, mas não excede o máximo
                if velocidade_cano_atual < Velocidade_cano_max:
                    velocidade_cano_atual += 0.5
            
            if cano_cima.right < 0:
                canos_para_remover.append((cano_cima, cano_baixo, foi_pontuado, proximo_espaçamento_horizontal, imagem_cano_cima, imagem_cano_baixo))
        
        for cano_removido in canos_para_remover:
            canos.remove(cano_removido)


        #Geração de canos através do espaçamento dinâmico
        if len(canos) == 0:
            canos.append(criar_cano())
        else:
            #Pega espaçamento horizontal do último cano para determinar quando gerar o próximo
            ultimo_cano_espaçamento = canos [-1][3]
            if canos[-1][0].x < largura_tela - ultimo_cano_espaçamento and len (canos) < 3:
                canos.append(criar_cano())

#Renderização
#   Preencher a tela com cor de fundo

    if imagem_fundo:
        tela.blit(imagem_fundo, (fundo_x, 0))
        tela.blit(imagem_fundo, (fundo_x + largura_tela, 0)) # Desenha uma segunda imagem para rolagem contínua
    else:
        tela.fill(Cor_de_fundo) # Fallback para cor de fundo se a imagem não carregar

 
    if imagem_tucano:
        tela.blit(imagem_tucano, Passaro_rect)
    else:
        pygame.draw.rect(tela, Cor_passaro, Passaro_rect) # Fallback para retângulo

    # Desenha todos os canos (árvores) da lista
    # Desempacotamento das 6 tuplas
    for cano_cima, cano_baixo, _, _, imagem_cano_cima, imagem_cano_baixo in canos:
        if imagem_cano_cima:
            tela.blit(imagem_cano_cima, cano_cima)
        else:
            pygame.draw.rect(tela, Cor_cano, cano_cima) # Fallback para retângulo

        if imagem_cano_baixo:
            tela.blit(imagem_cano_baixo, cano_baixo)
        else:
            pygame.draw.rect(tela, Cor_cano, cano_baixo) # Fallback para retângulo
 


    texto_pontuacao_surface = fonte_pontuação.render(f"PONTOS: {pontuação}", True, (0,0,0)) #Cor
    tela.blit(texto_pontuacao_surface, (10,10)) #Posição superior esquerda


    #Exibição de game over
    if estado_jogo == Game_over:
        texto_surface = fonte_game_over.render("GAME OVER", True, (255, 0, 0)) #Texto, antialias, cor vermelha
        texto_rect = texto_surface.get_rect(center=(largura_tela // 2, altura_tela // 2)) # Centraliza o texto
        tela.blit(texto_surface, texto_rect) # Desenha o texto na tela

    #Mensagem para reiniciar
        fonte_reiniciar = pygame.font.Font(None, 36)
        texto_reiniciar_surface = fonte_reiniciar.render("Pressione ESPAÇO para reiniciar", True, (255,255,255))
        texto_reiniciar_rect = texto_reiniciar_surface.get_rect(center=(largura_tela // 2, altura_tela // 2 + 50))
        tela.blit(texto_reiniciar_surface, texto_reiniciar_rect)


#Atualiza a tela:
#   Tudo desenhado na "tela" seja exibido
    pygame.display.flip()

#Controle de FPS
    #Garante que o jogo não passe do FPS desejado, caso o loop termine antes do próximo frame ele espera.
    clock.tick(FPS)

#Finalizar o pygame:
#   Finalizando o loop principal o pygame encerra
pygame.quit()
