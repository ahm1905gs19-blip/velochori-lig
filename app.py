import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM
st.markdown("""
<style>

.main{
background:linear-gradient(135deg,#eef2ff,#f8fafc);
}

/* BAŞLIK */
.league-title{
font-size:55px;
font-weight:900;
text-align:center;
margin-bottom:30px;
background: linear-gradient(90deg,#16a34a,#22c55e,#4ade80);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

/* TAKIM KARTI */
.team-card{
display:flex;
align-items:center;
gap:20px;
background:white;
padding:18px;
border-radius:16px;
margin-bottom:15px;
border:1px solid #e2e8f0;
transition:all .35s;
box-shadow:0 6px 15px rgba(0,0,0,0.07);
}

.team-card:hover{
transform:translateY(-6px) scale(1.02);
box-shadow:0 12px 30px rgba(0,0,0,0.18);
}

/* LİDER TAKIM */
.leader{
border:2px solid gold;
background:linear-gradient(90deg,#fffbe6,#ffffff);
}

/* PUAN */
.points{
font-size:42px;
font-weight:900;
color:#16a34a;
}

/* FİKSTÜR */
.match-card{
background:white;
padding:18px;
border-radius:14px;
margin-bottom:12px;
border-left:6px solid #16a34a;
transition:all .3s;
box-shadow:0 4px 10px rgba(0,0,0,0.08);
}

.match-card:hover{
transform:scale(1.03);
box-shadow:0 10px 25px rgba(0,0,0,0.15);
}

/* SKOR */
.score{
font-size:30px;
font-weight:900;
padding:0 25px;
animation:pulse 2s infinite;
}

@keyframes pulse{
0%{transform:scale(1)}
50%{transform:scale(1.1)}
100%{transform:scale(1)}
}

/* TABLO */
.stTable{
background:white;
border-radius:10px;
box-shadow:0 6px 15px rgba(0,0,0,0.1);
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#16a34a,#15803d);
color:white;
}

</style>
""",unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR
st.sidebar.header("🕹️ Yönetici Paneli")

with st.sidebar.form("score_form"):

    week_input = st.number_input("Hafta Seçin", min_value=11, max_value=20, value=11)

    is_even = week_input % 2 == 0
    h_team = "Prospor" if is_even else "Billispor"
    a_team = "Billispor" if is_even else "Prospor"

    st.write(f"{h_team} vs {a_team}")

    c1,c2 = st.columns(2)

    h_score = c1.number_input(h_team,min_value=0,step=1)
    a_score = c2.number_input(a_team,min_value=0,step=1)

    if st.form_submit_button("Skoru Kaydet"):

        st.session_state.matches[week_input] = {
            "Ev":h_team,
            "EvSkor":h_score,
            "Dep":a_team,
            "DepSkor":a_score
        }

        st.success("Skor kaydedildi")

# PUAN HESAPLAMA
def get_standings():

    stats = {
        "Billispor":{"O":10,"G":6,"B":0,"M":4,"AG":15,"YG":19,"P":18,"Logo":"billispor.jpg"},
        "Prospor":{"O":10,"G":4,"B":0,"M":6,"AG":19,"YG":15,"P":12,"Logo":"prospor.jpg"}
    }

    for w,m in st.session_state.matches.items():

        stats[m["Ev"]]["O"] +=1
        stats[m["Dep"]]["O"] +=1

        stats[m["Ev"]]["AG"] +=m["EvSkor"]
        stats[m["Ev"]]["YG"] +=m["DepSkor"]

        stats[m["Dep"]]["AG"] +=m["DepSkor"]
        stats[m["Dep"]]["YG"] +=m["EvSkor"]

        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["G"]+=1
            stats[m["Ev"]]["P"]+=3
            stats[m["Dep"]]["M"]+=1

        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["G"]+=1
            stats[m["Dep"]]["P"]+=3
            stats[m["Ev"]]["M"]+=1

        else:
            stats[m["Ev"]]["B"]+=1
            stats[m["Dep"]]["B"]+=1
            stats[m["Ev"]]["P"]+=1
            stats[m["Dep"]]["P"]+=1

    df = pd.DataFrame.from_dict(stats,orient='index').reset_index()

    df.columns = ["Takım","O","G","B","M","AG","YG","P","Logo"]

    df["Av"] = df["AG"] - df["YG"]

    return df.sort_values(by=["P","Av"],ascending=False)

# TABLAR
tab1,tab2 = st.tabs(["📊 PUAN DURUMU","📅 FİKSTÜR"])

# PUAN DURUMU
with tab1:

    df = get_standings()

    for i,row in df.iterrows():

        leader = "leader" if i==0 else ""

        st.markdown(f"""
        <div class="team-card {leader}">
            <img src="file/{row['Logo']}" width="70" style="border-radius:10px;">
            <div style="flex-grow:1">
                <h3>{row['Takım']}</h3>
                <span>{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</span>
            </div>
            <div style="text-align:right">
                <div class="points">{row['P']}</div>
                <div>Averaj {row['Av']}</div>
            </div>
        </div>
        """,unsafe_allow_html=True)

    st.table(df[["Takım","O","G","B","M","AG","YG","Av","P"]])

# FİKSTÜR
with tab2:

    start_date = datetime.date(2026,3,22)

    for i in range(10):

        w = 11+i
        date = start_date + datetime.timedelta(days=7*i)

        h = "Prospor" if w%2==0 else "Billispor"
        a = "Billispor" if h=="Prospor" else "Prospor"

        score = "vs"
        status = "Bekleniyor"

        if w in st.session_state.matches:

            m = st.session_state.matches[w]

            score = f'<span class="score">{m["EvSkor"]} - {m["DepSkor"]}</span>'
            status = "Tamamlandı"

        st.markdown(f"""
        <div class="match-card">

        <div style="display:flex;justify-content:space-between">

        <div>
        <b>{w}. Hafta</b><br>
        <small>{date.strftime('%d.%m.%Y')}</small>
        </div>

        <div>
        {h} {score} {a}
        </div>

        <div>
        {status}
        </div>

        </div>

        </div>
        """,unsafe_allow_html=True)
