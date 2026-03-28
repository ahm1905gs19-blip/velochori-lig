import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: SOFASCORE PRESTİJ TASARIMI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* CANLI YAYIN PARLAMASI */
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
.live-badge { 
    color: #ef4444; font-weight: 900; font-size: 11px; 
    animation: pulse 1.5s infinite; background: #fee2e2;
    padding: 2px 10px; border-radius: 6px; border: 1px solid #fecaca;
    display: inline-block; margin-bottom: 8px;
}

/* LİG BAŞLIĞI */
.league-title {
    font-size: clamp(24px, 7vw, 36px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* TAKIM KARTLARI */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 15px 20px; border-radius: 15px; 
    margin-bottom: 10px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

/* SAHA VE DİZİLİŞ */
.pitch-container {
    background: #1a3a16; padding: 25px; border-radius: 15px; margin-top: 15px;
    background-image: repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.03) 40px, rgba(255,255,255,0.03) 80px);
    border: 2px solid #2d5a27;
}
.player-node {
    width: 32px; height: 32px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 900; color: #1e293b; border: 2px solid #fbbf24;
    margin: 5px auto; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

/* DETAYLI TABLO (AG-YG-AV ÖZEL) */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
.custom-table th { background: #1e293b; color: white; padding: 12px 8px; font-size: 11px; text-align: center; }
.custom-table td { padding: 12px 8px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA (AG-YG GARANTİLİ) ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w, m in st.session_state.matches.items():
        data[m["Ev"]]["O"]+=1; data[m["Dep"]]["O"]+=1
        data[m["Ev"]]["AG"]+=m["EvS"]; data[m["Ev"]]["YG"]+=m["DepS"]
        data[m["Dep"]]["AG"]+=m["DepS"]; data[m["Dep"]]["YG"]+=m["EvS"]
        res = "G" if m["EvS"] > m["DepS"] else "M" if m["EvS"] < m["DepS"] else "B"
        if res=="G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res=="M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- TABS ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_stats()
    # Üst Kartlar
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = (idx == 0)
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <div style="font-size:10px; font-weight:900; color:#94a3b8;">{ "🥇 LİDER" if is_l else f"SIRA {idx+1}"}</div>
                <div style="font-size:20px; font-weight:900; color:#1e293b;">{r['Takım'].upper()}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:32px; font-weight:900; color:#10b981; line-height:1;">{r['P']}<small style="font-size:12px; color:#94a3b8; margin-left:4px;">P</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detaylı Tablo (AG-YG-AV BURADA)
    st.markdown("<h5 style='margin-top:20px; font-size:14px;'>📈 GENEL SIRALAMA</h5>", unsafe_allow_html=True)
    t_html = f"""
    <table class="custom-table">
        <thead>
            <tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    now = datetime.now()
    match_start = time(18, 30)
    match_end = time(20, 15)
    
    for week in range(11, 21):
        if week == 11:
            m_date = datetime(2026, 3, 28)
            arena = "Filia Arena"
        else:
            m_date = datetime(2026, 3, 29) + timedelta(weeks=(week-12))
            arena = "Velochori Arena"
            
        is_today = (now.date() == m_date.date())
        is_live = is_today and (match_start <= now.time() <= match_end)
        
        ev, dep = ("Billispor", "Prospor") if week % 2 != 0 else ("Prospor", "Billispor")
        res = st.session_state.matches.get(week)
        
        # Skor/Zaman Durumu
        if res:
            score_box = f"{res['EvS']} - {res['DepS']}"
            time_label = "MAÇ SONUCU"
        elif is_live:
            score_box = "OYNANIYOR"
            time_label = '<div class="live-badge">● CANLI</div>'
        else:
            score_box = "18:30"
            time_label = m_date.strftime("%d.%m.%Y")

        with st.expander(f"📅 {week}. HAFTA | {ev.upper()} - {dep.upper()}", expanded=is_today):
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center;">
                <div style="font-size: 12px; font-weight: 800; color: #64748b; margin-bottom: 5px;">📍 {arena}</div>
                <div style="margin-bottom: 10px;">{time_label}</div>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px;">
                    <div style="flex: 1; font-weight: 900; font-size: 18px;">{ev.upper()}</div>
                    <div style="background: #1e293b; color: #34d399; padding: 8px 20px; border-radius: 10px; font-size: 22px; font-weight: 900; min-width: 120px;">{score_box}</div>
                    <div style="flex: 1; font-weight: 900; font-size: 18px;">{dep.upper()}</div>
                </div>
                <div class="pitch-container">
                    <div style="color: rgba(255,255,255,0.4); font-size: 10px; font-weight: 800; margin-bottom: 15px;">SAHA DİZİLİŞİ</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div class="player-node">?</div><div class="player-node">?</div>
                            <div class="player-node">?</div><div class="player-node">?</div>
                            <div class="player-node">?</div><div class="player-node">?</div>
                        </div>
                        <div style="border-left: 2px dashed rgba(255,255,255,0.1); display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div class="player-node">?</div><div class="player-node">?</div>
                            <div class="player-node">?</div><div class="player-node">?</div>
                            <div class="player-node">?</div><div class="player-node">?</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.header("⚙️ SKOR GİRİŞİ")
    with st.form("admin_form"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0); s2 = st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            ev_t, dep_t = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
            st.session_state.matches[h] = {"Ev": ev_t, "Dep": dep_t, "EvS": s1, "DepS": s2}
            st.rerun()
