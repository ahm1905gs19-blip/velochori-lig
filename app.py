import streamlit as st
import pandas as pd
import datetime
import random
import time

st.set_page_config(page_title="Velochori Ultimate League", layout="wide")

# ---------------- SESSION ----------------
if "matches" not in st.session_state:
    st.session_state.matches = {}

if "live" not in st.session_state:
    st.session_state.live = False
    st.session_state.minute = 0
    st.session_state.home_score = 0
    st.session_state.away_score = 0
    st.session_state.events = []

if "budget" not in st.session_state:
    st.session_state.budget = 100

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f172a,#1e293b); color:white;}
.card {background:#1e293b;padding:20px;border-radius:20px;margin-bottom:15px;}
.score {font-size:50px;font-weight:900;color:#22c55e;}
.live {color:red;animation: blink 1s infinite;}
@keyframes blink {50%{opacity:0.3;}}
</style>
""", unsafe_allow_html=True)

st.title("🏆 VELOCHORI SUPER LEAGUE PRO")

# ---------------- DATA ----------------
def get_table():
    data = {
        "Billispor": {"P":18,"AG":150,"YG":154},
        "Prospor": {"P":12,"AG":154,"YG":150}
    }
    df = pd.DataFrame(data).T
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values("P", ascending=False)

# ---------------- AI ----------------
def predict(home, away):
    df = get_table()
    if df.loc[home,"P"] > df.loc[away,"P"]:
        return f"🔥 {home} favori"
    elif df.loc[home,"P"] < df.loc[away,"P"]:
        return f"⚡ {away} önde"
    return "🤝 Dengede"

# ---------------- SIMULATION ----------------
def simulate():
    if st.session_state.minute < 90:
        st.session_state.minute += 1

        if random.random() < 0.07:
            if random.random() < 0.5:
                st.session_state.home_score += 1
                st.session_state.events.insert(0,f"⚽ {st.session_state.minute}' GOL! Ev sahibi attı!")
            else:
                st.session_state.away_score += 1
                st.session_state.events.insert(0,f"⚽ {st.session_state.minute}' GOL! Deplasman attı!")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🎮 MANAGER MODE")

    team = st.selectbox("Takımın", ["Billispor","Prospor"])
    st.metric("💰 Bütçe", f"{st.session_state.budget}M €")

    players = {"Messi Jr":50,"Ronaldo Jr":45,"Haaland Mini":60}

    p = st.selectbox("Transfer", list(players.keys()))
    if st.button("Satın Al"):
        if st.session_state.budget >= players[p]:
            st.session_state.budget -= players[p]
            st.success(f"{p} alındı!")
        else:
            st.error("Para yok!")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Lig", "⚽ Canlı Maç", "📈 Analiz"])

# ---------------- TAB 1 ----------------
with tab1:
    df = get_table()
    st.dataframe(df)

    st.subheader("📊 Grafikler")
    st.bar_chart(df[["AG","YG"]])

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("🔥 CANLI MAÇ")

    col1,col2,col3 = st.columns([2,1,2])

    with col1:
        st.markdown("<div class='card'>BILLISPOR</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='score'>{st.session_state.home_score} - {st.session_state.away_score}</div>", unsafe_allow_html=True)
        if st.session_state.live:
            st.markdown(f"<div class='live'>{st.session_state.minute}'</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>PROSPOR</div>", unsafe_allow_html=True)

    st.info(predict("Billispor","Prospor"))

    colA,colB = st.columns(2)

    if colA.button("▶ Maçı Başlat"):
        st.session_state.live = True
        st.session_state.minute = 0
        st.session_state.home_score = 0
        st.session_state.away_score = 0
        st.session_state.events = []

    if colB.button("⏹ Durdur"):
        st.session_state.live = False

    if st.session_state.live:
        simulate()
        time.sleep(0.5)
        st.rerun()

    st.subheader("📺 Maç Anlatımı")
    for e in st.session_state.events[:10]:
        st.write(e)

# ---------------- TAB 3 ----------------
with tab3:
    df = get_table()
    lider = df.index[0]

    st.markdown(f"""
    <div class='card'>
        <h1>{lider}</h1>
        <p>Şampiyonluk yolunda lider!</p>
    </div>
    """, unsafe_allow_html=True)
