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

.live-anim { animation: blink 1.5s infinite; background: #ef4444; color: white; padding: 3px 12px; border-radius: 6px; font-weight: 900; font-size: 11px; }

/* MAÇ GÜNÜ ROZETİ */
.match-day-badge {
    background: #fbbf24; color: #1e293b; padding: 4px 15px; border-radius: 20px;
    font-weight: 900; font-size: 10px; border: 1.5px solid #1e293b;
}

.league-title {
    font-size: clamp(24px, 5vw, 40px); font-weight: 900; text-align: center;
    padding: 20px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* PUAN DURUMU TASARIMI */
.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 15px 20px; border-radius: 15px;
    margin-bottom: 10px; border: 1px solid #e2e8f0;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* SKORBOARD (SİYAH KUTU) DÜZENLEMESİ */
.digital-scoreboard {
    background: #273142;
    color: #00ff85;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    padding: 6px 15px;
    border-radius: 10px;
    min-width: 90px;
    text-align: center;
    border: 1px solid #334155;
    margin: 0 45px; /* Takımlarla arayı açtık */
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.team-name { font-size: 1.1rem; font-weight: 800; color: #1e293b; text-transform: uppercase; flex: 1; }
.stadium-card { background: white; border-radius: 20px; margin-bottom: 25px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
.match-day-card { border: 2.5px solid #fbbf24 !important; animation: border-glow 2s infinite; background: #fffef9; }
.fixture-header { background: #f8fafc; padding: 12px 20px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; }

.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 11px; text-align: center; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ VE SAAT AYARLARI ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# TÜRKİYE SAATİ (Sunucu saati ne olursa olsun GMT+3 alır)
now_utc = datetime.datetime.utcnow()
now = now_utc + datetime.timedelta(hours=3)
cur_time_int = now.hour * 100 + now.minute # Örn: 1847

def get_live_stats():
    # Başlangıç verileri
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    # Kayıtlı maçları ekle
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

# --- 3. SIDEBAR (SKOR GİRİŞİ) ---
with st.sidebar:
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    with st.form("admin_panel"):
        h_no = st.number_input("Hafta Seçin", 11, 20, 11)
        # Ev/Dep sırasını haftaya göre otomatik belirle
        ev_t, dep_t = ("Billispor", "Prospor") if h_no % 2 != 0 else ("Prospor", "Billispor")
        st.write(f"**{h_no}. Hafta:** {ev_t} vs {dep_t}")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_t}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_t}", 0, 100, 0)
        if st.form_submit_button("SKORU KAYDET"):
            st.session_state.matches[h_no] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
            st.success(f"{h_no}. Hafta kaydedildi!")
            st.rerun()
    if st.button("Tüm Verileri Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- 4. ANA PANEL ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    # Lider Kartı ve Diğerleri
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_lider else ''}">
            <div style="flex:1;">
                <span style="font-size:10px; font-weight:900; background:{'#fbbf24' if is_lider else '#f1f5f9'}; padding:2px 8px; border-radius:4px;">
                    { '🏆 LİDER' if is_lider else f'{idx+1}. SIRADA'}
                </span>
                <h3 style="margin:5px 0; color:#1e293b;">{r['Takım'].upper()}</h3>
                <div style="display:flex;">{form_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:800; color:#64748b; font-size:12px;">AV: {r['Av']}</div>
                <div style="font-size:30px; font-weight:900; color:#10b981;">{r['P']}<small style="font-size:12px; color:#94a3b8; margin-left:2px;">P</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📉 DETAYLI TABLO")
    st.markdown(f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>""", unsafe_allow_html=True)

with tab2:
    start_t, end_t = 1830, 2015
    base_date = datetime.date(2026, 3, 28) # Bugün
    
    for i in range(10):
        w = 11 + i
        m_date = base_date if w == 11 else datetime.date(2026, 3, 29) + datetime.timedelta(weeks=i-1)
        is_today = (now.date() == m_date)
        res = st.session_state.matches.get(w)
        
        # CANLI DURUM MANTIĞI
        is_live = is_today and (start_t <= cur_time_int <= end_t) and not res

        if res:
            status_html = '<span>● BİTTİ</span>'
            score_txt = f'{res["EvSkor"]} - {res["DepSkor"]}'
        elif is_live:
            status_html = '<span class="live-anim">⚽ OYNANIYOR...</span>'
            score_txt = 'LIVE'
        elif is_today:
            if cur_time_int < start_t:
                status_html = '<span class="match-day-badge">🔥 MAÇ GÜNÜ</span>'
                score_txt = '18:30'
            else:
                status_html = '<span>🕒 BEKLENİYOR</span>'
                score_txt = 'VS'
        else:
            status_html = '<span>🕒 18:30</span>'
            score_txt = 'VS'

        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        tarih_label = "📅 BUGÜN" if is_today else f"{m_date.strftime('%d.%m.%Y')}"

        st.markdown(f"""
        <div class="stadium-card {'match-day-card' if is_today and not res else ''}">
            <div class="fixture-header">
                <span style="font-size:10px; font-weight:800; color:#64748b;">{w}. HAFTA</span>
                <span style="font-size:10px; font-weight:800; color:{'#fbbf24' if is_today else '#94a3b8'};">{tarih_label}</span>
            </div>
            <div style="padding: 25px 30px; display: flex; align-items: center; justify-content: center;">
                <div class="team-name" style="text-align:right;">{t1}</div>
                <div class="digital-scoreboard">{score_txt}</div>
                <div class="team-name" style="text-align:left;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:10px; text-align:center; border-top:1px solid #f1f5f9; font-size:10px; font-weight:800; color:#475569;">
                {status_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
