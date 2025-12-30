import streamlit as st

st.set_page_config(
    page_title="Predicciones 2026",
    page_icon="🔮",
    layout="wide",
)

# Estilo CSS personalizado para un look premium
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: white;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
    }
    h1 {
        font-family: 'Outfit', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-align: center;
    }
    .prediction-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔮 Predicciones 2026")
    
    # Lógica de la cuenta atrás
    from datetime import datetime
    
    target_date = datetime(2026, 1, 1, 0, 0, 0)
    now = datetime.now()
    
    if target_date > now:
        diff = target_date - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        col_c1.metric("Días", days)
        col_c2.metric("Horas", hours)
        col_c3.metric("Minutos", minutes)
        col_c4.metric("Segundos", seconds)
    else:
        st.success("¡BIENVENIDO AL 2026! 🥂")

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="prediction-card">
            <h3>Bienvenido a la porra de NPM</h3>
            <hr style="opacity: 0.1">
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 COMENZAR MI VIAJE", use_container_width=True):
            st.switch_page("pages/2_🔮_Predicciones.py")

    st.markdown("---")


if __name__ == "__main__":
    main()
