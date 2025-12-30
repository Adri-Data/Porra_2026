import streamlit as st
import pandas as pd
from utils.database import GameDB
import datetime

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

@st.cache_resource
def get_db():
    return GameDB()

def predictions_page():
    st.title("🔮 Tu Futuro en 2026")
    
    db = get_db()
    players = db.get_players()
    
    if not players:
        st.error("El administrador aún no ha añadido jugadores. Por favor, contacta con el administrador.")
        return

    # Buscador de usuario
    st.markdown('<div class="question-block">', unsafe_allow_html=True)
    user_name = st.selectbox("🔍 Busca y selecciona tu nombre:", [""] + sorted(players), help="Escribe tu nombre para buscar")
    st.markdown('</div>', unsafe_allow_html=True)

    if user_name:
        with st.form("predictions_form"):
            # SECCIÓN 1: MOODBOARD VISUAL
            st.header("📸 Tu Moodboard 2026")
            st.write("Define visualmente tu año:")
            
            col_mood1, col_mood2, col_mood3 = st.columns(3)
            with col_mood1:
                mood_color = st.color_picker("Elige el color de tu año", "#ff4b2b")
            with col_mood2:
                mood_emoji = st.selectbox("Emoji de tu año", ["🚀", "✨", "💸", "🏖️", "🧘", "🔥", "🌈", "📚", "🏠", "🍕"])
            with col_mood3:
                mood_vibe = st.text_input("Año en una frase")

            # SECCIÓN 2: REFLEXIONES 2025
            st.header("📅 2025")
            
            # Palabra 2025
            st.markdown('<div class="question-block">', unsafe_allow_html=True)
            col_a1, col_a2 = st.columns([4, 1])
            skip_2025 = col_a2.checkbox("Saltar", key="skip_2025")
            p_2025 = col_a1.text_input("Define tu 2025 en una sola palabra", disabled=skip_2025)
            st.markdown('</div>', unsafe_allow_html=True)

            # Momento Top 2025 + FOTO
            st.markdown('<div class="question-block">', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns([4, 1])
            skip_top = col_d2.checkbox("Saltar", key="skip_top")
            momento_top = col_d1.text_area("¿Cuál fue el momento TOP de este año 2025?", disabled=skip_top)
            foto_top = st.file_uploader("Sube una foto de tu momento TOP (opcional)", type=["jpg", "png", "jpeg"], disabled=skip_top)
            st.markdown('</div>', unsafe_allow_html=True)

            # SECCIÓN 3: PREDICCIONES 2026
            st.header("🎯 Futuro 2026")

            # Palabra 2026
            st.markdown('<div class="question-block">', unsafe_allow_html=True)
            col_b1, col_b2 = st.columns([4, 1])
            skip_2026 = col_b2.checkbox("Saltar", key="skip_2026")
            p_2026 = col_b1.text_input("Define como sera tu 2026 en una sola palabra", disabled=skip_2026)
            st.markdown('</div>', unsafe_allow_html=True)

            # Expectativa 2026
            st.markdown('<div class="question-block">', unsafe_allow_html=True)
            col_c1, col_c2 = st.columns([4, 1])
            skip_exp = col_c2.checkbox("Saltar", key="skip_exp")
            expectativa = col_c1.text_area("¿Cómo esperas que sea 2026?", disabled=skip_exp)
            st.markdown('</div>', unsafe_allow_html=True)

            # SECCIÓN 4: SOBRE LOS DEMÁS (PREDICCIÓN GENERAL)
            st.header("👥 Predicciones de NPM")
            st.write("¿Quién será el protagonista en estos temas?")
            
            others = [p for p in players if p != user_name]
            
            # Helper para selectbox con saltar
            def select_with_skip(label, key):
                st.markdown('<div class="question-block">', unsafe_allow_html=True)
                c1, c2 = st.columns([4, 1])
                skip = c2.checkbox("Saltar", key=f"skip_{key}")
                val = c1.selectbox(label, [""] + others, key=f"val_{key}", disabled=skip)
                st.markdown('</div>', unsafe_allow_html=True)
                return val if not skip else "Saltado"

            pred_noticia = select_with_skip("¿Quién crees que dará la noticia más importante en 2026?", "noticia")
            pred_inesperada = select_with_skip("¿Quién dará la noticia más inesperada?", "inesperada")
            pred_relacion = select_with_skip("¿Quién empezará una relación que no nos esperemos?", "relacion")
            pred_anecdota = select_with_skip("¿Quién tendrá la anécdota más surrealista?", "anecdota")
            pred_frase = select_with_skip("¿Quién dirá la frase más mítica del año?", "frase")
            pred_fisico = select_with_skip("¿Quién va a hacer el mayor cambio físico este año?", "fisico")
            pred_coche = select_with_skip("¿Quién se comprará un coche este año?", "coche")

            # SECCIÓN 5: UNO POR UNO
            st.header("🧪 Análisis Personalizado")
            st.write("Dinos que esperas de cada integrante:")
            
            individual_preds = {}
            for person in others:
                st.markdown(f'<div class="question-block">', unsafe_allow_html=True)
                st.subheader(f"Sobre {person}")
                c1, c2 = st.columns([4, 1])
                skip_p = c2.checkbox("Saltar", key=f"skip_ind_{person}")
                p_text = c1.text_area(f"¿Qué crees que hará o cómo le irá a {person} este año?", key=f"text_ind_{person}", disabled=skip_p)
                individual_preds[person] = p_text if not skip_p else "Saltado"
                st.markdown('</div>', unsafe_allow_html=True)

            submit = st.form_submit_button("✨ Enviar mis predicciones")

            if submit:
                # Procesar foto si existe (la convertimos a bytes o string base64 si fuera necesario, 
                # pero por simplicidad para Google Sheets guardaremos que se subió o usaremos un placeholder)
                # NOTA: Google Sheets no guarda imágenes binarias directamente de forma fácil sin Drive.
                foto_status = "Subida ✅" if foto_top is not None else "No subida"

                final_data = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Jugador": user_name,
                    "Mood Color": mood_color,
                    "Mood Emoji": mood_emoji,
                    "Mood Vibe": mood_vibe,
                    "Palabra 2025": p_2025 if not skip_2025 else "Saltado",
                    "Momento Top 2025": momento_top if not skip_top else "Saltado",
                    "Foto Momentos": foto_status,
                    "Palabra 2026": p_2026 if not skip_2026 else "Saltado",
                    "Expectativa 2026": expectativa if not skip_exp else "Saltado",
                    "Noticia Importante": pred_noticia,
                    "Noticia Inesperada": pred_inesperada,
                    "Relacion Sorpresa": pred_relacion,
                    "Anecdota Surrealista": pred_anecdota,
                    "Frase Mitica": pred_frase,
                    "Cambio Fisico": pred_fisico,
                    "Comprara Coche": pred_coche
                }
                
                # Añadir las predicciones individuales
                for person, val in individual_preds.items():
                    final_data[f"Sobre {person}"] = val
                
                db.save_prediction(final_data)
                st.success("¡Tus predicciones han sido guardadas con éxito! Nos vemos en 2026.")
                st.balloons()

if __name__ == "__main__":
    predictions_page()
