import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Velochori Süper Lig", layout="wide")

# CSS
st.markdown("""
<style>
.main{background:linear-gradient(135deg,#eef2ff,#f8fafc);}

.title{
text-align:center;
font-size:55px;
font-weight:900;
background:linear-gradient(90deg,#16a34a,#4ade80);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:30px;
}

/* takım kart */
.card{
display:flex;
align-items:center;
justify-content:space-between;
background:white;
padding:20px;
border-radius:15px;
margin-bottom:15px;
box-shadow:0 6px 15px rgba(0,0,0,0.08);
transition:.3s;
}

.card:hover{
transform:scale(1.03);
}

/* lider */
.leader{
border:3px solid gold;
box-shadow:0 0 25px gold;
}

/* skor animasyon */
.goal{
font-size:28px;
font-weight:900;
color:#16a34a;
animation:pulse 1.5s infinite;
}

@keyframes pulse{
0%{transform:scale(1)}
50%{transform:scale(1.15)}
100%{transform:scale(1)}
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# SESSION
if "matches" not in st.session_state:
    st.session_state.matches = {}

# RESET
if st.sidebar.button("🔄 Sıfırla"):
    st.session_state.matches = {}
    st.rerun()

# SKOR GİRİŞ
st.sidebar.header("⚽ Skor")

with st.sidebar.form("form"):
    w = st.number_input("Hafta",11,20,11)

    home = "Prospor" if w%2==0 else "Billispor"
    away = "Billispor" if home=="Prospor" else "Prospor"

    st.write(home,"vs",away)

    c1,c2 = st.columns(2)
    hs = c1.number_input(home,0,200)
    as_ = c2.number_input(away,0,200)

    if st.form_submit_button("Kaydet"):

        st.session_state.matches[w] = {
            "Ev":home,"EvSkor":hs,
            "Dep":away,"DepSkor":as_
        }

        if hs>0 or as_>0:
            st.balloons()
            st.success("⚽ GOALLL!")

# TABLO
def table():

    stats = {
        "Billispor":{"O":10,"G":6,"B":0,"M":4,"AG":150,"YG":154,"P":18},
        "Prospor":{"O":10,"G":4,"B":0,"M":6,"AG":154,"YG":150,"P":12}
    }

    for m in st.session_state.matches.values():

        stats[m["Ev"]]["O"]+=1
        stats[m["Dep"]]["O"]+=1

        stats[m["Ev"]]["AG"]+=m["EvSkor"]
        stats[m["Ev"]]["YG"]+=m["DepSkor"]

        stats[m["Dep"]]["AG"]+=m["DepSkor"]
        stats[m["Dep"]]["YG"]+=m["EvSkor"]

        if m["EvSkor"]>m["DepSkor"]:
            stats[m["Ev"]]["P"]+=3
        elif m["EvSkor"]<m["DepSkor"]:
            stats[m["Dep"]]["P"]+=3

    df = pd.DataFrame(stats).T
    df["Av"]=df["AG"]-df["YG"]

    return df.sort_values(["P","Av"],ascending=False)

# TABLAR
tab1,tab2,tab3 = st.tabs(["📊 Puan","📅 Fikstür","📈 Grafik"])

# PUAN
with tab1:

    df = table().reset_index()
    df.columns=["Takım","O","G","B","M","AG","YG","P","Av"]

    df.index+=1

    medals=["🥇","🥈","🥉"]

    for i,row in df.iterrows():

        medal = medals[i-1] if i<=3 else i
        leader = "leader" if i==1 else ""

        st.markdown(f"""
        <div class="card {leader}">
        <div>{medal} {row['Takım']}</div>
        <div>{row['P']} Puan</div>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(df)

# FİKSTÜR
with tab2:

    start = datetime.date(2026,3,22)

    for i in range(10):

        w = 11+i
        date = start + datetime.timedelta(days=7*i)

        home = "Prospor" if w%2==0 else "Billispor"
        away = "Billispor" if home=="Prospor" else "Prospor"

        score="vs"

        if w in st.session_state.matches:
            m = st.session_state.matches[w]
            score=f'<span class="goal">{m["EvSkor"]}-{m["DepSkor"]}</span>'

        st.markdown(f"""
        <div class="card">
        {w}. Hafta | {date}<br>
        {home} {score} {away}
        </div>
        """, unsafe_allow_html=True)

# GRAFİK
with tab3:

    df = table()

    st.line_chart(df["P"])
