import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: FORM VE TABLO ÖZELLİKLERİ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* FORM NOKTALARI */
.f-dot {
    width: 20px; height: 20px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; font-size: 10px;
    font-weight: 900; color: white; margin-right: 3px;
}
.W { background-color: #10b981; } /* Galibiyet */
.L { background-color: #ef4444; } /* Mağlubiyet */
.D { background-color: #94a3b8; } /* Beraberlik */

.league-title {
    font-size: clamp(24px, 7vw, 36px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-top: 10px;}
.custom-table th { background: #1e293b; color: white; padding: 12px 5px; font-size: 11px; text-align: center; }
.custom-table td { padding: 12px 5px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }

.pitch-container {
    background: #1a3a16; padding: 25px; border-radius: 15px; margin-top: 15px;
    background-image: repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.03) 40px, rgba(255,255,255,0.03) 80px);
    border: 2px solid #2d5a27;
}
.player-node {
    width: 32px; height: 32px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 900; color: #1e293b; border: 2px solid #fbbf24;
    margin: 5px auto;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_form_html(form_list):
    html = '<div style="display: flex; justify-content: center;">'
    for res in form_list[-5:]:
        css_class = 'W' if res == 'G' else 'L' if res == 'M' else 'D'
        html += f'<div class="f-dot {css_class}">{res}</div>'
    html += '</div>'
    return html

def get_stats():
    # Başlangıç verileri
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    # Eklenen maçları işle
    for w, m in st.session_state.matches.items():
        data[m["Ev"]]["O"]+=1; data[m["Dep"]]["O"]+=1
        data[m["Ev"]]["AG"]+=m["EvS"]; data[m["Ev"]]["YG"]+=m["DepS"]
        data[m["Dep"]]["AG"]+=m["DepS"]; data[m["Dep"]]["YG"]+=m["EvS"]
        
        if m["EvS"] > m["DepS"]:
            data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvS"] < m["DepS"]:
            data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
            
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- TABS ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_stats()
    
    st.markdown("<h5 style='font-size:14px; margin-bottom:10px;'>🏆 LİG SIRALAMASI</h5>", unsafe_allow_html=True)
    
    # Detaylı Tablo (Form Sütunu Eklendi)
    rows_html = ""
    for _, r in df.iterrows():
        form_visual = get_form_html(r['form'])
        rows_html += f"""
        <tr>
            <td style="text-align:left; padding-left:15px;">{r['Takım']}</td>
            <td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td>
            <td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td>
            <td style='color:#10b981; font-weight:900;'>{r['P']}</td>
            <td>{form_visual}</td>
        </tr>
        """
        
    t_html = f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th style="text-align:left; padding-left:15px;">TAKIM</th>
                <th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th><th>FORM</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    now = datetime.now()
    match_start, match_end = time(18, 30), time(20, 15)
    
    for week in range(11, 21):
        if week == 11:
            m_date, arena = datetime(2026, 3, 28), "Filia Arena"
        else:
            m_date = datetime(2026, 3, 29) + timedelta(weeks=(week-12))
            arena = "Velochori Arena"
            
        is_today = (now.date() == m_date.date())
        is_live = is_today and (match_start <= now.time() <= match_end)
        ev, dep = ("Billispor", "Prospor") if week % 2 != 0 else ("Prospor", "Billispor")
        res = st.session_state.matches.get(week)
        
        # Durum Mantığı
        if res:
            score_box, label = f"{res['EvS']} - {res['DepS']}", "MAÇ SONUCU"
        elif is_live:
            score_box, label = "OYNANIYOR", '<span style="color:red; font-weight:900;">● CANLI</span>'
        else:
            score_box, label = "18:30", m_date.strftime("%d.%m.%Y")

        with st.expander(f"📅 {week}. HAFTA | {ev} - {dep}", expanded=is_today):
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center;">
                <div style="font-size: 11px; color: #64748b; font-weight: 800;">📍 {arena}</div>
                <div style="margin: 5px 0;">{label}</div>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px;">
                    <div style="flex: 1; font-weight: 900;">{ev.upper()}</div>
                    <div style="background: #1e293b; color: #34d399; padding: 8px 20px; border-radius: 10px; font-size: 20px; font-weight: 900; min-width: 110px;">{score_box}</div>
                    <div style="flex: 1; font-weight: 900;">{dep.upper()}</div>
                </div>
                <div class="pitch-container">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px;">
                            <div class="player-node">?</div><div class="player-node">?</div><div class="player-node">?</div><div class="player-node">?</div>
                        </div>
                        <div style="border-left: 1px dashed rgba(255,255,255,0.2); display: grid; grid-template-columns: 1fr 1fr; gap: 5px;">
                            <div class="player-node">?</div><div class="player-node">?</div><div class="player-node">?</div><div class="player-node">?</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.header("⚙️ SKOR YÖNETİMİ")
    with st.form("admin_form"):
        h = st.number_input("Hafta", 11, 20)
        s1, s2 = st.number_input("Ev", 0), st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            ev_t, dep_t = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
            st.session_state.matches[h] = {"Ev": ev_t, "Dep": dep_t, "EvS": s1, "DepS": s2}
            st.rerun()
