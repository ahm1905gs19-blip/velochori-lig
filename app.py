import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM (Daha Dengeli Boyutlar)
st.markdown("""
<style>
.stApp { background: #f8fafc; }

/* BAŞLIK (Daha Şık ve Orta Boyut) */
.league-title {
    font-size: 45px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(90deg, #15803d, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TAKIM KARTI (Yazılar Küçültüldü) */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 15px 25px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.leader { border: 2px solid #eab308; background: #fefce8; }

.stats-container {
    display: flex;
    gap: 20px;
    align-items: center;
}

.points-text {
    font-size: 28px;
    font-weight: 800;
    color: #15803d;
}

.av-text {
    font-size: 18px;
    font-weight: 600;
    color: #64748b;
}

/* TABLO STİLİ */
.stTable {
    background: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR (SKOR GİRİŞİ)
st.sidebar.header("🕹️ Yönetici Paneli")
with st.sidebar.form("score_form"):
    week_input = st.number_input("Hafta", min_value=11, max_value=20, value=11)
    is_even = week_input % 2 == 0
    h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
    h_score = st.number_input(f"{h_team}", min_value=0, step=1)
    a_score = st.number_input(f"{a_team}", min_value=0, step=1)
    if st.form_submit_button("Kaydet"):
        st.session_state.matches[week_input] = {"Ev": h_team, "EvSkor": h_score, "Dep": a_team, "DepSkor": a_score}

# HESAPLAMA MOTORU
def get_standings():
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 15, "YG": 19, "P": 18},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 19, "YG": 15, "P": 12}
    }
    for w, m in st.session_state.matches.items():
        stats[m["Ev"]]["O"] += 1; stats[m["Dep"]]["O"] += 1
        stats[m["Ev"]]["AG"] += m["EvSkor"]; stats[m["Ev"]]["YG"] += m["DepSkor"]
        stats[m["Dep"]]["AG"] += m["DepSkor"]; stats[m["Dep"]]["YG"] += m["EvSkor"]
        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["G"] += 1; stats[m["Ev"]]["P"] += 3; stats[m["Dep"]]["M"] += 1
        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["G"] += 1; stats[m["Dep"]]["P"] += 3; stats[m["Ev"]]["M"] += 1
        else:
            stats[m["Ev"]]["B"] += 1; stats[m["Dep"]]["B"] += 1; stats[m["Ev"]]["P"] += 1; stats[m["Dep"]]["P"] += 1
    
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    df.columns = ["Takım", "O", "G", "B", "M", "AG", "YG", "P"]
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(by=["P", "Av"], ascending=[False, False])

# TABLAR
tab1, tab2 = st.tabs(["📊 SIRALAMA", "📅 FİKSTÜR"])

with tab1:
    df = get_standings()
    # 1. Kart Görünümü
    for i, row in df.iterrows():
        l_class = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {l_class}">
            <div>
                <b style="font-size:18px;">{i+1}. {row['Takım'].upper()}</b><br>
                <small style="color:#64748b;">{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</small>
            </div>
            <div class="stats-container">
                <span class="av-text">AV: {row['Av']}</span>
                <span class="points-text">{row['P']} <small style="font-size:12px;">PTS</small></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    # 2. Detaylı Tablo Görünümü
    st.subheader("Detaylı Puan Durumu")
    st.table(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]])

with tab2:
    start_date = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        date = start_date + datetime.timedelta(days=7*i)
        h = "Prospor" if w % 2 == 0 else "Billispor"
        a = "Billispor" if h == "Prospor" else "Prospor"
        res = f"{st.session_state.matches[w]['EvSkor']} - {st.session_state.matches[w]['DepSkor']}" if w in st.session_state.matches else "vs"
        st.write(f"**{w}. Hafta** | {date.strftime('%d.%m.%Y')} | {h} {res} {a}")
