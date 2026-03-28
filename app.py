import streamlit as st
import pandas as pd
import datetime

# --- 1. PREMIUM SAYFA TASARIMI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=JetBrains+Mono:wght@700&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* ANİMASYONLAR */
@keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
@keyframes gold-glow { 0% { border-color: #fbbf24; } 50% { border-color: #f59e0b; } 100% { border-color: #fbbf24; } }

/* GENEL BİLEŞENLER */
.live-badge { animation: pulse-red 2s infinite; background: #ef4444; color: white; padding: 4px 12px; border-radius: 50px; font-weight: 900; font-size: 10px; text-transform: uppercase; }
.day-badge { background: #facc15; color: #1e293b; padding: 4px 12px; border-radius: 50px; font-weight: 900; font-size: 10px; }

/* PUAN DURUMU KARTLARI */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 15px 20px; border-radius: 16px; 
    margin-bottom: 12px; border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    transition: transform 0.2s;
}
.team-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
.leader-card { border: 2px solid #fbbf24 !important; background: linear-gradient(135deg, #fffdf5 0%, #ffffff 100%) !important; animation: gold-glow 3s infinite; }

.f-dot { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; border: 1px solid rgba(0,0,0,0.1); }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

.points-val { font-size: 32px; font-weight: 900; color: #0f172a; line-height: 1; }
.av-label { font-weight: 800; color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }

/* MAÇ MERKEZİ */
.match-box { background: white; border-radius: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.match-today { border: 2px solid #facc15 !important; }
.scoreboard { 
    background: #1e293b; color: #22c55e; font-family: 'JetBrains Mono', monospace; 
    font-size: 1.4rem; padding: 10px 20px; border-radius: 12px; min-width: 110px; 
    text-align: center; border: 2px solid #334155; 
    text-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
}
.t-name { font-size: 1.1rem; font-weight: 900; color: #1e293b; flex: 1; letter-spacing: -0.5px; }

/* LİG TABLOSU */
.custom-table { width: 100%; border-collapse: separate; border-spacing: 0; background: white; border-radius: 16px; overflow: hidden; margin-top: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.custom-table th { background: #0f172a; color: #f8fafc; padding: 15px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
.custom-table td { padding: 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; color: #334155; }
.custom-table tr:hover { background-color: #f8fafc; }

.title-container { 
    padding: 30px 0; text-align: center; 
    background: radial-gradient(circle, #ecfdf5 0%, #f8fafc 100%);
    border-radius: 20px; margin-bottom: 20px;
}
.league-title { font-size: 42px; font-weight: 900; color: #064e3b; letter-spacing: -1.5px; margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ MANTIĞI (11. Hafta 16-15 Sabitlendi) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}

# GÜNCEL ZAMAN (Türkiye)
now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
cur_time_int = now.hour * 100 + now.minute
today_date = now.date()

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
        
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["P"] += 3; data[m["Ev"]]["G"] += 1; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"] += 3; data[m["Dep"]]["G"] += 1; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. ANA PANEL ---
st.markdown('<div class="title-container"><h1 class="league-title">🏆 VELOCHORI SUPER LEAGUE</h1><p style="color:#059669; font-weight:700; margin-top:5px;">ULTIMATE SEASON 2026</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CANLI PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    col_a, col_b = st.columns([1, 1])
    
    # Takım Kartları (Üstte İki Yan Yana)
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        target_col = col_a if idx == 0 else col_b
        with target_col:
            st.markdown(f"""
            <div class="team-card {'leader-card' if is_lider else ''}">
                <div style="flex:1;">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px;">
                        <span style="font-size:11px; font-weight:900; color:{'#b45309' if is_lider else '#64748b'}; letter-spacing:1px;">{ '👑 LİDER' if is_lider else '🥈 2. SIRADA'}</span>
                    </div>
                    <div style="font-size:1.4rem; font-weight:900; color:#0f172a; margin-bottom:8px;">{r['Takım'].upper()}</div>
                    <div style="display:flex;">{form_html}</div>
                </div>
                <div style="text-align:right;">
                    <div class="av-label">AVERAJ {r['Av']}</div>
                    <div class="points-val">{r['P']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Detaylı Tablo
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr><th>SIRALAMA</th><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{i+1}</td><td style='text-align:left; padding-left:30px;'>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-size:1.1rem; font-weight:900;'>{row['P']}</td></tr>" for i, row in df.iterrows()])}
        </tbody>
    </table>
    """, unsafe_allow_html=True)

with tab2:
    start_t, end_t = 1830, 2015
    base_date = datetime.date(2026, 3, 28)
    
    for i in range(10):
        w = 11 + i
        m_date = base_date + datetime.timedelta(weeks=i)
        is_today = (today_date == m_date)
        res = st.session_state.matches.get(w)
        
        # Durum Belirleme
        if res:
            status = '● BİTTİ'; score = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_today:
            if cur_time_int < start_t: status = '<span class="day-badge">🔥 MAÇ GÜNÜ</span>'; score = '18:30'
            elif start_t <= cur_time_int <= end_t: status = '<span class="live-badge">⚽ OYNANIYOR</span>'; score = 'LIVE'
            else: status = '🕒 BEKLENİYOR'; score = 'VS'
        else: status = f'🕒 18:30'; score = 'VS'

        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="match-box {'match-today' if is_today and not res else ''}">
            <div style="background:#f1f5f9; padding:10px 20px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:900; font-size:12px; color:#475569;">{w}. HAFTA</span>
                <span style="font-weight:800; font-size:12px; color:#475569;">{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:25px; display:flex; align-items:center; justify-content:center; gap:20px;">
                <div class="t-name" style="text-align:right;">{t1}</div>
                <div class="scoreboard">{score}</div>
                <div class="t-name" style="text-align:left;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:10px; text-align:center; border-top:1px solid #e2e8f0; font-weight:800; font-size:11px; letter-spacing:1px;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏆 LİG KONTROL")
    with st.form("admin"):
        h = st.number_input("Hafta Seç", 11, 20, 12)
        ev, dep = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
        st.write(f"**Maç:** {ev} vs {dep}")
        s1 = st.number_input(f"{ev}", 0, 100, 0); s2 = st.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("SKORU KAYDET"):
            st.session_state.matches[h] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}; st.rerun()
    if st.button("Ligi Sıfırla"):
        st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}; st.rerun()
