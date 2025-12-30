import streamlit as st
import pandas as pd
from utils.database import GameDB
import datetime
import time

st.set_page_config(page_title="Hacer Predicciones", page_icon="🔮")

st.markdown("""
<style>
    .question-block {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 5px solid #ff4b2b;
    }
</style>
""", unsafe_allow_html=True)

def get_db():
    return GameDB()

def predictions_page():
    st.title("🔮 Tu Futuro en 2026")
    
    db = get_db()
    players = db.get_players()
    
    if not players:
        st.error("El administrador aún no ha añadido jugadores. Por favor, contacta con el administrador.")
        return

    # Inicializar estado si no existe
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    # --- BARRA DE PROGRESO ---
    # Calculamos el total de pasos:
    # 0: Nombre
    # 1: Moodboard
    # 2: 2025
    # 3: 2026
    # 4-10: Social Predictions
    # 11+: Individual Analyzes
    
    # Para simplificar y que no sean 50 pasos, agruparemos por bloques lógicos "temáticos" 
    # que se sientan como "pantallas" de móvil.
    
    total_steps = 5 # Nombre, Mood, 2025, 2026, Social, Individuales
    
    # 0. SELECCIÓN DE NOMBRE (Fuera del flujo de pasos principal para bloquear)
    if st.session_state.step == 0:
        
        user_name = st.selectbox("🔍 Busca y selecciona tu nombre:", [""] + sorted(players), key="user_name_select")
        
        if user_name:
            st.session_state.form_data['Jugador'] = user_name
            if st.button("Comenzar ✨", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        return

    # Si ya tenemos nombre, mostramos progreso
    progress = (st.session_state.step - 1) / (total_steps)
    st.progress(progress)
    st.write(f"Paso {st.session_state.step} de {total_steps}")

    # --- PANTALLAS ---
    
    # PASO 1: MOODBOARD
    if st.session_state.step == 1:
        st.header("📸 Tu Moodboard 2026")
        mood_color = st.color_picker("Elige el color de tu año", st.session_state.form_data.get('Mood Color', "#ff4b2b"))
        mood_emoji = st.selectbox("Emoji de tu año", ["🚀", "✨", "💸", "🏖️", "🧘", "🔥", "🌈", "📚", "🏠", "🍕"], 
                                 index=["🚀", "✨", "💸", "🏖️", "🧘", "🔥", "🌈", "📚", "🏠", "🍕"].index(st.session_state.form_data.get('Mood Emoji', "🚀")))
        mood_vibe = st.text_input("Año en una frase", value=st.session_state.form_data.get('Mood Vibe', ""))
        st.session_state.form_data.update({"Mood Color": mood_color, "Mood Emoji": mood_emoji, "Mood Vibe": mood_vibe})

    # PASO 2: REFLEXIONES 2025
    elif st.session_state.step == 2:
        st.header("📅 Looking Back: 2025")
        p_2025 = st.text_input("Define tu 2025 en una palabra", value=st.session_state.form_data.get('Palabra 2025', ""))
        momento_top = st.text_area("¿Momento TOP?", value=st.session_state.form_data.get('Momento Top 2025', ""))
        foto_top = st.file_uploader("Sube una foto (opcional)", type=["jpg", "png", "jpeg"])
        if foto_top: st.session_state.form_data['Foto Momentos'] = "Subida ✅"
        st.session_state.form_data.update({"Palabra 2025": p_2025, "Momento Top 2025": momento_top})

    # PASO 3: PREDICCIONES 2026
    elif st.session_state.step == 3:
        st.header("🎯 Futuro 2026")
        p_2026 = st.text_input("Define tu 2026 en una palabra", value=st.session_state.form_data.get('Palabra 2026', ""))
        expectativa = st.text_area("¿Cómo esperas que sea?", value=st.session_state.form_data.get('Expectativa 2026', ""))
        st.session_state.form_data.update({"Palabra 2026": p_2026, "Expectativa 2026": expectativa})

    # PASO 4: SOBRE LOS DEMÁS (Ahora permite votarse a sí mismo)
    elif st.session_state.step == 4:
        st.header("👥 Predicciones de Grupo")
        st.write("¿Quién será el protagonista?")
        
        def input_step(label, key):
            current_val = st.session_state.form_data.get(key, "")
            options = [""] + sorted(players)
            idx = options.index(current_val) if current_val in options else 0
            val = st.selectbox(label, options, index=idx, key=f"step_{key}")
            st.session_state.form_data[key] = val

        input_step("Noticia más importante", "Noticia Importante")
        input_step("Noticia más inesperada", "Noticia Inesperada")
        input_step("Relación sorpresa", "Relacion Sorpresa")
        input_step("Anécdota surrealista", "Anecdota Surrealista")
        input_step("Frase mítica", "Frase Mitica")
        input_step("Mayor cambio físico", "Cambio Fisico")
        input_step("Se comprará un coche", "Comprara Coche")

    # PASO 5: ANÁLISIS PERSONALIZADO
    elif st.session_state.step == 5:
        st.header("🧪 Uno por Uno")
        st.write("Dinos qué esperas de cada uno:")
        
        for person in players:
            # No preguntamos por sí mismo en la sección individual para no ser repetitivo,
            # pero el usuario preguntó específicamente por Predicciones de Grupo (Paso 4).
            # Si quiere también individualmente por sí mismo, quitamos el if.
            if person != st.session_state.form_data.get('Jugador'):
                p_text = st.text_area(f"Sobre {person}...", value=st.session_state.form_data.get(f"Sobre {person}", ""), key=f"ind_{person}")
                st.session_state.form_data[f"Sobre {person}"] = p_text

    # --- NAVEGACIÓN ---
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav1:
        if st.session_state.step > 1:
            if st.button("⬅️ Anterior", use_container_width=True):
                # Guardar progreso antes de volver
                st.session_state.form_data["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.save_prediction(st.session_state.form_data)
                st.session_state.step -= 1
                st.rerun()
    
    with col_nav2:
        if st.session_state.step < total_steps:
            if st.button("Siguiente ➡️", use_container_width=True):
                # Guardar progreso al avanzar
                st.session_state.form_data["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.save_prediction(st.session_state.form_data)
                st.session_state.step += 1
                st.rerun()
        else:
            if st.button("✨ Finalizar y Enviar", use_container_width=True):
                st.session_state.form_data["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if 'Foto Momentos' not in st.session_state.form_data:
                    st.session_state.form_data['Foto Momentos'] = "No subida"
                
                db.save_prediction(st.session_state.form_data)
                st.success("¡Todo guardado con éxito! 🥂")
                st.balloons()
                # Reset para que otro pueda jugar
                st.session_state.step = 0
                st.session_state.form_data = {}
                time.sleep(3)
                st.rerun()

if __name__ == "__main__":
    predictions_page()
