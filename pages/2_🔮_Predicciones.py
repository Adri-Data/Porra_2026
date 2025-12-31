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

    # Total de bloques lógicos (pantallas)
    total_steps = 5 # 2025, 2026 Personal, 2026 Mundo, Grupo, Individuales
    
    # 0. SELECCIÓN DE NOMBRE (Bloqueo inicial)
    if st.session_state.step == 0:
        user_name = st.selectbox("🔍 Busca y selecciona tu nombre:", [""] + sorted(players), key="user_name_select")
        
        if user_name:
            st.session_state.form_data['Jugador'] = user_name
            if st.button("Comenzar ✨", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        return

    # Progreso visual
    progress = (st.session_state.step - 1) / (total_steps)
    st.progress(progress)
    st.write(f"Paso {st.session_state.step} de {total_steps}")

    # Lista de jugadores para las preguntas grupales
    all_players = sorted(players)

    # --- PANTALLAS ---
    
    # PASO 1: REFLEXIONES 2025
    if st.session_state.step == 1:
        st.header("📅 Despídete del 2025")
        p_2025_word = st.text_input("Define tu 2025 en una sola palabra", value=st.session_state.form_data.get('Palabra 2025', ""))
        p_2025_desc = st.text_area("¿Qué te ha parecido este año? Cuéntanos un poco", value=st.session_state.form_data.get('Descripcion 2025', ""))
        momento_top = st.text_area("¿Cuál fue tu momento TOP?", value=st.session_state.form_data.get('Momento Top 2025', ""))
        foto_top = st.file_uploader("Sube una foto de ese momento (opcional)", type=["jpg", "png", "jpeg"])
        
        if foto_top: st.session_state.form_data['Foto Momentos'] = "Subida ✅"
        st.session_state.form_data.update({
            "Palabra 2025": p_2025_word, 
            "Descripcion 2025": p_2025_desc,
            "Momento Top 2025": momento_top
        })

    # PASO 2: PREDICCIONES 2026 (PERSONAL)
    elif st.session_state.step == 2:
        st.header("🎯 Tu 2026")
        p_2026_word = st.text_input("Define como sera tu 2026 en una sola palabra", value=st.session_state.form_data.get('Palabra 2026', ""))
        expectativa = st.text_area("¿Cómo crees que te irá este año? ¿Qué esperas?", value=st.session_state.form_data.get('Expectativa 2026', ""))
        st.session_state.form_data.update({
            "Palabra 2026": p_2026_word, 
            "Expectativa 2026": expectativa
        })

    # PASO 3: EL MUNDO EN 2026 (NUEVO)
    elif st.session_state.step == 3:
        st.header("🌍 La Porra Mundial")
        st.write("¿Qué pasará en el mundo en 2026?")
        
        def world_input(label, key, type="text"):
            if type == "text":
                val = st.text_input(label, value=st.session_state.form_data.get(key, ""))
            elif type == "select":
                options = ["", "Sí", "No", "Tal vez"]
                current = st.session_state.form_data.get(key, "")
                idx = options.index(current) if current in options else 0
                val = st.selectbox(label, options, index=idx)
            st.session_state.form_data[key] = val

        st.subheader("🏆 Deportes")
        world_input("Mundial 2026: ¿Quién ganará la final del mundial en NY?", "Ganador Mundial")
        world_input("Champions League 2026: ¿Quién será el ganador de la Champions League?", "Ganador Champions")
        world_input("La Liga 25/26: ¿Quién será el campeón de la La Liga?", "Ganador Liga")
        
        st.divider()
        st.subheader("⚖️ Política y Actualidad")
        world_input("¿Crees que habrá Elecciones Generales en España en 2026?", "Elecciones España", type="select")
        world_input("Necroporra: ¿Qué famoso palma este año?", "Necroporra")
       
    # PASO 4: SOBRE LOS DEMÁS (Permite autovoto)
    elif st.session_state.step == 4:
        st.header("👥 Predicciones de Grupo")
        st.write("¿Quién crees que será el protagonista?")
        
        def group_vote(label, key):
            current_val = st.session_state.form_data.get(key, "")
            options = [""] + all_players
            idx = options.index(current_val) if current_val in options else 0
            val = st.selectbox(label, options, index=idx, key=f"step_{key}")
            st.session_state.form_data[key] = val

        group_vote("¿Quién dará la noticia más importante en 2026?", "Noticia Importante")
        group_vote("¿Quién dará la noticia más inesperada?", "Noticia Inesperada")
        group_vote("¿Quién empezará una relación sorpresa?", "Relacion Sorpresa")
        group_vote("¿Quién tendrá la anécdota más surrealista?", "Anecdota Surrealista")
        group_vote("¿Quién dirá la frase más mítica del año?", "Frase Mitica")
        group_vote("¿Quién va a hacer el mayor cambio físico?", "Cambio Fisico")
        group_vote("¿Quién se comprará un coche este año?", "Comprara Coche")

    # PASO 5: ANÁLISIS PERSONALIZADO
    elif st.session_state.step == 5:
        st.header("🧪 Uno por Uno")
        st.write(f"Dinos qué esperas de cada integrante de NPM para este 2026:")
        
        current_user = st.session_state.form_data.get('Jugador')
        for person in all_players:
            if person != current_user:
                p_text = st.text_area(f"¿Qué hará o cómo le irá a {person}?", 
                                     value=st.session_state.form_data.get(f"Sobre {person}", ""), 
                                     key=f"ind_{person}")
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
