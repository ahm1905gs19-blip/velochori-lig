import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM (Ekran görüntündeki temaya sadık kalınmıştır)
st.markdown("""
<style>
.stApp { background: #ffffff; }

/* BAŞLIK */
.league-title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 30px;
    color: #1e293b;
    font-family: 'Arial', sans-serif;
}

/* TAKIM KARTI */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px 30px;
    border-radius: 15px;
    margin-bottom: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.leader { 
    border: 2px solid #fbbf24; 
    background: #fffdf2; 
}

.stats-right {
    display: flex;
    gap: 30px;
    align-items: center;
}

.points-val {
    font-size: 32px;
    font-weight: 900;
    color: #16a34a;
}

.av-val {
    font-size: 18px;
    font-weight: 600;
    color: #64748b;
}

/* FİKSTÜR KARTLARI */
.match-card {
    background: white;
    padding: 15px 25px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR
st.sidebar.header("🕹️ Yönetici Paneli")
with st.sidebar.form("score_form"):
    week_input = st.number_input("Hafta", min_value=11, max_value=20, value=11)
    is_even = week_input % 2 == 0
    h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
    h_score = st.number_input(f"{h_team}", min_value=0, step=1)
    a_score = st.number_input(f"{a_team}", min_value=0, step=1)
    if st.form_submit_button("Skoru Kaydet"):
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
    # Billispor 1, Prospor 2 olacak şekilde sırala
    return df.sort_values(by=["P", "Av"], ascending=[False, False])

# SEKMELER
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "📅 FİKSTÜR"])

with tab1:
    df = get_standings()
    # Kart Görünümü
    for i, row in df.iterrows():
        l_class = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {l_class}">
            <div>
                <b style="font-size:20px;">{i+1}. {row['Takım'].upper()}</b><br>
                <small style="color:#64748b;">{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</small>
            </div>
            <div class="stats-right">
                <span class="av-val">AV: {row['Av']}</span>
                <span class="points-val">{row['P']} <small style="font-size:14px;">PTS</small></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### Detaylı Puan Durumu")
    # İşaretlediğin '0' ve '1' rakamlarını kaldırmak için index=False kullanıyoruz
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        date = start_date + datetime.timedelta(days=7*i)
        h = "Prospor" if w % 2 == 0 else "Billispor"
        a = "Billispor" if h == "Prospor" else "Prospor"
        res = f"<b>{st.session_state.matches[w]['EvSkor']} - {st.session_state.matches[w]['DepSkor']}</b>" if w in st.session_state.matches else "vs"
        
        st.markdown(f"""
        <div class="match-card">
            <div style="width:100px;"><b>{w}. Hafta</b><br><small>{date.strftime('%d.%m.%Y')}</small></div>
            <div style="flex-grow:1; text-align:center; font-size:18px;">{h} &nbsp; {res} &nbsp; {a}</div>
            <div style="width:100px; text-align:right; color:#16a34a;">●</div>
        </div>
        """, unsafe_allow_html=True)
