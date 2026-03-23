import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TÜM TASARIM SİSTEMİ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.live-anim { animation: blink 1.5s infinite; color: #ef4444 !important; font-weight: 900; }

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

.stadium-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border-radius: 25px; padding: 20px; margin-bottom: 15px; border: 1px solid #e2e8f0;
    display: flex; flex-direction: column; gap: 15px; position: relative; overflow: hidden;
}
.today-card { border: 2px solid #10b981 !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); }
.postponed-card { border: 2px dashed #f59e0b !important; opacity: 0.8; box-shadow: none !important; }

.digital-scoreboard {
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem; padding: 10px 25px; border-radius: 15px; text-align: center; 
    border: 2px solid #1e293b; display: flex; justify-content: center; align-items: center; min-width: 120px;
}
.vs-text { color: #64748b; font-size: 0.8rem; font-weight: 900; }
.team-name { font-size: 1.1rem; font-weight: 900; color: #1e293b; text-transform: uppercase; letter-spacing: 1px; }
.home-vibe { border-bottom: 3px solid #10b981; display: inline-block; padding: 0 5px; }
.status-pill { font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}
if 'postponed' not in st.session_state: st.session_state.postponed = []

# --- SIDEBAR: MAÇ YÖNETİMİ ---
with st.sidebar:
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    h_no = st.number_input("Hafta Seç", 11, 20, 11)
    
    with st.form("match_score"):
        ev, dep = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev}", 0, 100, 0)
        s2 = c2.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}
            if h_no in st.session_state.postponed: st.session_state.postponed.remove(h_no)
            st.rerun()
            
    if st.button("⚠️ MAÇI ERTELE"):
        if h_no not in st.session_state.postponed:
            st.session_state.postponed.append(h_no)
            if h_no in st.session_state.matches: del st.session_state.matches[h_no]
            st.rerun()

# --- ANA EKRAN ---
tab1, tab2, tab3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK YOLU"])

# (Tab 1 ve Tab 3 önceki kodlarla aynı...)

with tab2:
    start_date = datetime.date.today() 
    today = datetime.date.today()
    now = datetime.datetime.now().time()
    match_time = datetime.time(19, 30)
    
    for i in range(10):
        w = 11 + i
        m_dt = start_date + datetime.timedelta(days=7*i)
        is_today = m_dt == today
        is_postponed = w in st.session_state.postponed
        is_live = is_today and now >= match_time and not is_postponed
        
        res = st.session_state.matches.get(w)
        
        # DURUM BELİRLEME
        if res:
            status_text, status_color, status_bg = '● MAÇ BİTTİ', '#166534', '#dcfce7'
            score_display = f'<div>{res["EvSkor"]}</div><div style="font-size:1rem; color:#475569; margin:0 10px;">-</div><div>{res["DepSkor"]}</div>'
        elif is_postponed:
            status_text, status_color, status_bg = '⚠️ ERTELENDİ', '#92400e', '#fef3c7'
            score_display = '<div class="vs-text">TBD</div>'
        elif is_live:
            status_text, status_color, status_bg = '<span class="live-anim">⚽ OYNANIYOR...</span>', '#ef4444', '#fee2e2'
            score_display = '<div class="vs-text">VS</div>'
        elif is_today:
            status_text, status_color, status_bg = '🔥 MAÇ GÜNÜ', '#059669', '#ecfdf5'
            score_display = '<div class="vs-text">VS</div>'
        else:
            status_text, status_color, status_bg = '○ BEKLİYOR', '#64748b', '#f1f5f9'
            score_display = '<div class="vs-text">VS</div>'

        st.markdown(f"""
        <div class="stadium-card {'today-card' if is_today and not is_postponed else ''} {'postponed-card' if is_postponed else ''}">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="background:{'#f59e0b' if is_postponed else ('#10b981' if is_today else '#059669')}; color:white; padding:4px 12px; border-radius:50px; font-size:12px; font-weight:900;">{w}. HAFTA</span>
                    <span style="background:#1e293b; color:#fbbf24; padding:4px 10px; border-radius:8px; font-size:11px; font-weight:800; font-family:'JetBrains Mono';">🕒 19:30</span>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:15px 0;">
                <div style="flex:1; text-align:center;"><span class="team-name">{ev_t if w%2==0 else dep_t}</span></div>
                <div class="digital-scoreboard">{score_display}</div>
                <div style="flex:1; text-align:center;"><span class="team-name">{dep_t if w%2==0 else ev_t}</span></div>
            </div>
            <div style="display:flex; justify-content:center;"><div class="status-pill" style="background:{status_bg}; color:{status_color};">{status_text}</div></div>
        </div>
        """, unsafe_allow_html=True)
