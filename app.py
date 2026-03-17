import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_index_config = st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TASARIM SİSTEMİ (TÜM ÖZELLİKLER BİR ARADA) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* ANA BAŞLIK */
.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* SIRALAMA KARTLARI (KOMPAKT) */
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

/* TABLO SİSTEMİ */
.custom-table {
    width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden;
}
.custom-table th { background: #1e293b; color: white; padding: 8px; font-size: 11px; text-align: center; }
.custom-table td { padding: 8px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }

/* ÇİFTLİ ANALİZ PANELLERİ */
.analysis-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 20px; padding: 25px; color: white; border: 1px solid #334155;
    text-align: center; height: 100%;
}
.magic-number-val { font-size: 2.8rem; font-weight: 900; font-family: 'JetBrains Mono', monospace; line-height:1; }
.progress-container { background: #334155; height: 12px; border-radius: 10px; margin: 15px 0; overflow: hidden; }
.progress-bar { height: 100%; border-radius: 10px; transition: width 1s ease; }

/* FİKSTÜR KARTLARI */
.stadium-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border-radius: 25px; padding: 20px; margin-bottom: 15px; border: 1px solid #e2e8f0;
}
.digital-scoreboard {
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-size: 2rem; padding: 8px 20px; border-radius: 12px; display: flex; align-items: center; justify-content: center; min-width: 100px;
}
.team-name { font-size: 1rem; font-weight: 900; color: #1e293b; text-transform: uppercase; }
.home-vibe { border-bottom: 3px solid #10b981; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ÇEKİRDEĞİ ---
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

# --- SIDEBAR YÖNETİM ---
with st.sidebar:
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    with st.form("match_admin"):
        h_no = st.number_input("Hafta Seç", 11, 20, 11)
        ev, dep = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev}", 0, 100, 0)
        s2 = c2.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}
            st.rerun()

# --- ANA PANEL ---
tab1, tab2, tab3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK YOLU"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""<div class="team-card {'leader-card' if is_l else ''}"><div style="flex:1;"><span style="background:{'#fbbf24' if is_l else '#f1f5f9'}; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900;">{ '🏆 LİDER' if is_l else f'RANK {idx+1}'}</span><h3 style="margin:5px 0; color:#1e293b; font-size:1.1rem;">{r['Takım'].upper()}</h3><div style="display:flex;">{f_html}</div></div><div style="display:flex; align-items:center; gap:20px;"><div style="text-align:right;"><div style="font-weight:800; color:#64748b; font-size:12px;">AV: {r['Av']}</div></div><div style="font-size:32px; font-weight:900; color:#10b981;">{r['P']}<small style="font-size:12px; color:#94a3b8; margin-left:2px;">P</small></div></div></div>""", unsafe_allow_html=True)
    
    st.markdown("#### 📈 PERFORMANS ANALİZİ")
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    aylar = {"January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan", "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos", "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"}
    for i in range(10):
        w = 11 + i
        m_dt = start_date + datetime.timedelta(days=7*i)
        tarih_tr = f"{m_dt.strftime('%d')} {aylar[m_dt.strftime('%B')]} {m_dt.strftime('%Y')}"
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        score_display = f'<div>{res["EvSkor"]}</div><div style="margin:0 10px;">-</div><div>{res["DepSkor"]}</div>' if res else 'VS'
        st.markdown(f"""<div class="stadium-card"><div style="display:flex; justify-content:space-between; border-bottom:1px dashed #e2e8f0; padding-bottom:8px;"><span style="background:#059669; color:white; padding:4px 12px; border-radius:50px; font-size:11px; font-weight:900;">{w}. HAFTA</span><span style="font-size:11px; font-weight:700; color:#94a3b8;">{tarih_tr}</span></div><div style="display:flex; justify-content:space-between; align-items:center; padding:15px 0;"><div style="flex:1; text-align:center;"><span class="team-name home-vibe">{ev_t}</span></div><div class="digital-scoreboard">{score_display}</div><div style="flex:1; text-align:center;"><span class="team-name">{dep_t}</span></div></div></div>""", unsafe_allow_html=True)

with tab3:
    df = get_live_stats()
    col1, col2 = st.columns(2)
    
    for i, t_name in enumerate(["Billispor", "Prospor"]):
        me = df[df['Takım'] == t_name].iloc[0]
        rakip = df[df['Takım'] != t_name].iloc[0]
        kalan = 20 - me['O']
        max_rakip_olasi = rakip['P'] + (kalan * 3)
        sihirli = max(0, max_rakip_olasi - me['P'] + 1)
        yuzde = min(100, int((me['P'] / max_rakip_olasi * 100))) if max_rakip_olasi > 0 else 100
        gereken_g = (sihirli + 2) // 3
        
        with [col1, col2][i]:
            st.markdown(f"""
            <div class="analysis-card">
                <div style="font-size: 24px;">{'🏆' if i==0 else '🎯'}</div>
                <h3 style="color:{'#fbbf24' if i==0 else '#3b82f6'}; margin:10px 0; font-size:1.5rem;">{t_name.upper()}</h3>
                <div class="progress-container"><div class="progress-bar" style="width:{yuzde}%; background:{'#fbbf24' if i==0 else '#3b82f6'};"></div></div>
                <div style="font-size:12px; color:#cbd5e1; margin-bottom:15px;">Şampiyonluk İhtimali: <b>%{yuzde}</b></div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background:rgba(255,255,255,0.05); padding:15px; border-radius:12px;">
                    <div><div class="magic-number-val" style="color:{'#fbbf24' if i==0 else '#3b82f6'};">{sihirli}</div><div style="font-size:8px; color:#94a3b8; font-weight:800;">SİHİRLİ SAYI</div></div>
                    <div><div class="magic-number-val" style="color:#10b981;">{gereken_g}</div><div style="font-size:8px; color:#94a3b8; font-weight:800;">GEREKLİ GALİBİYET</div></div>
                </div>
                <div style="margin-top:15px; font-size:11px; color:#94a3b8; font-style:italic;">
                    * {t_name} kalan {kalan} maçta {gereken_g} galibiyetle rakibini geçebilir.
                </div>
            </div>
            """, unsafe_allow_html=True)
