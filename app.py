import streamlit as st
import pandas as pd
import datetime

# --- 1. SAYFA VE GENEL TASARIM ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* ANİMASYONLAR */
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
@keyframes border-glow { 0% { border-color: #10b981; } 50% { border-color: #fbbf24; } 100% { border-color: #10b981; } }

.live-anim { animation: blink 1.5s infinite; background: #ef4444; color: white; padding: 3px 12px; border-radius: 4px; font-weight: 900; font-size: 11px; }
.match-day-badge { background: #fbbf24; color: #000; padding: 3px 12px; border-radius: 4px; font-weight: 900; font-size: 11px; }

/* PUAN DURUMU KARTLARI */
.team-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 18px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #e2e8f0; }
.leader-card { border: 1.5px solid #fbbf24; background: linear-gradient(135deg, #fffcf0 0%, #ffffff 100%); }
.f-dot { width: 18px; height: 18px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
.points-text { font-size: 26px; font-weight: 900; color: #10b981; line-height: 1; }
.av-text { font-weight: 700; color: #64748b; font-size: 11px; }

/* MAÇ MERKEZİ */
.stadium-card { background: white; border-radius: 15px; margin-bottom: 15px; border: 1px solid #e2e8f0; overflow: hidden; }
.match-day-card { border: 2.5px solid #fbbf24 !important; animation: border-glow 2s infinite; }
.digital-scoreboard { background: #273142; color: #00ff85; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; padding: 6px 15px; border-radius: 8px; min-width: 90px; text-align: center; border: 1px solid #334155; margin: 0 35px; }
.team-name { font-size: 1rem; font-weight: 800; color: #1e293b; text-transform: uppercase; flex: 1; }

.league-title { font-size: 32px; font-weight: 900; text-align: center; padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-top: 10px; }
.custom-table th { background: #1e293b; color: white; padding: 10px; font-size: 11px; text-align: center; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ VE TARİH ---
if 'matches' not in st.session_state:
    st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}

# TÜRKİYE SAATİ
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
        res = "G" if m["EvSkor"] > m["DepSkor"] else "M" if m["EvSkor"] < m["DepSkor"] else "B"
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res == "G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res == "M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR YÖNETİMİ")
    with st.form("admin_form"):
        h = st.number_input("Hafta", 11, 20, 12)
        ev, dep = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
        st.info(f"{h}. Hafta: {ev} vs {dep}")
        s1 = st.number_input(f"{ev}", 0, 100, 0); s2 = st.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}; st.rerun()
    if st.button("Ligi Sıfırla"):
        st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}; st.rerun()

# --- 4. ANA PANEL ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    # Kart Tasarımları
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""<div class="team-card {'leader-card' if is_lider else ''}"><div style="flex:1;"><span style="font-size:9px; font-weight:900; color:{'#b45309' if is_lider else '#64748b'};">{ '🏆 LİDER' if is_lider else f'{idx+1}. SIRADA'}</span><div class="team-title">{r['Takım'].upper()}</div><div style="display:flex;">{form_html}</div></div><div style="text-align:right; display:flex; align-items:center; gap:15px;"><div class="av-text">AV: {r['Av']}</div><div class="points-text">{r['P']}</div></div></div>""", unsafe_allow_html=True)
    
    # Detaylı Puan Tablosu (Geri Geldi!)
    st.markdown("#### 📉 DETAYLI TABLO")
    st.markdown(f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>""", unsafe_allow_html=True)

with tab2:
    start_t, end_t = 1830, 2015
    base_date = datetime.date(2026, 3, 28)
    for i in range(10):
        w = 11 + i
        match_date = base_date + datetime.timedelta(weeks=i)
        is_today = (today_date == match_date)
        res = st.session_state.matches.get(w)
        
        if res:
            status = '● BİTTİ'; score = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_today:
            if cur_time_int < start_t: status = '<span class="match-day-badge">🔥 MAÇ GÜNÜ</span>'; score = '18:30'
            elif start_t <= cur_time_int <= end_t: status = '<span class="live-anim">⚽ OYNANIYOR...</span>'; score = 'LIVE'
            else: status = '🕒 BEKLENİYOR'; score = 'VS'
        else: status = f'🕒 18:30'; score = 'VS'

        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        st.markdown(f"""<div class="stadium-card {'match-day-card' if is_today and not res else ''}"><div style="background:#f8fafc; padding:8px 15px; display:flex; justify-content:space-between; font-size:10px; font-weight:800;"><span style="color:#64748b;">{w}. HAFTA</span><span style="color:{'#fbbf24' if is_today else '#94a3b8'};">{"📅 BUGÜN" if is_today else match_date.strftime('%d.%m.%Y')}</span></div><div style="padding:15px 20px; display:flex; align-items:center; justify-content:center;"><div class="team-name" style="text-align:right;">{t1}</div><div class="digital-scoreboard">{score}</div><div class="team-name" style="text-align:left;">{t2}</div></div><div style="background:#f8fafc; padding:8px; text-align:center; font-size:10px; font-weight:800; border-top:1px solid #f1f5f9;">{status}</div></div>""", unsafe_allow_html=True)
