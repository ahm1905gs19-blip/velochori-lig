import streamlit as st
import pandas as pd
import datetime

# --- 1. AÇIK VE GÖRKEMLİ PREMIUM TASARIM ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="🏆", layout="wide")

st.markdown("""
<style>
/* Modern ve Açık Fontlar */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Roboto+Mono:wght@700&display=swap');

.stApp { 
    background: #fdfdfd; 
    font-family: 'Montserrat', sans-serif; 
    color: #1e293b; 
}

/* BAŞLIK TASARIMI */
.title-container { text-align: center; padding: 20px 0; margin-bottom: 20px; border-bottom: 2px solid #f1f5f9; }
.league-title { 
    font-size: 28px; 
    font-weight: 900; 
    letter-spacing: -1px;
    background: linear-gradient(90deg, #0f172a, #334155);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* GÖRKEMLİ LİDER KARTI (ALTIN EFEKTLİ) */
@keyframes gold-glow { 0% { box-shadow: 0 0 5px #fbbf24; } 50% { box-shadow: 0 0 20px #fbbf24; } 100% { box-shadow: 0 0 5px #fbbf24; } }
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 15px 25px; border-radius: 20px; 
    margin-bottom: 12px; border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}
.leader-card { 
    border: 2px solid #fbbf24 !important; 
    background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%) !important;
    animation: gold-glow 3s infinite;
}

/* PUAN VE FORM TASARIMI */
.points-text { font-size: 36px; font-weight: 900; color: #10b981; line-height: 1; }
.f-dot { width: 20px; height: 20px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MAÇ MERKEZİ DİJİTAL TABELA */
.digital-scoreboard { 
    background: #0f172a; color: #00ff85; font-family: 'Roboto Mono', monospace; font-size: 1.3rem; 
    padding: 8px 20px; border-radius: 12px; min-width: 100px; text-align: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.stadium-card { 
    background: white; border-radius: 20px; margin-bottom: 15px; 
    border: 1px solid #e2e8f0; overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

/* LİG TABLOSU */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 15px; overflow: hidden; margin-top: 15px; border: 1px solid #f1f5f9; }
.custom-table th { background: #f8fafc; color: #64748b; padding: 15px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
.custom-table td { padding: 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state:
    # 11. Hafta: Billispor 16 - 15 Prospor (Sisteme dahil)
    st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}

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
st.markdown('<div class="title-container"><div class="league-title">VELOCHORI SUPER LEAGUE</div><p style="font-size:10px; font-weight:700; color:#64748b; margin:0;">PREMIUM SEASON 2026</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_lider else ''}">
            <div style="flex:1;">
                <span style="font-size:10px; font-weight:900; color:{'#fbbf24' if is_lider else '#94a3b8'}; letter-spacing:1px;">{ '🏆 LİDER' if is_lider else f'{idx+1}. SIRADA'}</span>
                <div style="font-size:1.3rem; font-weight:900; color:#1e293b; margin:2px 0;">{r['Takım'].upper()}</div>
                <div style="display:flex;">{form_html}</div>
            </div>
            <div style="text-align:right; display:flex; align-items:center; gap:25px;">
                <div style="font-weight:700; color:#64748b; font-size:12px;">AVERAJ: {r['Av']}</div>
                <div class="points-text">{r['P']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr><th>SIRALAMA</th><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{i+1}</td><td style='text-align:left; padding-left:20px;'>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-size:1.2rem;'>{row['P']}</td></tr>" for i, row in df.iterrows()])}
        </tbody>
    </table>
    """, unsafe_allow_html=True)

with tab2:
    base_date = datetime.date(2026, 3, 28)
    for i in range(10):
        w = 11 + i
        match_date = base_date + datetime.timedelta(weeks=i)
        is_today = (today_date == match_date)
        res = st.session_state.matches.get(w)
        
        status = '● BİTTİ' if res else '🕒 18:30'
        score = f'{res["EvSkor"]} - {res["DepSkor"]}' if res else "VS"
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card" style="border-left: 5px solid {'#fbbf24' if is_today else '#e2e8f0'};">
            <div style="background:#f8fafc; padding:8px 20px; display:flex; justify-content:space-between; font-size:11px; font-weight:800; color:#64748b;">
                <span>{w}. HAFTA</span><span>{match_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:20px; display:flex; align-items:center; justify-content:center;">
                <div style="flex:1; text-align:right; font-weight:900; font-size:1.1rem;">{t1}</div>
                <div style="margin: 0 30px;" class="digital-scoreboard">{score}</div>
                <div style="flex:1; text-align:left; font-weight:900; font-size:1.1rem;">{t2}</div>
            </div>
            <div style="text-align:center; padding-bottom:10px; font-size:10px; font-weight:900; color:#94a3b8; letter-spacing:1px;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ YÖNETİM")
    with st.form("admin"):
        h = st.number_input("Hafta", 11, 20, 12)
        ev, dep = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
        s1 = st.number_input(f"{ev}", 0, 100, 0); s2 = st.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}; st.rerun()
