from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ==============================
# FUNÇÃO DE PONTUAÇÃO (atualizada)
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

    # -------- VÍTIMAS (apenas certas) --------

    # VÍTIMAS VIVAS
    vivas = int(dados.get('vit_viv', 0))
    if vivas == 1:
        vivas = 1.3
    elif vivas == 2:
        vivas = 1.3 * 1.3
    else:
        vivas = 0

    # VÍTIMA MORTA
    morta = int(dados.get('vit_morta', 0))
    if morta == 1:
        morta = 1.3
    else:
        morta = 0

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
# BANCO DE DADOS
# ==============================

equipes = []
pontos = {}  # equipe -> { round_1, round_2, round_3 }


# ==============================
# TEMPLATE HTML ATUALIZADO
# ==============================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>RoboScore</title>
    <style>
        body { font-family: Arial; background:#0f172a; color:white; padding:20px; }
        .card { background:#020617; padding:15px; border-radius:12px; margin-bottom:25px; }
        input, select { padding:5px; margin-top:5px; width:100%; background:#111827; color:white; border:1px solid #4b5563; border-radius:5px;}
        button { padding:8px 15px; border:none; background:#2563eb; color:white; border-radius:8px; cursor:pointer; margin-top:10px; }
        table { width:100%; border-collapse:collapse; margin-top:10px; }
        th, td { border:1px solid #1f2937; padding:6px; text-align:left; }
    </style>
</head>
<body>

<h1>RoboScore – Sistema de Pontuação</h1>

<div class="card">
    <h2>1. Adicionar Equipe</h2>
    <form method="POST" action="{{ url_for('adicionar_equipe') }}">
        <label>Nome da equipe:</label>
        <input type="text" name="nome_equipe" required>
        <button>Adicionar</button>
    </form>

    <p>
    <strong>Equipes cadastradas:</strong>
    {% if equipes %}
        {{ equipes|join(', ') }}
    {% else %}
        Nenhuma ainda.
    {% endif %}
    </p>
</div>

<div class="card">
    <h2>2. Registrar Round</h2>

    <form method="POST" action="{{ url_for('registrar_round') }}">

        <label>Equipe:</label>
        <select name="equipe">
            <option value="">Selecione</option>
            {% for e in equipes %}
                <option value="{{e}}">{{e}}</option>
            {% endfor %}
        </select>

        <label>Round:</label>
        <select name="round">
            <option value="1">Round 1</option>
            <option value="2">Round 2</option>
            <option value="3">Round 3</option>
        </select>

        <label>Realizou o round?</label>
        <select name="realizou">
            <option value="1">Sim</option>
            <option value="2">Não</option>
        </select>

        <hr>

        <h3>Ladrilho inicial e Checkpoints</h3>

        <label>Superou o ladrilho inicial?</label>
        <select name="lad_ini">
            <option value="1">Sim</option>
            <option value="2">Não</option>
        </select>

        <label>Ladrilhos até o 1º checkpoint:</label>
        <input name="prim_check" type="number" value="0">

        <label>Tentativa:</label>
        <select name="tent_prim">
            <option value="1">1ª Tentativa</option>
            <option value="2">2ª Tentativa</option>
            <option value="3">3ª Tentativa</option>
            <option value="4">Não superou</option>
        </select>

        <label>Ladrilhos até o 2º checkpoint:</label>
        <input name="seg_check" type="number" value="0">

        <label>Tentativa:</label>
        <select name="tent_seg">
            <option value="1">1ª Tentativa</option>
            <option value="2">2ª Tentativa</option>
            <option value="3">3ª Tentativa</option>
            <option value="4">Não superou</option>
        </select>

        <label>Ladrilhos até o 3º checkpoint:</label>
        <input name="ter_check" type="number" value="0">

        <label>Tentativa:</label>
        <select name="tent_ter">
            <option value="1">1ª Tentativa</option>
            <option value="2">2ª Tentativa</option>
            <option value="3">3ª Tentativa</option>
            <option value="4">Não superou</option>
        </select>

        <hr>

        <h3>Elementos de pista</h3>

        <label>Gaps superados:</label>
        <input type="number" name="gap" value="0">

        <label>Lombadas superadas:</label>
        <input type="number" name="lombada" value="0">

        <label>Rampas superadas:</label>
        <input type="number" name="rampa" value="0">

        <label>Interseções superadas:</label>
        <input type="number" name="intersec" value="0">

        <label>Obstáculos superados:</label>
        <input type="number" name="obstaculo" value="0">

        <label>Gangorras superadas:</label>
        <input type="number" name="gangorra" value="0">

        <label>Falhas de progresso:</label>
        <input type="number" name="fal_pro" value="0">

        <label>Chegou no ladrilho final?</label>
        <select name="lad_cheg">
            <option value="1">Sim</option>
            <option value="2">Não</option>
        </select>

        <hr>

        <h3>Multiplicadores</h3>

        <label>Vítimas vivas (no lugar certo):</label>
        <select name="vit_viv">
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>

        <label>Vítima morta (no lugar certo):</label>
        <select name="vit_morta">
            <option value="0">0</option>
            <option value="1">1</option>
        </select>

        <label>Desafio surpresa:</label>
        <select name="desaf_sur">
            <option value="1">Sim</option>
            <option value="2">Não</option>
        </select>

        <button>Salvar Round</button>
    </form>

    {% if msg_round %}
        <p>{{ msg_round }}</p>
    {% endif %}

</div>

<div class="card">
    <h2>Ranking (2 melhores rounds)</h2>
    <table>
        <tr>
            <th>Posição</th>
            <th>Equipe</th>
            <th>Round 1</th>
            <th>Round 2</th>
            <th>Round 3</th>
            <th>Total</th>
        </tr>

        {% for item in ranking_ordenado %}
        <tr>
            <td>{{ loop.index }}º</td>
            <td>{{ item[0] }}</td>
            <td>{{ pontos[item[0]]["round_1"] }}</td>
            <td>{{ pontos[item[0]]["round_2"] }}</td>
            <td>{{ pontos[item[0]]["round_3"] }}</td>
            <td>{{ item[1] }}</td>
        </tr>
        {% endfor %}
    </table>
</div>

</body>
</html>
"""


# ==============================
# ROTAS FLASK
# ==============================

@app.route("/")
def index():
    ranking = []
    for e in equipes:
        r1 = pontos[e]["round_1"]
        r2 = pontos[e]["round_2"]
        r3 = pontos[e]["round_3"]
        melhor2 = sum(sorted([r1, r2, r3], reverse=True)[:2])
        ranking.append((e, melhor2))

    ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

    return render_template_string(TEMPLATE,
                                  equipes=equipes,
                                  pontos=pontos,
                                  ranking_ordenado=ranking_ordenado,
                                  msg_round=None)


@app.route("/adicionar_equipe", methods=["POST"])
def adicionar_equipe():
    nome = request.form.get("nome_equipe").strip()
    if nome and nome not in equipes:
        equipes.append(nome)
        pontos[nome] = {"round_1": 0, "round_2": 0, "round_3": 0}
    return redirect(url_for("index"))


@app.route("/registrar_round", methods=["POST"])
def registrar_round():
    equipe = request.form.get("equipe")
    round_n = request.form.get("round")
    realizou = int(request.form.get("realizou"))

    if equipe not in equipes:
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

    ranking = []
    for e in equipes:
        r1 = pontos[e]["round_1"]
        r2 = pontos[e]["round_round_2"] if "round_2" in pontos[e] else pontos[e]["round_2"]
        r3 = pontos[e]["round_3"]
        melhor2 = sum(sorted([r1, r2, r3], reverse=True)[:2])
        ranking.append((e, melhor2))

    ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

    return render_template_string(TEMPLATE,
                                  equipes=equipes,
                                  pontos=pontos,
                                  ranking_ordenado=ranking_ordenado,
                                  msg_round=msg)


# Para Render:
if __name__ == "__main__":
    app.run(host="0.0.0.0")
