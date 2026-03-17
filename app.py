import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM (Tüm yapı korunup detaylar rafine edildi)
st.markdown("""
<style>
.stApp { background: #ffffff; }

/* O GÖSTERİŞLİ BAŞLIK - DOKUNULMADI */
.league-title {
    font-size: 60px;
    font-weight: 900;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 40px;
    font-family: 'Arial Black', sans-serif;
    background: linear-gradient(90deg, #16a34a, #22c55e, #4ade80, #22c55e, #16a34a);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.05);
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* TAKIM KARTI - KORUNDU */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px 30px;
    border-radius: 15px;
    margin-bottom: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
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
    font-size: 35px;
    font-weight: 900;
    color: #16a34a;
}

.av-val {
    font-size: 18px;
    font-weight: 600;
    color: #64748b;
    background: #f1f5f9;
    padding: 5px 12px;
    border-radius: 8px;
}

/* MODERN FİKSTÜR - GELİŞTİRİLDİ */
.modern-fixture {
    background: #ffffff;
    border: 1px solid #f1f5f9;
    border-radius: 20px;
    padding: 15px 25px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 15px rgba(0,0,0,0.04);
}

.fixture-teams {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-grow: 1;
    justify-content: center;
    font-weight: 700;
    font-size: 1.1rem;
}

.vs-circle {
    background: #f8fafc;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 0.7rem;
    color: #16a34a;
    border: 1px solid #e2e8f0;
}

/* FORM NOKTALARI (Küçük Detay) */
.form-dot {
    height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-left: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR
with st.sidebar:
    st.header("🕹️ Yönetici Paneli")
    with st.form("score_form"):
        week_input = st.number_input("Hafta", min_value=11, max_value=20, value=11)
        is_even = week_input % 2 == 0
        h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
        st.info(f"Maç: {h_team} vs {a_team}")
        h_score = st.number_input(f"{h_team} Skoru", min_value=0, step=1)
        a_score = st.number_input(f"{a_team} Skoru", min_value=0, step=1)
        if st.form_submit_button("Skoru Kaydet"):
            st.session_state.matches[week_input] = {"Ev": h_team, "EvSkor": h_score, "Dep": a_team, "DepSkor": a_score}
            st.rerun()

    if st.button("Verileri Sıfırla", use_container_width=True):
        st.session_state.matches = {}
        st.rerun()

# HESAPLAMA MOTORU
def get_standings():
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12}
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

# SEKMELER
tab1, tab2 = st.tabs(["📊 GENEL DURUM", "📅 MAÇ TAKVİMİ"])

with tab1:
    df = get_standings()
    
    # Üst Bilgi Kartları (Yeni Geliştirme)
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Maç", f"{df['O'].sum() // 2}")
    c2.metric("Toplam Gol", f"{df['AG'].sum()}")
    c3.metric("Lider", f"{df.iloc[0]['Takım']}")

    st.write("") # Boşluk
    
    for i, row in df.iterrows():
        l_class = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {l_class}">
            <div>
                <b style="font-size:22px;">{i+1}. {row['Takım'].upper()}</b><br>
                <small style="color:#64748b;">{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</small>
            </div>
            <div class="stats-right">
                <span class="av-val">AV: {row['Av']}</span>
                <span class="points-val">{row['P']} <small style="font-size:14px;">PTS</small></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📝 Detaylı İstatistikler")
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    st.info("💡 Not: Skorlar girildikçe puan durumu otomatik olarak güncellenir.")
    
    for i in range(10):
        w = 11 + i
        date = start_date + datetime.timedelta(days=7*i)
        h = "Prospor" if w % 2 == 0 else "Billispor"
        a = "Billispor" if h == "Prospor" else "Prospor"
        
        is_done = w in st.session_state.matches
        if is_done:
            m = st.session_state.matches[w]
            score_display = f"<span style='color:#16a34a; font-size:1.5rem;'>{m['EvSkor']} - {m['DepSkor']}</span>"
            status = '<span style="color:#16a34a; font-size:0.8rem;">● BİTTİ</span>'
        else:
            score_display = '<div class="vs-circle">VS</div>'
            status = '<span style="color:#94a3b8; font-size:0.8rem;">○ BEKLENİYOR</span>'

        st.markdown(f"""
        <div class="modern-fixture">
            <div style="min-width:100px; border-right: 1px solid #f1f5f9;">
                <b style="color:#16a34a;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8;">{date.strftime('%d.%m.%Y')}</small>
            </div>
            <div class="fixture-teams">
                <span>{h.upper()}</span>
                {score_display}
                <span>{a.upper()}</span>
            </div>
            <div style="min-width:100px; text-align:right;">
                {status}
            </div>
        </div>
        """, unsafe_allow_html=True)
