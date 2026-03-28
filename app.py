import streamlit as st
import pandas as pd
import datetime

# --- 1. PREMIUM GÖRKEMLİ TASARIM ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="🏆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #0f172a; font-family: 'Inter', sans-serif; color: #f8fafc; }

/* ANİMASYONLAR VE GÖRKEM EFEKTLERİ */
@keyframes gold-pulse { 0% { box-shadow: 0 0 0 0 rgba(251, 191, 36, 0.5); } 70% { box-shadow: 0 0 0 15px rgba(251, 191, 36, 0); } 100% { box-shadow: 0 0 0 0 rgba(251, 191, 36, 0); } }
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
@keyframes border-glow { 0% { border-color: #10b981; } 50% { border-color: #fbbf24; } 100% { border-color: #10b981; } }

.live-anim { animation: blink 1.5s infinite; background: #ef4444; color: white; padding: 3px 12px; border-radius: 4px; font-weight: 900; font-size: 11px; }
.match-day-badge { background: #fbbf24; color: #000; padding: 3px 12px; border-radius: 4px; font-weight: 900; font-size: 11px; }

/* PUAN DURUMU KARTLARI (Kompakt ama Görkemli) */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: rgba(255, 255, 255, 0.05); padding: 12px 18px; border-radius: 12px; 
    margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.1); 
    backdrop-filter: blur(10px);
}
.leader-card { 
    border: 2px solid #fbbf24 !important; 
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%) !important; 
    animation: gold-pulse 2.5s infinite; 
}

.f-dot { width: 18px; height: 18px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
.team-title { margin: 2px 0; color: #f8fafc; font-size: 0.95rem; font-weight: 800; text-transform: uppercase; }
.points-text { font-size: 32px; font-weight: 900; color: #10b981; line-height: 1; }
.av-text { font-weight: 700; color: #94a3b8; font-size: 11px; }

/* MAÇ MERKEZİ (Dijital Kompakt) */
.stadium-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.1); overflow: hidden; backdrop-filter: blur(10px); }
.match-day-card { border: 2.5px solid #fbbf24 !important; animation: border-glow 2s infinite; }
.digital-scoreboard { 
    background: #1e293b; color: #00ff85; font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; 
    padding: 6px 15px; border-radius: 8px; min-width: 95px; text-align: center; 
    border: 2px solid #334155; box-shadow: inset 0 0 10px #000;
}
.team-name { font-size: 1.05rem; font-weight: 800; color: #f8fafc; text-transform: uppercase; flex: 1; }

/* KÜÇÜLTÜLMÜŞ BAŞLIK */
.title-container { text-align: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
.league-title { font-size: 24px; font-weight: 900; background: linear-gradient(90deg, #059669, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.league-sub { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; }

/* DETAYLI TABLO (Geri Geldi ve Geliştirildi) */
.custom-table { width: 100%; border-collapse: collapse; background: rgba(255, 255, 255, 0.03); border-radius: 12px; overflow: hidden; margin-top: 15px; }
.custom-table th { background: rgba(0, 0, 0, 0.3); color: #fbbf24; padding: 12px; font-size: 11px; text-align: center; text-transform: uppercase; letter-spacing: 1px; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-weight: 600; font-size: 13px; color: #e2e8f0; }
.custom-table tr:hover { background: rgba(255, 255, 255, 0.05); }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ VE TARİH YÖNETİMİ ---
if 'matches' not in st.session_state:
    # 11. Hafta skorun otomatik yüklendi (Ölçüm yapılması için)
    st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}

# TÜRKİYE SAATİ AYARI (Canlı Durumlar İçin)
now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
cur_time_int = now.hour * 100 + now.minute
today_date = now.date()

def get_live_stats():
    # 10. Hafta Sonu Verileri
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    
    # 11. Hafta ve sonrasını hesapla
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
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. ANA PANEL ---
st.markdown('<div class="title-container"><div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div><div class="league-sub">Season 2026 • Ultimate Control</div></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CANLI PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    # Şık ve Kompakt Takım Kartları
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        
        lider_badge = '<span style="font-size:10px; font-weight:900; color:#fbbf24; letter-spacing:1px; margin-right:5px;">🏆 ŞAMPİYON ADAYI</span>' if is_lider else ''
        
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_lider else ''}">
            <div style="flex:1;">
                <div style="display:flex; align-items:center; margin-bottom:2px;">
                    {lider_badge}
                    <span style="font-size:9px; font-weight:900; color:{'#94a3b8' if not is_lider else '#facc15'};">{ 'LİDER' if is_lider else f'{idx+1}. SIRADA'}</span>
                </div>
                <div class="team-title">{r['Takım'].upper()}</div>
                <div style="display:flex; margin-top:4px;">{form_html}</div>
            </div>
            <div style="text-align:right; display:flex; align-items:center; gap:20px;">
                <div class="av-text">AVERAY: {r['Av']}</div>
                <div class="points-text">{r['P']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detaylı Puan Tablosu (Geri Geldi!)
    st.markdown("#### 📉 DETAYLI TABLO")
    st.markdown(f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900; font-size:1.1rem;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>""", unsafe_allow_html=True)

with tab2:
    start_time, end_time = 1830, 2015
    base_match_date = datetime.date(2026, 3, 28) # 11. Hafta başlangıcı
    
    for i in range(10): # 11. haftadan 20. haftaya kadar
        week_num = 11 + i
        match_date = base_match_date + datetime.timedelta(weeks=i)
        is_today = (today_date == match_date)
        res = st.session_state.matches.get(week_num)
        
        # Durum Belirleme Mantığı
        if res: status = '● BİTTİ'; score_show = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_today:
            if cur_time_int < start_time: status = '<span class="match-day-badge">🔥 MAÇ GÜNÜ</span>'; score_show = '18:30'
            elif start_time <= cur_time_int <= end_time: status = '<span class="live-anim">⚽ OYNANIYOR...</span>'; score_show = 'LIVE'
            else: status = '🕒 BEKLENİYOR'; score_show = 'VS'
        else: status = f'🕒 18:30'; score_show = 'VS'

        t1, t2 = ("Billispor", "Prospor") if week_num % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card {'match-day-card' if is_today and not res else ''}">
            <div style="background:rgba(255, 255, 255, 0.02); padding:8px 15px; display:flex; justify-content:space-between; font-size:11px; font-weight:800; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                <span style="color:#94a3b8;">{week_num}. HAFTA</span>
                <span style="color:{'#fbbf24' if is_today else '#94a3b8'};">{"📅 BUGÜN" if is_today else match_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:18px 25px; display:flex; align-items:center; justify-content:center;">
                <div class="team-name" style="text-align:right;">{t1}</div>
                <div class="digital-scoreboard">{score_show}</div>
                <div class="team-name" style="text-align:left;">{t2}</div>
            </div>
            <div style="background:rgba(255, 255, 255, 0.02); padding:8px; text-align:center; font-size:11px; font-weight:800; border-top:1px solid rgba(255, 255, 255, 0.05); color: #e2e8f0;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏆 LİG YÖNETİMİ")
    with st.form("admin_form"):
        h = st.number_input("Hafta", 11, 20, 12)
        ev, dep = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
        st.info(f"{h}. Hafta Maçı: {ev} vs {dep}")
        s1 = st.number_input(f"{ev} Skor", 0, 100, 0); s2 = st.number_input(f"{dep} Skor", 0, 100, 0)
        if st.form_submit_button("SKORU KAYDET"):
            st.session_state.matches[h] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}; st.rerun()
    if st.button("Ligi Sıfırla (Başlangıca Dön)"):
        st.session_state.matches = {11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}}; st.rerun()
