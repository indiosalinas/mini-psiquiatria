import streamlit as st

st.set_page_config(page_title="MINI Psiquiatria", layout="centered")

st.title("🧠 MINI - Entrevista Psiquiátrica Estruturada")

# -----------------------------
# ESTADO
# -----------------------------
if "respostas" not in st.session_state:
    st.session_state.respostas = {}

r = st.session_state.respostas

# -----------------------------
# MÓDULO A - DEPRESSÃO
# -----------------------------
st.header("Módulo A - Episódio Depressivo Maior")

r["A1"] = st.radio("Humor deprimido?", ["Não", "Sim"], key="A1") == "Sim"
r["A2"] = st.radio("Perda de interesse?", ["Não", "Sim"], key="A2") == "Sim"

if r["A1"] or r["A2"]:
    r["A3a"] = st.checkbox("Alteração de apetite")
    r["A3b"] = st.checkbox("Insônia/hipersonia")
    r["A3c"] = st.checkbox("Agitação/lentificação")
    r["A3d"] = st.checkbox("Fadiga")
    r["A3e"] = st.checkbox("Culpa")
    r["A3f"] = st.checkbox("Concentração")
    r["A3g"] = st.checkbox("Ideação de morte")

# -----------------------------
# MÓDULO D - MANIA
# -----------------------------
st.header("Módulo D - Mania/Hipomania")

r["D1"] = st.radio("Período de humor elevado/irritável?", ["Não", "Sim"], key="D1") == "Sim"

if r["D1"]:
    r["D2a"] = st.checkbox("Grandiosidade")
    r["D2b"] = st.checkbox("Pouca necessidade de sono")
    r["D2c"] = st.checkbox("Mais falante")
    r["D2d"] = st.checkbox("Fuga de ideias")
    r["D2e"] = st.checkbox("Distrabilidade")
    r["D2f"] = st.checkbox("Aumento de atividade")
    r["D2g"] = st.checkbox("Comportamento de risco")

# -----------------------------
# MÓDULO J - TAG
# -----------------------------
st.header("Módulo J - Ansiedade Generalizada")

r["J1"] = st.radio("Preocupação excessiva por meses?", ["Não", "Sim"], key="J1") == "Sim"

if r["J1"]:
    r["J2a"] = st.checkbox("Inquietação")
    r["J2b"] = st.checkbox("Fadiga")
    r["J2c"] = st.checkbox("Dificuldade de concentração")
    r["J2d"] = st.checkbox("Irritabilidade")
    r["J2e"] = st.checkbox("Tensão muscular")
    r["J2f"] = st.checkbox("Alteração do sono")

# -----------------------------
# MÓDULO E - PÂNICO
# -----------------------------
st.header("Módulo E - Transtorno do Pânico")

r["E1"] = st.radio("Teve ataques súbitos de medo intenso?", ["Não", "Sim"], key="E1") == "Sim"

if r["E1"]:
    r["E2a"] = st.checkbox("Palpitação")
    r["E2b"] = st.checkbox("Sudorese")
    r["E2c"] = st.checkbox("Falta de ar")
    r["E2d"] = st.checkbox("Medo de morrer")
    r["E2e"] = st.checkbox("Tontura")

# -----------------------------
# MÓDULO C - SUICÍDIO
# -----------------------------
st.header("Módulo C - Risco de Suicídio")

r["C1"] = st.checkbox("Desejo de estar morto")
r["C2"] = st.checkbox("Quis se machucar")
r["C3"] = st.checkbox("Pensou em suicídio")
r["C4"] = st.checkbox("Planejou suicídio")
r["C5"] = st.checkbox("Tentativa recente")
r["C6"] = st.checkbox("Tentativa na vida")

# -----------------------------
# FUNÇÕES
# -----------------------------
def avaliar_depressao(r):
    if not (r.get("A1") or r.get("A2")):
        return False, 0
    total = sum([r.get(k, False) for k in ["A3a","A3b","A3c","A3d","A3e","A3f","A3g"]])
    return total >= 3, total

def avaliar_mania(r):
    if not r.get("D1"):
        return False, 0
    total = sum([r.get(k, False) for k in ["D2a","D2b","D2c","D2d","D2e","D2f","D2g"]])
    return total >= 3, total

def avaliar_tag(r):
    if not r.get("J1"):
        return False, 0
    total = sum([r.get(k, False) for k in ["J2a","J2b","J2c","J2d","J2e","J2f"]])
    return total >= 3, total

def avaliar_panico(r):
    if not r.get("E1"):
        return False, 0
    total = sum([r.get(k, False) for k in ["E2a","E2b","E2c","E2d","E2e"]])
    return total >= 2, total

def risco_suicidio(r):
    pontos = 0
    if r.get("C1"): pontos += 1
    if r.get("C2"): pontos += 2
    if r.get("C3"): pontos += 6
    if r.get("C4"): pontos += 10
    if r.get("C5"): pontos += 10
    if r.get("C6"): pontos += 4

    if pontos >= 10: return "Alto"
    elif pontos >= 6: return "Moderado"
    elif pontos >= 1: return "Baixo"
    return "Nenhum"

# -----------------------------
# RESULTADO
# -----------------------------
st.header("📊 Resultado")

if st.button("Calcular"):

    dep, n_dep = avaliar_depressao(r)
    mania, n_mania = avaliar_mania(r)
    tag, n_tag = avaliar_tag(r)
    panico, n_panico = avaliar_panico(r)
    suic = risco_suicidio(r)

    if dep:
        st.success(f"Depressão maior ({n_dep} sintomas)")

    if mania:
        st.error(f"⚠️ Mania/Hipomania ({n_mania} sintomas)")

    if tag:
        st.info(f"Ansiedade Generalizada ({n_tag} sintomas)")

    if panico:
        st.warning(f"Pânico ({n_panico} sintomas)")

    if suic == "Alto":
        st.error("RISCO DE SUICÍDIO: ALTO")
    elif suic == "Moderado":
        st.warning("RISCO: MODERADO")

    st.divider()

    resumo = ""

    if mania:
        resumo += "Sugestivo de transtorno bipolar.\n"

    if dep:
        resumo += "Critérios para episódio depressivo maior.\n"

    if tag:
        resumo += "Quadro compatível com ansiedade generalizada.\n"

    if panico:
        resumo += "Presença de sintomas de pânico.\n"

    if suic != "Nenhum":
        resumo += f"Risco de suicídio: {suic}.\n"

    if resumo == "":
        resumo = "Sem alterações significativas."

    st.text_area("Relatório", resumo, height=150)