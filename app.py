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

/* ANIMASYONLAR */
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.live-anim { animation: blink 1.5s infinite; color: #ef4444 !important; font-weight: 900; }

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* KART VE TABLO TASARIMLARI */
.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 15px 25px; border-radius: 18px;
    margin-bottom: 12px; border: 1px solid #e2e8f0;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.f-dot {
    width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; 
    justify-content: center; font-size: 11px; font-weight: 900; color: white; margin-right: 4px;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

.stadium-card {
    background: white; border-radius: 25px; padding: 20px; margin-bottom: 15px; border: 1px solid #e2e8f0;
}
.postponed-card { border: 2px dashed #f59e0b !important; background: #fffaf0; }

.digital-scoreboard {
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem; padding: 10px 25px; border-radius: 15px; min-width: 130px; text-align: center;
}

/* ANALIZ KARTI */
.analysis-card {
    background: #1e293b; border-radius: 30px; padding: 40px; color: white;
    text-align: center; border: 1px solid #334155; position: relative; overflow: hidden;
}
.magic-number { font-size: 5rem; font-weight: 900; color: #fbbf24; line-height: 1; }
.progress-container { background: #334155; height: 20px; border-radius: 10px; margin: 20px 0; }
.progress-bar { background: #10b981; height: 100%; border-radius: 10px; transition: width 1s; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERI VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_live_stats():
    # Başlangıç verileri (10. hafta sonu)
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    # Yeni girilen maçları ekle
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
    with st.form("admin_panel"):
        h_no = st.number_input("Hafta Seç", 11, 20, 11)
        ev_s, dep_s = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_s}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_s}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU KAYDET"):
            st.session_state.matches[h_no] = {"Ev": ev_s, "EvSkor": s1, "Dep": dep_s, "DepSkor": s2}
            st.rerun()

# --- ANA PANEL ---
tab1, tab2, tab3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK ANALİZİ"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f'<div class="team-card {"leader-card" if is_l else ""}"><div style="flex:1;"><span style="background:{"#fbbf24" if is_l else "#f1f5f9"}; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900;">{ "🏆 LİDER" if is_l else f"RANK {idx+1}"}</span><h3 style="margin:5px 0; color:#1e293b; font-size:1.2rem;">{r["Takım"].upper()}</h3><div style="display:flex;">{f_html}</div></div><div style="font-size:35px; font-weight:900; color:#10b981;">{r["P"]}<small style="font-size:15px; color:#94a3b8; margin-left:3px;">P</small></div></div>', unsafe_allow_html=True)

with tab2:
    today = datetime.date.today()
    now_time = datetime.datetime.now().time()
    match_time = datetime.time(19, 30)
    
    for i in range(10):
        w = 11 + i
        m_dt = today + datetime.timedelta(days=7*i)
        is_today = m_dt == today
        res = st.session_state.matches.get(w)
        
        # Dinamik Durumlar
        is_postponed = is_today and not res # Eğer bugünse ve skor girilmemişse ERTELENDİ
        is_live = is_today and now_time >= match_time and not res # Saat 19:30 geçmişse OYNANIYOR
        
        if res:
            status, s_col, s_bg = '● MAÇ BİTTİ', '#166534', '#dcfce7'
            score = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_live:
            status, s_col, s_bg = '<span class="live-anim">⚽ OYNANIYOR...</span>', '#ef4444', '#fee2e2'
            score = 'VS'
        elif is_postponed:
            status, s_col, s_bg = '⚠️ ERTELENDİ', '#92400e', '#fef3c7'
            score = 'TBD'
        else:
            status, s_col, s_bg = '○ BEKLİYOR', '#64748b', '#f1f5f9'
            score = 'VS'

        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        st.markdown(f"""
        <div class="stadium-card {'postponed-card' if is_postponed else ''}">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:12px; font-weight:800; color:#94a3b8;">
                <span>{w}. HAFTA | 🕒 19:30</span>
                <span style="color:#10b981;">{'📅 BUGÜN' if is_today else m_dt.strftime('%d %m %Y')}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex:1; text-align:center; font-weight:900; color:#1e293b;">{ev_t.upper()}</div>
                <div class="digital-scoreboard">{score}</div>
                <div style="flex:1; text-align:center; font-weight:900; color:#1e293b;">{dep_t.upper()}</div>
            </div>
            <center><div class="status-pill" style="background:{s_bg}; color:{s_col};">{status}</div></center>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    df = get_live_stats()
    lider = df.iloc[0]
    ikinci = df.iloc[1]
    
    kalan_hafta = 20 - (10 + len(st.session_state.matches))
    puan_farki = lider['P'] - ikinci['P']
    # Basit bir şampiyonluk ihtimali (kalan maçlar üzerinden)
    sihirli_puan = (kalan_hafta * 3) - puan_farki
    lig_ilerleme = ((20 - kalan_hafta) / 20) * 100

    st.markdown(f"""
    <div class="analysis-card">
        <h2 style="color:#fbbf24; margin-bottom:0;">🏆 ŞAMPİYONLUK YAKIN</h2>
        <h1 style="font-size:3.5rem; margin:10px 0;">{lider['Takım'].upper()}</h1>
        <p style="color:#94a3b8;">En yakın rakibi ile arasındaki fark: <b>{puan_farki} Puan</b></p>
        
        <div style="margin-top:30px;">
            <span style="color:#34d399; font-weight:800;">LİG TAMAMLANMA ORANI</span>
            <div class="progress-container">
                <div class="progress-bar" style="width:{lig_ilerleme}%"></div>
            </div>
            <small>{20-kalan_hafta} / 20 HAFTA OYNANDI</small>
        </div>

        <div style="display:flex; justify-content:space-around; margin-top:40px; background:rgba(255,255,255,0.05); padding:20px; border-radius:20px;">
            <div>
                <div style="font-size:0.8rem; color:#94a3b8;">KALAN MAÇ SAYISI</div>
                <div style="font-size:2rem; font-weight:900;">{kalan_hafta}</div>
            </div>
            <div>
                <div style="font-size:0.8rem; color:#94a3b8;">MAX. ALINABİLİR PUAN</div>
                <div style="font-size:2rem; font-weight:900; color:#fbbf24;">{kalan_hafta * 3}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if puan_farki > (kalan_hafta * 3):
        st.balloons()
        st.success(f"🎊 MATEMATİKSEL OLARAK ŞAMPİYON: {lider['Takım'].upper()}!")
