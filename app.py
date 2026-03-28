import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TASARIM GÜNCELLEMESİ (SAAT VE SKORBOARD DÜZELTİLDİ) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* CANLI OYNANIYOR ANİMASYONU */
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
@keyframes border-glow { 0% { border-color: #10b981; } 50% { border-color: #fbbf24; } 100% { border-color: #10b981; } }

.live-anim { animation: blink 1.5s infinite; background: #ef4444; color: white; padding: 2px 10px; border-radius: 6px; font-weight: 900; }

/* MAÇ GÜNÜ ROZETİ */
.match-day-badge {
    background: #fbbf24; color: #1e293b; padding: 4px 15px; border-radius: 20px;
    font-weight: 900; font-size: 12px; border: 1.5px solid #1e293b;
    box-shadow: 0 4px 10px rgba(251, 191, 36, 0.3);
}

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* PUAN DURUMU KARTLARI */
.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 12px 20px; border-radius: 15px;
    margin-bottom: 10px; border: 1px solid #e2e8f0;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.f-dot {
    width: 20px; height: 20px; border-radius: 5px; display: flex; align-items: center; 
    justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 3px;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* FİKSTÜR VE SAAT DÜZENLEMESİ */
.stadium-card {
    background: white; border-radius: 18px; padding: 0; margin-bottom: 20px; 
    border: 1px solid #e2e8f0; overflow: hidden; position: relative;
}
.match-day-card {
    border: 2px solid #fbbf24 !important;
    animation: border-glow 2s infinite;
    background: #fffdf9;
}
.fixture-header { 
    background: #f8fafc; padding: 10px 20px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
}

/* YENİLENMİŞ DİJİTAL TABELA (KOYULUK DENGELENDİ) */
.digital-scoreboard {
    background: #273142; /* Çok az daha açık bir ton */
    color: #00ff85; /* Parlak neon yeşil */
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem; padding: 6px 22px; border-radius: 12px; min-width: 110px;
    text-align: center; border: 1px solid #334155;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.team-name { font-size: 1.1rem; font-weight: 800; color: #1e293b; flex: 1; text-transform: uppercase; }

.custom-table {
    width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden;
}
.custom-table th { background: #1e293b; color: white; padding: 10px; font-size: 11px; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA (DEĞİŞMEDİ) ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_live_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w in sorted(st.session_state.matches.keys()):
        m = st.session_state.matches[w]
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        res = "G" if m["EvSkor"] > m["DepSkor"] else "M" if m["EvSkor"] < m["DepSkor"] else "B"
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res == "G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res == "M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏟️ SKOR GİRİŞİ")
    with st.form("match_admin"):
        h_no = st.number_input("Hafta", 11, 20, 11)
        ev_s, dep_s = ("Billispor", "Prospor") if h_no % 2 != 0 else ("Prospor", "Billispor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_s}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_s}", 0, 100, 0)
        if st.form_submit_button("⚽ SONUCU KAYDET"):
            st.session_state.matches[h_no] = {"Ev": ev_s, "EvSkor": s1, "Dep": dep_s, "DepSkor": s2}
            st.rerun()

# --- ANA EKRAN ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f'<div class="team-card {"leader-card" if is_l else ""}"><div style="flex:1;"><span style="background:{"#fbbf24" if is_l else "#f1f5f9"}; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900;">{ "🏆 LİDER" if is_l else f"SIRA {idx+1}"}</span><h3 style="margin:5px 0; color:#1e293b; font-size:1.1rem;">{r["Takım"].upper()}</h3><div style="display:flex;">{f_html}</div></div><div style="display:flex; align-items:center; gap:20px;"><div style="text-align:right;"><div style="font-weight:800; color:#64748b; font-size:12px;">AV: {r["Av"]}</div></div><div style="font-size:32px; font-weight:900; color:#10b981;">{r["P"]}<small style="font-size:12px; color:#94a3b8; margin-left:2px;">P</small></div></div></div>', unsafe_allow_html=True)
    
    st.markdown("#### 📈 DETAYLI TABLO")
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    now = datetime.datetime.now()
    match_start_time = datetime.time(18, 30)
    match_end_time = datetime.time(20, 15)
    base_date = datetime.date(2026, 3, 28)
    
    for i in range(10):
        w = 11 + i
        m_dt = base_date if w == 11 else datetime.date(2026, 3, 29) + datetime.timedelta(weeks=i-1)
        arena = "Filia Arena" if w == 11 else "Velochori Arena"
        is_today = (now.date() == m_dt)
        res = st.session_state.matches.get(w)
        is_live = is_today and (match_start_time <= now.time() <= match_end_time) and not res

        if res:
            status_html = '<span>● BİTTİ</span>'
            score_html = f'<div>{res["EvSkor"]}</div><div style="font-size:1rem; opacity:0.4; margin:0 15px;">-</div><div>{res["DepSkor"]}</div>'
        elif is_live:
            status_html = '<span class="live-anim">⚽ OYNANIYOR...</span>'
            score_html = '<div style="font-size:1.2rem; color:#00ff85;">LIVE</div>'
        elif is_today:
            status_html = '<span class="match-day-badge">🔥 MAÇ GÜNÜ</span>'
            score_html = '<div style="font-size:1.2rem; color:#00ff85; letter-spacing:1px;">18:30</div>'
        else:
            status_html = f'<span>🕒 18:30</span>'
            score_html = '<div style="font-size:1.1rem; color:#94a3b8;">VS</div>'

        ev_t, dep_t = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        tarih_str = "📅 BUGÜN" if is_today else f"{m_dt.strftime('%d.%m.%Y')}"

        st.markdown(f"""
        <div class="stadium-card {'match-day-card' if is_today and not res else ''}">
            <div class="fixture-header">
                <div style="display:flex; gap:10px; align-items:center;">
                    <span style="background:#1e293b; color:white; padding:2px 10px; border-radius:6px; font-size:11px; font-weight:800;">{w}. HAFTA</span>
                    <span style="color:#64748b; font-size:11px; font-weight:700;">📍 {arena}</span>
                </div>
                <div style="font-size:11px; font-weight:800; color:{'#fbbf24' if is_today else '#94a3b8'};">{tarih_str}</div>
            </div>
            <div style="padding: 25px 30px; display: flex; align-items: center; justify-content: space-between;">
                <div class="team-name" style="text-align:right;">{ev_t}</div>
                <div class="digital-scoreboard">{score_html}</div>
                <div class="team-name" style="text-align:left;">{dep_t}</div>
            </div>
            <div style="background:{'#fffbeb' if is_today else '#f8fafc'}; padding:10px; text-align:center; border-top:1px solid #f1f5f9; font-size:11px; font-weight:800; color:#475569;">
                {status_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
