import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM (Tüm yapı korunup detaylar zirveye taşındı)
st.markdown("""
<style>
.stApp { background: #ffffff; }

/* O EFSANE BAŞLIK - DOKUNULMADI */
.league-title {
    font-size: 65px;
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

/* TAKIM KARTI */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px 30px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    transition: all 0.3s ease;
}

.team-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }

.leader { 
    border: 2px solid #fbbf24; 
    background: linear-gradient(90deg, #fffdf2, #ffffff); 
}

.stats-right { display: flex; gap: 30px; align-items: center; }

.points-val { font-size: 38px; font-weight: 900; color: #16a34a; }

.av-val {
    font-size: 16px; font-weight: 700; color: #64748b;
    background: #f8fafc; padding: 6px 15px; border-radius: 10px; border: 1px solid #e2e8f0;
}

/* MODERN FİKSTÜR */
.modern-fixture {
    background: #ffffff;
    border: 1px solid #f1f5f9;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s;
}

.modern-fixture:hover { background: #f0fdf4; border-color: #bbf7d0; }

.fixture-teams {
    display: flex; align-items: center; gap: 25px; flex-grow: 1;
    justify-content: center; font-weight: 800; font-size: 1.2rem;
}

.vs-badge {
    background: #16a34a; color: white; padding: 4px 12px;
    border-radius: 8px; font-size: 0.7rem; font-weight: 900;
}

.score-box {
    font-size: 1.8rem; font-weight: 900; color: #16a34a;
    min-width: 100px; text-align: center;
}

/* ANALİZ KUTUSU */
.analysis-card {
    background: #1e293b; color: white; padding: 20px;
    border-radius: 15px; margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR (YÖNETİCİ PANELİ)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/824/824726.png", width=100)
    st.title("Admin Paneli")
    with st.form("score_form"):
        week_input = st.number_input("Hafta Seç", min_value=11, max_value=20, value=11)
        is_even = week_input % 2 == 0
        h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
        st.divider()
        st.subheader(f"{h_team} - {a_team}")
        h_score = st.number_input("Ev Sahibi", min_value=0, step=1)
        a_score = st.number_input("Deplasman", min_value=0, step=1)
        if st.form_submit_button("⚽ SKORU KAYDET"):
            st.session_state.matches[week_input] = {"Ev": h_team, "EvSkor": h_score, "Dep": a_team, "DepSkor": a_score}
            st.rerun()
    
    if st.button("🗑️ Verileri Temizle"):
        st.session_state.matches = {}
        st.rerun()

# HESAPLAMA MOTORU (Goller: 150-154 Sabitlendi)
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
tab1, tab2, tab3 = st.tabs(["📊 CANLI PUAN DURUMU", "📅 FİKSTÜR & SONUÇLAR", "🔮 LİG ANALİZİ"])

with tab1:
    df = get_standings()
    
    # Canlı Özet Kartları
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Maç Sayısı", f"{df['O'].sum() // 2}")
    c2.metric("Gol Sayısı", f"{df['AG'].sum()}")
    c3.metric("Lider", f"{df.iloc[0]['Takım']}")
    c4.metric("Kalan Hafta", f"{20 - (10 + len(st.session_state.matches))}")

    st.write("---")
    
    for i, row in df.iterrows():
        l_class = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {l_class}">
            <div>
                <b style="font-size:24px; color:#1e293b;">{i+1}. {row['Takım'].upper()}</b><br>
                <span style="color:#94a3b8; font-weight:600;">{row['G']} Galibiyet • {row['B']} Beraberlik • {row['M']} Mağlubiyet</span>
            </div>
            <div class="stats-right">
                <div class="av-val">AVERAGE: {row['Av']}</div>
                <div class="points-val">{row['P']} <small style="font-size:14px; color:#94a3b8;">PTS</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🔍 Tüm Detayları Gör"):
        st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    
    for i in range(10):
        w = 11 + i
        date = start_date + datetime.timedelta(days=7*i)
        h = "Prospor" if w % 2 == 0 else "Billispor"
        a = "Billispor" if h == "Prospor" else "Prospor"
        
        is_done = w in st.session_state.matches
        if is_done:
            m = st.session_state.matches[w]
            score_content = f"<div class='score-box'>{m['EvSkor']} - {m['DepSkor']}</div>"
            status = '<span style="color:#16a34a; font-weight:800;">● BİTTİ</span>'
        else:
            score_content = '<div class="vs-badge">HENÜZ OYNANMADI</div>'
            status = '<span style="color:#94a3b8;">○ BEKLEMEDE</span>'

        st.markdown(f"""
        <div class="modern-fixture">
            <div style="min-width:120px;">
                <span style="color:#16a34a; font-weight:900;">{w}. HAFTA</span><br>
                <small style="color:#94a3b8;">{date.strftime('%d %B %Y')}</small>
            </div>
            <div class="fixture-teams">
                <span>{h.upper()}</span>
                {score_content}
                <span>{a.upper()}</span>
            </div>
            <div style="min-width:120px; text-align:right;">
                {status}
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    df = get_standings()
    lider = df.iloc[0]['Takım']
    st.markdown(f"""
    <div class="analysis-card">
        <h3>🚀 Şampiyonluk Analizi</h3>
        <p>Mevcut verilere göre <b>{lider}</b> şampiyonluk yolunda avantajlı görünüyor.</p>
        <hr>
        <p>💡 <i>Not: Matematiksel olarak ligin bitmesine daha zaman var. Her maç dengeleri değiştirebilir!</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Performans Grafiği")
    st.bar_chart(df.set_index("Takım")["P"])
