import streamlit as st
import pandas as pd
import datetime

# --- 1. FİKSTÜR ODAKLI ELİT TASARIM ---
st.set_page_config(page_title="Velochori Fixture Control", page_icon="🗓️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@700&display=swap');

.stApp { background: #fcfcfd; font-family: 'Plus Jakarta Sans', sans-serif; }

/* FİKSTÜR BAŞLIKLARI */
.fixture-header {
    font-size: 32px; font-weight: 800; color: #1e293b;
    margin-bottom: 5px; text-align: left; letter-spacing: -1px;
}
.section-label {
    color: #64748b; font-size: 14px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 30px;
}

/* ZAMAN ÇİZGELESİ KARTI */
.timeline-card {
    background: white;
    border-radius: 24px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.timeline-card:hover { 
    transform: translateX(10px);
    box-shadow: 20px 20px 60px #d1d9e6, -20px -20px 60px #ffffff;
}

/* TARİH BLOĞU */
.date-badge {
    min-width: 80px; text-align: center;
    padding-right: 25px; border-right: 2px solid #f1f5f9;
    margin-right: 25px;
}
.date-day { font-size: 24px; font-weight: 800; color: #1e293b; line-height: 1; }
.date-month { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }

/* TAKIMLAR VE SKOR */
.match-info { flex: 3; display: flex; align-items: center; justify-content: space-between; }
.team-box { flex: 1; font-weight: 700; font-size: 1.1rem; color: #334155; }
.score-box {
    background: #f1f5f9; color: #1e293b; padding: 10px 20px;
    border-radius: 12px; font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem; margin: 0 30px; min-width: 100px; text-align: center;
}
.next-match-pill {
    background: #0ea5e9; color: white; padding: 5px 15px;
    border-radius: 20px; font-size: 11px; font-weight: 800;
    position: absolute; top: -10px; right: 30px;
}

/* STADYUM ETİKETİ */
.stadium-tag {
    flex: 1; text-align: right; font-size: 12px;
    color: #64748b; font-weight: 600;
}
.status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    display: inline-block; margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ VE FİKSTÜR MANTIĞI ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15, "Tarih": datetime.date(2026, 3, 28)},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19, "Tarih": datetime.date(2026, 4, 9)}
    }

stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]

# --- 3. EKRAN TASARIMI ---
st.markdown('<div class="fixture-header">Fikstür Takvimi</div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Velochori Super League • Gelecek ve Geçmiş Maçlar</div>', unsafe_allow_html=True)

# Fikstür Sekmeleri
tab_future, tab_past = st.tabs(["🚀 GELECEK MAÇLAR", "⏪ GEÇMİŞ SONUÇLAR"])

with tab_future:
    for i in range(13, 21):
        # 13. Hafta 19 Nisan Pazar, sonrası her Pazar
        m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-13)
        stad = stadiums[i % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if i % 2 != 0 else ("Prospor", "Billispor")
        
        is_next = (i == 13) # En yakın maç vurgusu
        pill = '<div class="next-match-pill">SIRADAKİ MAÇ</div>' if is_next else ""
        
        st.markdown(f"""
        <div class="timeline-card" style="{'border-left: 5px solid #0ea5e9' if is_next else ''}">
            {pill}
            <div class="date-badge">
                <div class="date-day">{m_date.day}</div>
                <div class="date-month">NİSAN</div>
            </div>
            <div class="match-info">
                <div class="team-box" style="text-align:right;">{t1}</div>
                <div class="score-box" style="background:white; border:1px solid #e2e8f0; color:#94a3b8;">VS</div>
                <div class="team-box" style="text-align:left;">{t2}</div>
            </div>
            <div class="stadium-tag">
                <span class="status-dot" style="background:#fbbf24;"></span>{stad}<br>
                <span style="font-size:10px;">SAAT: 18:30</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_past:
    for h in sorted(st.session_state.matches.keys(), reverse=True):
        m = st.session_state.matches[h]
        stad = stadiums[h % len(stadiums)]
        
        st.markdown(f"""
        <div class="timeline-card">
            <div class="date-badge">
                <div class="date-day">{m['Tarih'].day}</div>
                <div class="date-month">{"MART" if m['Tarih'].month == 3 else "NİSAN"}</div>
            </div>
            <div class="match-info">
                <div class="team-box" style="text-align:right;">{m['Ev']}</div>
                <div class="score-box">{m['EvSkor']} - {m['DepSkor']}</div>
                <div class="team-box" style="text-align:left;">{m['Dep']}</div>
            </div>
            <div class="stadium-tag">
                <span class="status-dot" style="background:#10b981;"></span>{stad}<br>
                <span style="font-size:10px; color:#10b981;">TAMAMLANDI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Yan Panel (Hızlı Skor Girişi)
with st.sidebar:
    st.markdown("### 🏆 Lig Yönetimi")
    st.info("Sıradaki maçı onaylamak veya skor girmek için aşağıdaki alanı kullanın.")
    with st.form("quick_score"):
        h_sel = st.number_input("Hafta", 11, 20, 13)
        t1, t2 = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
        st.write(f"**{t1} vs {t2}**")
        s1 = st.number_input(f"{t1} Skoru", 0, 100, 0)
        s2 = st.number_input(f"{t2} Skoru", 0, 100, 0)
        if st.form_submit_button("Skoru Sisteme İşle"):
            # Tarih hesaplama mantığıyla kaydet
            m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=h_sel-13) if h_sel >= 13 else datetime.date.today()
            st.session_state.matches[h_sel] = {
                "Ev": t1, "EvSkor": s1, "Dep": t2, "DepSkor": s2, "Tarih": m_date
            }
            st.success(f"{h_sel}. Hafta sonuçları kaydedildi!")
            st.rerun()
