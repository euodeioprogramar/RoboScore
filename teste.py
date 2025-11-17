def pontuacao(): 
    tentativas = 0 
    print('Superou o ladrilho inicial? 1- Sim / 2- Não')
    lad_ini = int(input())
    if lad_ini == 1:
        lad_ini = 5 
    else: 
        lad_ini = 0
    print('Quantos ladrilhos até o primeiro checkpoint? (Ladrilho inicial não conta)')
    prim_check = int(input())
    print('Quantas tentativas?')
    print('Primeira tentativa(1) / Segunda tentativa(2) / Terceira tentativa(3) / Não superou(4)')
    tentativas = int(input())
    if tentativas == 1:
        prim_check *= 5
    elif tentativas == 2:
        prim_check *= 3
    elif tentativas == 3:
        prim_check *= 1
    else:
        prim_check = 0
    tentativas = 0
    print('Quantos ladrilhos até o segundo checkpoint?')
    seg_check = int(input())
    print('Quantas tentativas?')
    print('Primeira tentativa(1) / Segunda tentativa(2) / Terceira tentativa(3) / Não superou(4)')
    tentativas = int(input())
    if tentativas == 1:
        seg_check *= 5
    elif tentativas == 2:
        seg_check *= 3
    elif tentativas == 3:
        seg_check *= 1
    else:
        seg_check = 0
    tentativas = 0
    print('Quantos ladrilhos até o terceiro checkpoint?')
    ter_check = int(input())
    print('Quantas tentativas?')
    print('Primeira tentativa(1) / Segunda tentativa(2) / Terceira tentativa(3) / Não superou(4)')
    tentativas = int(input())
    if tentativas == 1:
        ter_check *= 5
    elif tentativas == 2:
        ter_check *= 3
    elif tentativas == 3:
        ter_check *= 1
    else:
        ter_check = 0
    print('Quantos ladrilhos com gap superado?')
    gap = int(input()) * 10
    print('Quantos ladrilhos com lombada superada?')
    lombada = int(input()) * 10
    print('Quantos ladrilhos com rampa superada?')
    rampa = int(input()) * 10
    print('Quantos ladrilhos com intersecção superada?')
    intersec = int(input()) * 10
    print('Quantos obstáculos superados?')
    obstaculo = int(input()) * 20
    print('Quantas gangorras superadas?')
    gangorra = int(input()) * 20
    print('Quantas falhas de progresso?')
    fal_pro = int(input())
    print('Chegou no ladrilho de chegada? 1- Sim / 2- Não')
    lad_cheg = int(input())
    if lad_cheg == 1:  
        lad_cheg = 60 - (5 * fal_pro)
        if lad_cheg < 0:
            lad_cheg = 0
    else:
        lad_cheg = 0
    print('Quantas vítimas vivas resgatadas no lugar certo?')
    vit_viv_cer = int(input()) 
    if vit_viv_cer == 1:
        vit_viv_cer = 1.3
    elif vit_viv_cer == 2:
        vit_viv_cer = 1.3 * 1.3
    else:
        vit_viv_cer = 0
    print('Quantas vítimas vivas resgatadas no lugar errado?')
    vit_viv_err = int(input())
    if vit_viv_err == 1:
        vit_viv_err = 1.1
    elif vit_viv_err == 2:
        vit_viv_err = 1.1 * 1.1
    else:
        vit_viv_err = 0
    print('Quantas vítimas mortas resgatadas no lugar certo?')
    vit_mor_cer = int(input())
    if vit_mor_cer == 1:
        vit_mor_cer = 1.3
    else:
        vit_mor_cer = 0
    print('Quantas vítimas mortas resgatadas no lugar errado?')
    vit_mor_err = int(input())
    if vit_mor_err == 1:
        vit_mor_err = 1.1
    else:
        vit_mor_err = 0
    print('Completou o desafio surpresa? 1- Sim / 2- Não')
    desaf_sur = int(input())
    if desaf_sur == 1:
        desaf_sur = 1.5
    else:
        desaf_sur = 0
    if vit_viv_cer > 0 and vit_mor_cer > 0:
        multiplicador = vit_viv_cer * vit_mor_cer
    elif vit_viv_cer > 0 and vit_mor_err > 0:
        multiplicador = vit_viv_cer * vit_mor_err
    elif vit_viv_err > 0 and vit_mor_cer > 0:
        multiplicador = vit_viv_err * vit_mor_cer
    elif vit_viv_err > 0 and vit_mor_err > 0:
        multiplicador = vit_viv_err * vit_mor_err
    else:
        multiplicador = 1
    if desaf_sur > 0:
        multiplicador *= desaf_sur
    total = (lad_ini + prim_check + seg_check + ter_check + gap + lombada + rampa + intersec + obstaculo + gangorra + lad_cheg) * multiplicador
    return total

equipes = []
pontos = {}

while True:
    equipe = input('Digite as equipes participantes: ')

    if equipe == 'pare':
        break

    equipes.append(equipe) 
    pontos[equipe] = {'round_1': 0, 'round_2': 0, 'round_3': 0}


while True:
    print('O que você quer fazer? 1- Rounds / 2- Olhar Pontuação Geral / 3- Sair')
    acao = int(input())

    if acao == 1:
        while acao == 1:
            print('Qual equipe?')
            print(equipes)
            equipe_selecionada = str(input())
            if equipe_selecionada in equipes:
                print('Qual round? 1- Round 1 / 2- Round 2 / 3- Round 3')
                round = int(input())
                if round == 1:
                    chave_round = 'round_1'
                elif round == 2:
                    chave_round = 'round_2'
                elif round == 3:
                    chave_round = 'round_3'
                else:
                    print('Round inválido!')
                    continue    
                print('A equipe realizou o round? 1- Sim / 2- Não')
                realizou = int(input())
                if realizou == 1:
                    pontuacao_total = pontuacao()
                else:
                    pontuacao_total = 0
                
                pontos[equipe_selecionada][chave_round] = pontuacao_total
                print(f'Pontuação da equipe {equipe_selecionada} no {chave_round}: {pontuacao_total}')
                acao = 0
            else:
                print('Equipe inválida!')

    elif acao == 2:
        print('Pontuação Geral:')
        ranking = []
        for equipe in equipes:
            r1 = pontos[equipe]['round_1']
            r2 = pontos[equipe]['round_2']
            r3 = pontos[equipe]['round_3']
            
            melhores = sorted([r1, r2, r3], reverse=True)[:2]
            pontuacao_geral = sum(melhores)

            ranking.append((equipe, pontuacao_geral))   

        ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

        for posicao, (equipe, pontuacao_geral) in enumerate(ranking_ordenado, start=1):
            print(f'{posicao}° lugar - {equipe}: {pontuacao_geral} pontos')

    elif acao == 3:
        break

    else:
        print('Opção inválida!')
