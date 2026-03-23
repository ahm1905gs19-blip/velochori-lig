import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TASARIM SİSTEMİ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* CANLI ANİMASYONU */
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.live-anim { animation: blink 1.5s infinite; color: #ef4444 !important; font-weight: 900; }

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

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

.custom-table {
    width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden;
}
.custom-table th { background: #1e293b; color: white; padding: 10px; font-size: 12px; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; }

.stadium-card {
    background: white; border-radius: 25px; padding: 20px; margin-bottom: 15px; 
    border: 1px solid #e2e8f0; position: relative;
}
.today-card { border: 2px solid #10b981 !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.1); }
.postponed-card { border: 2px dashed #f59e0b !important; opacity: 0.8; }

.digital-scoreboard {
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem; padding: 10px 25px; border-radius: 15px; min-width: 120px; text-align: center;
}
.team-name { font-size: 1.1rem; font-weight: 900; color: #1e293b; text-transform: uppercase; }
.status-pill { font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 8px; margin-top: 10px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- SESSİON STATE VE VERİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}
if 'postponed' not in st.session_state: st.session_state.postponed = []

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
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    h_no = st.number_input("Hafta Seç", 11, 20, 11)
    ev_side, dep_side = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
    
    with st.form("match_score"):
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_side}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_side}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev_side, "EvSkor": s1, "Dep": dep_side, "DepSkor": s2}
            if h_no in st.session_state.postponed: st.session_state.postponed.remove(h_no)
            st.rerun()
            
    if st.button("⚠️ MAÇI ERTELE"):
        if h_no not in st.session_state.postponed:
            st.session_state.postponed.append(h_no)
            if h_no in st.session_state.matches: del st.session_state.matches[h_no]
            st.rerun()

# --- ANA EKRAN ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ FİKSTÜR"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f'<div class="team-card {"leader-card" if is_l else ""}"><div style="flex:1;"><span style="font-size:10px; font-weight:900;">{ "🏆 LİDER" if is_l else f"SIRA {idx+1}"}</span><h3 style="margin:0;">{r["Takım"].upper()}</h3><div style="display:flex; margin-top:5px;">{f_html}</div></div><div style="font-size:28px; font-weight:900; color:#10b981;">{r["P"]} P</div></div>', unsafe_allow_html=True)

with tab2:
    # 23 Mart 2026 Pazartesi'yi "Bugün" olarak simüle ediyoruz
    today = datetime.date(2026, 3, 23)
    start_date = today 
    now_time = datetime.datetime.now().time()
    match_time = datetime.time(19, 30)
    aylar = {"March": "Mart", "April": "Nisan", "May": "Mayıs"}
    
    for i in range(10):
        w = 11 + i
        m_dt = start_date + datetime.timedelta(days=7*i)
        is_today = (m_dt == today)
        is_postponed = w in st.session_state.postponed
        res = st.session_state.matches.get(w)
        
        # Dinamik Durum ve Saat Kontrolü
        if res:
            status, s_col, s_bg = '● MAÇ BİTTİ', '#166534', '#dcfce7'
            score = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_postponed:
            status, s_col, s_bg = '⚠️ ERTELENDİ', '#92400e', '#fef3c7'
            score = 'VS'
        elif is_today and now_time >= match_time:
            status, s_col, s_bg = '<span class="live-anim">⚽ OYNANIYOR...</span>', '#ef4444', '#fee2e2'
            score = 'VS'
        elif is_today:
            status, s_col, s_bg = '🔥 MAÇ GÜNÜ', '#059669', '#ecfdf5'
            score = 'VS'
        else:
            status, s_col, s_bg = '○ BEKLİYOR', '#64748b', '#f1f5f9'
            score = 'VS'

        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        t_str = "📅 BUGÜN" if is_today else f"{m_dt.strftime('%d')} {aylar.get(m_dt.strftime('%B'), m_dt.strftime('%B'))}"

        st.markdown(f"""
        <div class="stadium-card {'today-card' if is_today and not is_postponed else ''} {'postponed-card' if is_postponed else ''}">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span style="font-weight:900; font-size:12px; color:#64748b;">{w}. HAFTA | 🕒 19:30</span>
                <span style="font-weight:700; font-size:12px; color:#10b981;">{t_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex:1; text-align:center;" class="team-name">{ev_t}</div>
                <div class="digital-scoreboard">{score}</div>
                <div style="flex:1; text-align:center;" class="team-name">{dep_t}</div>
            </div>
            <center><div class="status-pill" style="background:{s_bg}; color:{s_col};">{status}</div></center>
        </div>
        """, unsafe_allow_html=True)
