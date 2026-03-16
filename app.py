import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS
st.markdown("""
<style>
.main{background:linear-gradient(135deg,#eef2ff,#f8fafc);}
.league-title{
font-size:50px;
font-weight:900;
text-align:center;
margin-bottom:30px;
background:linear-gradient(90deg,#16a34a,#22c55e);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}
.team-card{
display:flex;
align-items:center;
gap:20px;
background:white;
padding:18px;
border-radius:16px;
margin-bottom:15px;
border:1px solid #e2e8f0;
box-shadow:0 6px 15px rgba(0,0,0,0.07);
}
.leader{
border:2px solid gold;
background:linear-gradient(90deg,#fffbe6,#ffffff);
}
.points{
font-size:42px;
font-weight:900;
color:#16a34a;
}
.match-card{
background:white;
padding:18px;
border-radius:14px;
margin-bottom:12px;
border-left:6px solid #16a34a;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# SESSION
if "matches" not in st.session_state:
    st.session_state.matches = {}

# RESET BUTONU
if st.sidebar.button("🔄 Skorları Sıfırla"):
    st.session_state.matches = {}
    st.rerun()

# SIDEBAR
st.sidebar.header("⚽ Skor Gir")

with st.sidebar.form("score_form"):

    week = st.number_input("Hafta", min_value=11, max_value=20, value=11)

    home = "Prospor" if week % 2 == 0 else "Billispor"
    away = "Billispor" if home == "Prospor" else "Prospor"

    st.write(home, "vs", away)

    c1, c2 = st.columns(2)

    home_score = c1.number_input(home, 0, 200)
    away_score = c2.number_input(away, 0, 200)

    if st.form_submit_button("Kaydet"):

        st.session_state.matches[week] = {
            "Ev": home,
            "EvSkor": home_score,
            "Dep": away,
            "DepSkor": away_score
        }

        st.success("Skor kaydedildi")

# PUAN HESAPLAMA
def get_table():

    stats = {
        "Billispor": {"O":10,"G":6,"B":0,"M":4,"AG":150,"YG":154,"P":18,"Logo":"billispor.jpg"},
        "Prospor": {"O":10,"G":4,"B":0,"M":6,"AG":154,"YG":150,"P":12,"Logo":"prospor.jpg"}
    }

    for w,m in st.session_state.matches.items():

        stats[m["Ev"]]["O"] += 1
        stats[m["Dep"]]["O"] += 1

        stats[m["Ev"]]["AG"] += m["EvSkor"]
        stats[m["Ev"]]["YG"] += m["DepSkor"]

        stats[m["Dep"]]["AG"] += m["DepSkor"]
        stats[m["Dep"]]["YG"] += m["EvSkor"]

        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["G"] += 1
            stats[m["Ev"]]["P"] += 3
            stats[m["Dep"]]["M"] += 1

        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["G"] += 1
            stats[m["Dep"]]["P"] += 3
            stats[m["Ev"]]["M"] += 1

        else:
            stats[m["Ev"]]["B"] += 1
            stats[m["Dep"]]["B"] += 1
            stats[m["Ev"]]["P"] += 1
            stats[m["Dep"]]["P"] += 1

    df = pd.DataFrame.from_dict(stats, orient="index").reset_index()
    df.columns = ["Takım","O","G","B","M","AG","YG","P","Logo"]
    df["Av"] = df["AG"] - df["YG"]

    return df.sort_values(by=["P","Av"], ascending=False)

# TABLAR
tab1, tab2 = st.tabs(["📊 PUAN DURUMU","📅 FİKSTÜR"])

# PUAN TABLOSU
with tab1:

    df = get_table()

    for i,row in df.iterrows():

        leader = "leader" if i == 0 else ""

        st.markdown(f"""
        <div class="team-card {leader}">
        <img src="file/{row['Logo']}" width="70">
        <div style="flex-grow:1">
        <h3>{row['Takım']}</h3>
        <span>{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</span>
        </div>
        <div style="text-align:right">
        <div class="points">{row['P']}</div>
        <div>Averaj {row['Av']}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.table(df[["Takım","O","G","B","M","AG","YG","Av","P"]])

# FİKSTÜR
with tab2:

    start = datetime.date(2026,3,22)

    for i in range(10):

        w = 11 + i
        date = start + datetime.timedelta(days=7*i)

        home = "Prospor" if w % 2 == 0 else "Billispor"
        away = "Billispor" if home == "Prospor" else "Prospor"

        score = "vs"
        status = "Bekleniyor"

        if w in st.session_state.matches:
            m = st.session_state.matches[w]
            score = f"{m['EvSkor']} - {m['DepSkor']}"
            status = "Tamamlandı"

        st.markdown(f"""
        <div class="match-card">
        <b>{w}. Hafta</b> | {date.strftime('%d.%m.%Y')} <br>
        {home} {score} {away} <br>
        <small>{status}</small>
        </div>
        """, unsafe_allow_html=True)
