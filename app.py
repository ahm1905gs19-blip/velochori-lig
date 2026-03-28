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

/* CANLI ANİMASYONLAR */
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.live-anim { animation: blink 1.5s infinite; color: #ef4444 !important; font-weight: 900; }

@keyframes pulse-green {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* MAÇ MERKEZİ ŞIK TASARIM */
.stadium-card {
    background: white; border-radius: 24px; padding: 25px; margin-bottom: 20px;
    border: 1px solid #e2e8f0; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.01);
}
.stadium-card:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); }

.today-card { 
    border: 2px solid #10b981 !important; 
    background: linear-gradient(to right, #ffffff, #f0fdf4) !important;
}

.match-container { display: flex; justify-content: space-between; align-items: center; gap: 20px; width: 100%; padding: 15px 0; }
.team-box { flex: 1; min-width: 0; display: flex; align-items: center; }
.team-left { justify-content: flex-end; text-align: right; }
.team-right { justify-content: flex-start; text-align: left; }

.team-name { 
    font-size: clamp(1rem, 2.8vw, 1.4rem); font-weight: 900; color: #0f172a; 
    text-transform: uppercase; letter-spacing: -0.5px;
}

.digital-scoreboard { 
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace; 
    font-size: clamp(1.8rem, 4.5vw, 2.5rem); padding: 12px 25px; border-radius: 16px; 
    text-align: center; border: 1px solid #334155; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    min-width: 120px;
}

/* DİĞER STANDARTLAR */
.team-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 20px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #e2e8f0; }
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 20px; height: 20px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
.status-pill { font-size: 12px; font-weight: 800; padding: 6px 18px; border-radius: 100px; text-transform: uppercase; letter-spacing: 0.5px; }
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 12px; text-align: center; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 14px; }
.vs-text { color: #64748b; font-size: 0.9rem !important; font-weight: 900; opacity: 0.7; }

/* ŞAMPİYONLUK YOLU */
.championship-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 30px; padding: 40px; color: white; border: 2px solid #fbbf24; text-align: center; }
.stat-box { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
.stat-val { font-size: 1.8rem; font-weight: 900; color: #fbbf24; display: block; }
.stat-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
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
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    with st.form("match_admin"):
        h_no = st.number_input("Hafta Seç", 11, 20, 11)
        ev_s, dep_s = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_s}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_s}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev_s, "EvSkor": s1, "Dep": dep_s, "DepSkor": s2}
            st.rerun()

# --- ANA EKRAN ---
tab1, tab2, tab3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK YOLU"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f'<div class="team-card {"leader-card" if is_l else ""}"><div style="flex:1;"><span style="background:{"#fbbf24" if is_l else "#f1f5f9"}; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900;">{ "🏆 LİDER" if is_l else f"RANK {idx+1}"}</span><h3 style="margin:5px 0; color:#1e293b; font-size:1.1rem;">{r["Takım"].upper()}</h3><div style="display:flex;">{f_html}</div></div><div style="font-size:32px; font-weight:900; color:#10b981;">{r["P"]}<small style="font-size:12px; color:#94a3b8; margin-left:2px;">P</small></div></div>', unsafe_allow_html=True)
    st.markdown("#### 📈 PERFORMANS ANALİZİ")
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    today = datetime.date.today()
    aylar = {"March": "Mart", "April": "Nisan", "May": "Mayıs"}
    
    for i in range(10):
        w = 11 + i
        m_dt = today + datetime.timedelta(days=7*i)
        is_today = (m_dt == today)
        res = st.session_state.matches.get(w)
        
        if res:
            status_text, s_bg, s_color = '● BİTTİ', '#f1f5f9', '#475569'
            score_display = f'<div>{res["EvSkor"]}</div><div style="margin:0 15px; opacity:0.3;">-</div><div>{res["DepSkor"]}</div>'
        elif is_today:
            status_text, s_bg, s_color = '🔥 MAÇ GÜNÜ', '#10b981', 'white'
            score_display = '<div class="vs-text" style="color:#34d399; opacity:1;">CANLI</div>'
        else:
            status_text, s_bg, s_color = '○ BEKLİYOR', '#f8fafc', '#94a3b8'
            score_display = '<div class="vs-text">VS</div>'

        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        tarih_str = "📅 BUGÜN" if is_today else f"{m_dt.strftime('%d')} {aylar.get(m_dt.strftime('%B'), m_dt.strftime('%B'))}"

        st.markdown(f"""
        <div class="stadium-card {'today-card' if is_today else ''}">
            <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:11px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:1px;">
                <span>{w}. HAFTA • 🕒 18:30</span>
                <span style="color:{'#10b981' if is_today else '#94a3b8'}">{tarih_str}</span>
            </div>
            <div class="match-container">
                <div class="team-box team-left"><span class="team-name">{ev_t}</span></div>
                <div class="digital-scoreboard">{score_display}</div>
                <div class="team-box team-right"><span class="team-name">{dep_t}</span></div>
            </div>
            <div style="display:flex; justify-content:center; margin-top:15px;">
                <div class="status-pill" style="background:{s_bg}; color:{s_color}; border: 1px solid rgba(0,0,0,0.05);">{status_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    df = get_live_stats()
    lider = df.iloc[0]
    ikinci = df.iloc[1]
    k_hafta = 20 - lider['O']
    g_orani = int((lider['G']/lider['O'])*100) if lider['O']>0 else 0
    fark = lider['P'] - ikinci['P']

    champ_html = f"""
    <div class="championship-card">
        <div style="font-size: 3rem;">🏆</div>
        <h1 style="margin:10px 0; color:white;">{lider['Takım'].upper()}</h1>
        <p style="color:#fbbf24; font-weight:800;">ŞAMPİYONLUK YOLUNDA LİDER!</p>
        <div style="display:flex; justify-content:center; gap:10px; margin-top:20px; flex-wrap:wrap;">
            <div class="stat-box"><span class="stat-val">{lider['P']}</span><span class="stat-label">PUAN</span></div>
            <div class="stat-box"><span class="stat-val">{lider['Av']}</span><span class="stat-label">AVERAJ</span></div>
            <div class="stat-box"><span class="stat-val">{k_hafta}</span><span class="stat-label">MAÇ</span></div>
            <div class="stat-box"><span class="stat-val">%{g_orani}</span><span class="stat-label">GALİBİYET</span></div>
        </div>
        <div style="margin-top:25px; padding:15px; background:rgba(255,255,255,0.05); border-radius:15px;">
            <p style="color:#94a3b8; font-size:0.8rem; margin:0;">RAKİPLE FARK</p>
            <div style="font-size:1.8rem; font-weight:900; color:#10b981;">{fark} PUAN</div>
        </div>
    </div>
    """
    st.markdown(champ_html, unsafe_allow_html=True)
