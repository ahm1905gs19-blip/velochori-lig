import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Velochori Süper Lig", layout="wide")

# CSS
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#eef2ff,#f8fafc);
}

.title {
    text-align:center;
    font-size:45px;
    font-weight:900;
    margin-bottom:20px;
}

.card {
    background:white;
    padding:15px;
    border-radius:15px;
    margin-bottom:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
    transition:0.3s;
}

.card:hover {
    transform:scale(1.02);
}

.leader {
    border:2px solid gold;
    box-shadow:0 0 20px gold;
}

.goal {
    font-weight:900;
    color:#16a34a;
    animation:pulse 1.5s infinite;
}

@keyframes pulse {
    0%{transform:scale(1)}
    50%{transform:scale(1.2)}
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

# SKOR GİR
st.sidebar.header("⚽ Skor Gir")

with st.sidebar.form("form"):
    w = st.number_input("Hafta",11,20,11)

    home = "Prospor" if w % 2 == 0 else "Billispor"
    away = "Billispor" if home == "Prospor" else "Prospor"

    st.write(home,"vs",away)

    c1,c2 = st.columns(2)
    hs = c1.number_input(home,0,200)
    a_s = c2.number_input(away,0,200)

    if st.form_submit_button("Kaydet"):
        st.session_state.matches[w] = {
            "Ev":home,"EvSkor":hs,
            "Dep":away,"DepSkor":a_s
        }
        if hs>0 or a_s>0:
            st.balloons()
            st.success("⚽ GOAL!")

# TABLO
def get_table():
    stats = {
        "Billispor":{"O":10,"G":6,"B":0,"M":4,"AG":150,"YG":154,"P":18,"Logo":"billispor.png"},
        "Prospor":{"O":10,"G":4,"B":0,"M":6,"AG":154,"YG":150,"P":12,"Logo":"prospor.png"}
    }

    for m in st.session_state.matches.values():
        stats[m["Ev"]]["O"] += 1
        stats[m["Dep"]]["O"] += 1

        stats[m["Ev"]]["AG"] += m["EvSkor"]
        stats[m["Ev"]]["YG"] += m["DepSkor"]

        stats[m["Dep"]]["AG"] += m["DepSkor"]
        stats[m["Dep"]]["YG"] += m["EvSkor"]

        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["P"] += 3
        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["P"] += 3
        else:
            stats[m["Ev"]]["P"] += 1
            stats[m["Dep"]]["P"] += 1

    df = pd.DataFrame(stats).T
    df["Av"] = df["AG"] - df["YG"]

    return df.sort_values(["P","Av"], ascending=False)

# TABS
tab1,tab2,tab3 = st.tabs(["📊 Puan Durumu","📅 Fikstür","📈 Grafik"])

# PUAN DURUMU
with tab1:
    df = get_table().reset_index()
    df.columns = ["Takım","O","G","B","M","AG","YG","P","Logo","Av"]

    df.index += 1

    for i,row in df.iterrows():

        medal = ["🥇","🥈","🥉"][i-1] if i<=3 else str(i)
        leader = "leader" if i==1 else ""

        col1, col2, col3 = st.columns([1,5,2])

        with col1:
            st.image(row["Logo"], width=55)

        with col2:
            st.markdown(f"""
            <div class="card {leader}">
                <div style="font-size:20px; font-weight:800;">
                    {medal} {row['Takım']}
                </div>
                <div style="color:gray;">
                    {row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card {leader}" style="text-align:right;">
                <div style="font-size:26px; font-weight:900; color:#16a34a;">
                    {row['P']}
                </div>
                <div style="color:gray;">
                    Av {row['Av']}
                </div>
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

        score = "vs"

        if w in st.session_state.matches:
            m = st.session_state.matches[w]
            score = f'<span class="goal">{m["EvSkor"]}-{m["DepSkor"]}</span>'

        st.markdown(f"""
        <div class="card">
        <b>{w}. Hafta</b> | {date}<br>
        {home} {score} {away}
        </div>
        """, unsafe_allow_html=True)

# GRAFİK
with tab3:
    df = get_table()
    st.line_chart(df["P"])
