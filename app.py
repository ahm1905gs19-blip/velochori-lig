import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- BAŞLANGIÇ VERİSİ (MAÇ EKLİ) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}
    }

# --- SAAT ---
now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

# --- PUAN HESAPLAMA ---
def get_live_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }

    history = {"Billispor": [18], "Prospor": [12]}

    for w in sorted(st.session_state.matches):
        m = st.session_state.matches[w]

        ev, dep = m["Ev"], m["Dep"]
        evs, deps = m["EvSkor"], m["DepSkor"]

        data[ev]["O"] += 1
        data[dep]["O"] += 1

        data[ev]["AG"] += evs
        data[ev]["YG"] += deps

        data[dep]["AG"] += deps
        data[dep]["YG"] += evs

        if evs > deps:
            data[ev]["P"] += 3
            data[ev]["G"] += 1
            data[dep]["M"] += 1
            data[ev]["form"].append("G")
            data[dep]["form"].append("M")
        elif deps > evs:
            data[dep]["P"] += 3
            data[dep]["G"] += 1
            data[ev]["M"] += 1
            data[dep]["form"].append("G")
            data[ev]["form"].append("M")
        else:
            data[ev]["P"] += 1
            data[dep]["P"] += 1
            data[ev]["B"] += 1
            data[dep]["B"] += 1
            data[ev]["form"].append("B")
            data[dep]["form"].append("B")

        history["Billispor"].append(data["Billispor"]["P"])
        history["Prospor"].append(data["Prospor"]["P"])

    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]

    return df.sort_values(["P", "Av"], ascending=False), history

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Yönetim")

    with st.form("form"):
        hafta = st.number_input("Hafta", 11, 20, 12)
        ev, dep = ("Billispor", "Prospor") if hafta % 2 != 0 else ("Prospor", "Billispor")

        st.write(f"{ev} vs {dep}")

        s1 = st.number_input("Ev Skor", 0, 100, 0)
        s2 = st.number_input("Dep Skor", 0, 100, 0)

        if st.form_submit_button("Kaydet"):
            st.session_state.matches[hafta] = {
                "Ev": ev,
                "EvSkor": s1,
                "Dep": dep,
                "DepSkor": s2
            }
            st.rerun()

    if st.button("Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- ANA ---
st.title("🏆 VELOCHORI SUPER LEAGUE")

tab1, tab2, tab3 = st.tabs(["📊 Puan Durumu", "📅 Maçlar", "📈 Analiz"])

df, history = get_live_stats()

# --- PUAN DURUMU ---
with tab1:
    st.dataframe(df, use_container_width=True)

# --- MAÇLAR ---
with tab2:
    for h in range(11, 21):
        m = st.session_state.matches.get(h)

        ev, dep = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")

        if m:
            skor = f"{m['EvSkor']} - {m['DepSkor']}"
        else:
            skor = "VS"

        st.write(f"Hafta {h}: {ev} {skor} {dep}")

# --- ANALİZ ---
with tab3:
    st.subheader("📈 Puan Grafiği")
    chart_df = pd.DataFrame(history)
    st.line_chart(chart_df)

    st.subheader("🏆 Şampiyonluk İhtimali")

    lider = df.iloc[0]
    ikinci = df.iloc[1]

    fark = lider["P"] - ikinci["P"]

    if fark >= 6:
        st.success(f"{lider['Takım']} şampiyonluğa çok yakın!")
    elif fark >= 3:
        st.info("Yarış avantajlı gidiyor")
    else:
        st.warning("Şampiyonluk yarışı çok yakın!")
