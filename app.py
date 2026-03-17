import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Pro Lig", page_icon="⚽", layout="wide")

# --- GELİŞMİŞ CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

.league-title {
    font-size: clamp(30px, 7vw, 60px);
    font-weight: 900;
    text-align: center;
    padding: 25px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* SIRALAMA KARTLARI */
.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 20px; border-radius: 20px;
    margin-bottom: 15px; border: 1px solid #e2e8f0;
    flex-wrap: wrap; gap: 15px;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.f-dot {
    width: 24px; height: 24px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 900; color: white; margin-right: 4px;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MODERN DETAYLI TABLO */
.custom-table {
    width: 100%; border-collapse: collapse; background: white;
    border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 12px; text-align: center; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 14px; }
.custom-table tr:hover { background: #f8fafc; }
.col-p { color: #10b981; font-weight: 900; font-size: 16px; }

/* GELİŞMİŞ FİKSTÜR */
.match-card {
    background: white; border-radius: 15px; padding: 15px 20px;
    margin-bottom: 10px; display: flex; align-items: center;
    justify-content: space-between; border-left: 5px solid #e2e8f0;
    transition: all 0.3s;
}
.match-card:hover { border-left-color: #10b981; transform: translateX(5px); }
.match-done { border-left-color: #10b981; background: #f0fdf4; }

.score-box {
    background: #1e293b; color: white; padding: 6px 16px;
    border-radius: 8px; font-weight: 900; font-size: 1.2rem;
    min-width: 80px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_live_stats():
    # Başlangıç verileri
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
            data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📥 SKOR GİRİŞİ")
    with st.form("sc_in"):
        h = st.number_input("Hafta", 11, 20, 11)
        ev, dep = ("Prospor", "Billispor") if h % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev}", 0, 100, 0)
        s2 = c2.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}
            st.rerun()

# --- SEKMELER ---
t1, t2 = st.tabs(["📊 CANLI SIRALAMA", "🗓️ MAÇ MERKEZİ"])

with t1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1; min-width:200px;">
                <span style="background:{'#fbbf24' if is_l else '#f1f5f9'}; padding:2px 8px; border-radius:5px; font-size:10px; font-weight:900;">{ 'LİDER 👑' if is_l else f'RANK {idx+1}'}</span>
                <h2 style="margin:5px 0; color:#1e293b;">{r['Takım'].upper()}</h2>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="display:flex; align-items:center; gap:30px;">
                <div style="text-align:right;">
                    <div style="font-weight:800; color:#64748b; font-size:13px;">AVERAGE: {r['Av']}</div>
                    <div style="font-size:11px; color:#94a3b8;">{r['AG']} AG / {r['YG']} YG</div>
                </div>
                <div style="font-size:40px; font-weight:900; color:#10b981;">{r['P']}<small style="font-size:12px; color:#94a3b8; margin-left:4px;">PTS</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📝 DETAYLI PERFORMANS TABLOSU")
    # HTML Tablo ile 0-1 indekslerinden kurtulup tasarımı uçuruyoruz
    table_html = f"""
    <table class="custom-table">
        <thead>
            <tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>PUAN</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td class='col-p'>{row['P']}</td></tr>" for _, row in df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

with t2:
    s_dt = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        m_dt = s_dt + datetime.timedelta(days=7*i)
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        
        card_cls = "match-card match-done" if res else "match-card"
        score = f'<div class="score-box">{res["EvSkor"]} - {res["DepSkor"]}</div>' if res else '<div style="font-weight:900; color:#cbd5e1;">VS</div>'
        st.markdown(f"""
        <div class="{card_cls}">
            <div style="width:100px;">
                <b style="color:#10b981; font-size:14px;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8;">{m_dt.strftime('%d.%m')}</small>
            </div>
            <div style="flex:1; display:flex; justify-content:center; align-items:center; gap:25px; font-weight:700;">
                <span style="text-align:right; width:100px;">{ev_t}</span>
                {score}
                <span style="text-align:left; width:100px;">{dep_t}</span>
            </div>
            <div style="width:100px; text-align:right;">
                <span style="color:{'#10b981' if res else '#94a3b8'}; font-size:11px; font-weight:800;">
                    {'● OYNANDI' if res else '○ BEKLİYOR'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
