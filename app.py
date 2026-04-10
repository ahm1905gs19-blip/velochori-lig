import streamlit as st
import pandas as pd
import datetime

# --- 1. MODERN TASARIM VE CSS ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=JetBrains+Mono:wght@700&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

.league-title {
    font-size: 36px; font-weight: 900; text-align: center; padding: 25px 0;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

/* YENİ NESİL PUAN DURUMU TABLOSU */
.puan-container { background: white; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e2e8f0; }
.custom-table { width: 100%; border-collapse: collapse; margin: 0; }
.custom-table th { background: #f1f5f9; color: #475569; padding: 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #e2e8f0; }
.custom-table td { padding: 18px 16px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; color: #1e293b; font-size: 15px; }

/* LİDER VURGUSU */
.leader-row { background: #fffcf0 !important; }
.leader-badge { background: #fbbf24; color: #78350f; padding: 4px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; margin-left: 8px; }

/* PUAN SÜTUNU VURGUSU */
.points-col { background: #f0fdf4; color: #166534 !important; font-weight: 900 !important; font-size: 18px !important; }

/* MAÇ KARTLARI */
.stadium-card { background: white; border-radius: 16px; margin-bottom: 20px; border: 1px solid #e2e8f0; transition: transform 0.2s; }
.stadium-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.digital-scoreboard {
    background: #1e293b; color: #22c55e; font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem; display: inline-flex; align-items: center; justify-content: center;
    height: 50px; min-width: 110px; border-radius: 12px; margin: 0 30px; border: 2px solid #334155;
}

/* FORM İKONLARI */
.f-dot { width: 22px; height: 22px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #22c55e; } .L { background: #ef4444; } .D { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19}
    }

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
            data[m["Dep"]]["form"].append("G"); data[m["Ev"]]["form"].append("M")
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. ARAYÜZ ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 LİG SIRALAMASI", "🗓️ HAFTALIK PROGRAM"])

with tab1:
    df = get_live_stats()
    
    st.markdown('<div class="puan-container">', unsafe_allow_html=True)
    rows_html = ""
    for idx, r in df.reset_index(drop=True).iterrows():
        is_leader = idx == 0
        leader_class = "leader-row" if is_leader else ""
        leader_tag = '<span class="leader-badge">ŞAMPİYON ADAYI</span>' if is_leader else ""
        
        rows_html += f"""
        <tr class="{leader_class}">
            <td style="text-align:left; padding-left:25px;">
                <span style="color:#64748b; margin-right:12px;">{idx+1}</span>
                <strong>{r['Takım'].upper()}</strong>{leader_tag}
            </td>
            <td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td>
            <td>{r['AG']}</td><td>{r['YG']}</td>
            <td style="color:{'#10b981' if r['Av'] >= 0 else '#ef4444'}">{r['Av']}</td>
            <td class="points-col">{r['P']}</td>
        </tr>
        """
    
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th style="text-align:left; padding-left:25px;">TAKIMLAR</th>
                <th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FORM DURUMU
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (name, row) in enumerate(df.iterrows()):
        with cols[i]:
            dots = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in row["form"][-5:]])
            st.markdown(f"**{name} Son 5:** {dots}", unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    for i in range(10):
        w = 11 + i
        if w == 11: m_date = datetime.date(2026, 3, 28)
        elif w == 12: m_date = datetime.date(2026, 4, 9)
        else: m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-2)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card">
            <div style="background:#f8fafc; padding:10px 20px; display:flex; justify-content:space-between; font-size:12px; font-weight:800; color:#64748b; border-bottom:1px solid #e2e8f0;">
                <span>{w}. HAFTA | 📍 {stad}</span>
                <span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:25px; display:flex; align-items:center; justify-content:center;">
                <div style="flex:1; text-align:right; font-weight:800; font-size:1.1rem;">{t1}</div>
                <div class="digital-scoreboard">{"VS" if not res else f'{res["EvSkor"]} - {res["DepSkor"]}'}</div>
                <div style="flex:1; text-align:left; font-weight:800; font-size:1.1rem;">{t2}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ YÖNETİCİ PANELİ")
    h_sel = st.number_input("Hafta", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    if st.button("SKORU KAYDET"):
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
        st.rerun()
