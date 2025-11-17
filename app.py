from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Chave secreta para usar session (ideal seria vir de variável de ambiente).
app.secret_key = "uma_chave_beeem_secreta_e_grande_aqui"


# ==============================
# FUNÇÃO DE PONTUAÇÃO
# ==============================

def pontuacao_campos(dados):

    # Ladrilho inicial
    lad_ini = int(dados.get('lad_ini', 2))
    lad_ini = 5 if lad_ini == 1 else 0

    # -------- Checkpoint 1 --------
    prim_check = int(dados.get('prim_check', 0))
    tent_prim = int(dados.get('tent_prim', 4))
    if tent_prim == 1:
        prim_check *= 5
    elif tent_prim == 2:
        prim_check *= 3
    elif tent_prim == 3:
        prim_check *= 1
    else:
        prim_check = 0

    # -------- Checkpoint 2 --------
    seg_check = int(dados.get('seg_check', 0))
    tent_seg = int(dados.get('tent_seg', 4))
    if tent_seg == 1:
        seg_check *= 5
    elif tent_seg == 2:
        seg_check *= 3
    elif tent_seg == 3:
        seg_check *= 1
    else:
        seg_check = 0

    # -------- Checkpoint 3 --------
    ter_check = int(dados.get('ter_check', 0))
    tent_ter = int(dados.get('tent_ter', 4))
    if tent_ter == 1:
        ter_check *= 5
    elif tent_ter == 2:
        ter_check *= 3
    elif tent_ter == 3:
        ter_check *= 1
    else:
        ter_check = 0

    # -------- Elementos de pista --------
    gap = int(dados.get('gap', 0)) * 10
    lombada = int(dados.get('lombada', 0)) * 10
    rampa = int(dados.get('rampa', 0)) * 10
    intersec = int(dados.get('intersec', 0)) * 10
    obstaculo = int(dados.get('obstaculo', 0)) * 20
    gangorra = int(dados.get('gangorra', 0)) * 20

    fal_pro = int(dados.get('fal_pro', 0))

    # -------- Ladrilho de chegada --------
    lad_cheg = int(dados.get('lad_cheg', 2))
    if lad_cheg == 1:
        lad_cheg = max(0, 60 - (5 * fal_pro))
    else:
        lad_cheg = 0

    # -------- VÍTIMAS --------

    # Vítimas vivas (no lugar certo)
    vivas = int(dados.get('vit_viv', 0))
    if vivas == 1:
        vivas = 1.3
    elif vivas == 2:
        vivas = 1.3 * 1.3
    else:
        vivas = 0

    # Vítima morta (no lugar certo)
    morta = int(dados.get('vit_morta', 0))
    morta = 1.3 if morta == 1 else 0

    # -------- DESAFIO SURPRESA --------
    ds = int(dados.get('desaf_sur', 2))
    ds = 1.5 if ds == 1 else 0

    # -------- MULTIPLICADOR --------
    if vivas > 0 and morta > 0:
        mult = vivas * morta
    elif vivas > 0:
        mult = vivas
    elif morta > 0:
        mult = morta
    else:
        mult = 1

    if ds > 0:
        mult *= ds

    total_base = (
        lad_ini + prim_check + seg_check + ter_check +
        gap + lombada + rampa + intersec + obstaculo +
        gangorra + lad_cheg
    )

    return total_base * mult


# ==============================
# ESTADO POR USUÁRIO (SESSION)
# ==============================

def get_state():
    """Pega equipes e pontos da sessão do usuário atual."""
    equipes = session.get("equipes", [])
    pontos = session.get("pontos", {})
    return equipes, pontos


def save_state(equipes, pontos):
    """Salva equipes e pontos na sessão do usuário atual."""
    session["equipes"] = equipes
    session["pontos"] = pontos


# ==============================
# ROTAS
# ==============================

@app.route("/")
def index():
    equipes, pontos = get_state()

    ranking = []
    for e in equipes:
        r1 = pontos[e]["round_1"]
        r2 = pontos[e]["round_2"]
        r3 = pontos[e]["round_3"]
        melhor2 = sum(sorted([r1, r2, r3], reverse=True)[:2])
        ranking.append((e, melhor2))

    ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

    return render_template(
        "index.html",
        equipes=equipes,
        pontos=pontos,
        ranking_ordenado=ranking_ordenado,
        msg_round=None
    )


@app.route("/adicionar_equipe", methods=["POST"])
def adicionar_equipe():
    equipes, pontos = get_state()

    nome = request.form.get("nome_equipe", "").strip()
    if nome and nome not in equipes:
        equipes.append(nome)
        pontos[nome] = {"round_1": 0, "round_2": 0, "round_3": 0}

    save_state(equipes, pontos)
    return redirect(url_for("index"))


@app.route("/registrar_round", methods=["POST"])
def registrar_round():
    equipes, pontos = get_state()

    equipe = request.form.get("equipe")
    round_n = request.form.get("round")
    realizou = int(request.form.get("realizou", 2))

    if not equipe or equipe not in equipes:
        msg = "Equipe inválida!"
    else:
        chave = f"round_{round_n}"
        if realizou == 2:
            pontos[equipe][chave] = 0
            msg = f"{equipe} não realizou o round. Pontuação = 0."
        else:
            total = pontuacao_campos(request.form.to_dict())
            pontos[equipe][chave] = total
            msg = f"{equipe} marcou {total} pontos no {chave}!"

    save_state(equipes, pontos)

    ranking = []
    for e in equipes:
        r1 = pontos[e]["round_1"]
        r2 = pontos[e]["round_2"]
        r3 = pontos[e]["round_3"]
        melhor2 = sum(sorted([r1, r2, r3], reverse=True)[:2])
        ranking.append((e, melhor2))

    ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

    return render_template(
        "index.html",
        equipes=equipes,
        pontos=pontos,
        ranking_ordenado=ranking_ordenado,
        msg_round=msg
    )


@app.route("/reset", methods=["POST"])
def reset():
    """Apaga todos os dados da sessão deste usuário."""
    session.clear()
    return redirect(url_for("index"))


# ==============================
# EXECUÇÃO LOCAL
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0")
