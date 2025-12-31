import streamlit as st
import pandas as pd
from utils.database import GameDB
import plotly.express as px

st.set_page_config(page_title="Admin Panel", page_icon="⚙️")

st.markdown("""
<style>
    .admin-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def get_db():
    return GameDB()

def admin_page():
    st.title("⚙️ Panel de Control")
    db = get_db()
    # Autenticación desde secrets.toml
    password = st.sidebar.text_input("Contraseña de Admin", type="password")
    admin_pass = st.secrets.get("general", {}).get("admin_password", "2026")
    
    if password != admin_pass:
        st.warning("Introduce la contraseña correcta en la barra lateral para acceder.")
        return

    tab1, tab2, tab3 = st.tabs(["👥 Jugadores", "📊 Insights", "📂 Datos Crudos"])

    with tab1:
        st.subheader("Gestión de Jugadores")
        new_player = st.text_input("Nombre del nuevo jugador")
        if st.button("Añadir Jugador"):
            if new_player:
                db.save_player(new_player)
                st.success(f"Jugador {new_player} añadido!")
                st.rerun()
        
        players = db.get_players()
        st.write("Jugadores actuales:")
        st.dataframe(players)

    with tab2:
        st.subheader("📊 Insights del Grupo")
        data = db.get_all_predictions()
        
        if not data.empty:
            # 🖼️ MOODBOARD GALLERY
            st.markdown("### 🖼️ Galería de Auras 2026")
            
            # Crear collage con PIL si se solicita
            if st.button("🎨 Generar Collage del Grupo"):
                from PIL import Image, ImageDraw, ImageFont
                import io
                
                # Configuración del collage
                cols = 4
                rows = (len(data) + cols - 1) // cols
                tile_size = 200
                img = Image.new('RGB', (cols * tile_size, rows * tile_size), color='#1e1e2f')
                draw = ImageDraw.Draw(img)
                
                for i, (_, row) in enumerate(data.iterrows()):
                    r, c = divmod(i, cols)
                    x, y = c * tile_size, r * tile_size
                    color = row.get('Mood Color', '#ff4b2b')
                    
                    # Dibujar cuadrado de color
                    draw.rectangle([x, y, x + tile_size, y + tile_size], fill=color)
                    
                    # Añadir nombre y emoji (simplificado sin fuentes externas para evitar errores)
                    name = row['Jugador'][:10]
                    emoji = row.get('Mood Emoji', '✨')
                    draw.text((x + 10, y + 10), f"{emoji}\n{name}", fill='white')
                
                # Mostrar y permitir descarga
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                st.image(img, caption="Collage de Auras 2026")
                st.download_button("📥 Descargar Collage", buf.getvalue(), "collage_2026.png", "image/png")

            st.divider()
            
            # Resto de Insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔮 El 2026 en una palabra**")
                palabras = " ".join(data['Palabra 2026'].dropna().astype(str))
                palabras = palabras.replace("Saltado", "")
                
                if palabras.strip():
                    from wordcloud import WordCloud
                    
                    wordcloud = WordCloud(width=800, height=400, background_color='black', 
                                         colormap='magma', max_words=50).generate(palabras)
                    
                    st.image(wordcloud.to_image(), use_container_width=True)


            # --- SECCIÓN 1: EL MUNDO EN 2026 ---
            st.markdown("### 🌍 El Mundo en 2026")
            col_m1, col_m2, col_m3 = st.columns(3)
            
            def get_top_vote(column_name):
                if column_name in data.columns:
                    counts = data[column_name].value_counts()
                    if not counts.empty:
                        return counts.index[0], counts.values[0]
                return "N/A", 0

            with col_m1:
                top_m, v_m = get_top_vote('Ganador Mundial')
                st.metric("Favorito Mundial ⚽", top_m, f"{v_m} votos")
            with col_m2:
                top_c, v_c = get_top_vote('Ganador Champions')
                st.metric("Favorito Champions 🏆", top_c, f"{v_c} votos")
            with col_m3:
                top_l, v_l = get_top_vote('Ganador Liga')
                st.metric("Favorito Liga 🇪🇸", top_l, f"{v_l} votos")

            with st.expander("Ver todas las predicciones mundiales (Necroporra, Elecciones...)"):
                world_cols = ['Ganador Mundial', 'Ganador Champions', 'Ganador Liga', 'Ganador SuperBowl', 'Elecciones España', 'Necroporra', 'Mision Artemis', 'Avengers Hit', 'Bombazo Famosos']
                available_cols = [c for c in world_cols if c in data.columns]
                if available_players := data['Jugador'].tolist():
                    for idx, row in data.iterrows():
                        st.markdown(f"**{row['Jugador']}**")
                        for c in available_cols:
                            if not pd.isna(row.get(c)):
                                st.write(f"- *{c}*: {row[c]}")
                        st.divider()

            st.divider()

            # --- SECCIÓN 2: PREDICCIONES GRUPALES ---
            st.markdown("### 🫂 Porra de Grupo (NPM)")
            
            group_keys = [
                ('Noticia Importante', '#ff4b2b'),
                ('Noticia Inesperada', '#6a11cb'),
                ('Relacion Sorpresa', '#ff0080'),
                ('Anecdota Surrealista', '#2575fc'),
                ('Frase Mitica', '#00d2ff'),
                ('Cambio Fisico', '#3a7bd5'),
                ('Comprara Coche', '#f2994a')
            ]
            
            # Mostrar en una cuadrícula de 2 columnas
            for i in range(0, len(group_keys), 2):
                c1, c2 = st.columns(2)
                for j, (key, color) in enumerate(group_keys[i:i+2]):
                    col = c1 if j == 0 else c2
                    with col:
                        if key in data.columns:
                            st.markdown(f"**🎯 {key}**")
                            counts = data[key].value_counts()
                            if "" in counts.index: counts = counts.drop("")
                            if not counts.empty:
                                fig = px.bar(counts, x=counts.index, y=counts.values, 
                                             color_discrete_sequence=[color])
                                fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.write(f"Sin datos de {key}")

            st.divider()

            # --- SECCIÓN 3: INSIGHTS PERSONALES ---
            st.markdown("### 💭 Expectativas y Análisis 1 a 1")
            
            players_list = data['Jugador'].tolist()
            selected_p = st.selectbox("Selecciona un jugador para ver su reporte completo:", players_list)
            
            if selected_p:
                p_row = data[data['Jugador'] == selected_p].iloc[0]
                col_p1, col_p2 = st.columns(2)
                
                with col_p1:
                    st.markdown(f"#### El 2025 de {selected_p}")
                    st.write(f"**Palabra:** {p_row.get('Palabra 2025', 'N/A')}")
                    st.write(f"**¿Cómo le ha ido?:** {p_row.get('Descripcion 2025', 'N/A')}")
                    st.write(f"**Momento TOP:** {p_row.get('Momento Top 2025', 'N/A')}")
                
                with col_p2:
                    st.markdown(f"#### El 2026 de {selected_p}")
                    st.write(f"**Palabra:** {p_row.get('Palabra 2026', 'N/A')}")
                    st.write(f"**Expectativa:** {p_row.get('Expectativa 2026', 'N/A')}")
                
                st.markdown("#### 💌 Lo que dicen los demás sobre él/ella:")
                for other_p in players_list:
                    if other_p != selected_p:
                        col_key = f"Sobre {selected_p}"
                        if col_key in data.columns:
                            other_row = data[data['Jugador'] == other_p].iloc[0]
                            opinion = other_row.get(col_key)
                            if opinion and opinion != "Saltado":
                                with st.chat_message(other_p):
                                    st.write(f"**Para {selected_p}:** {opinion}")

        else:
            st.write("Aún no hay datos para mostrar insights.")

    with tab3:
        st.subheader("Descargar Datos")
        data = db.get_all_predictions()
        if not data.empty:
            st.dataframe(data)
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Descargar CSV",
                csv,
                "predicciones_2026.csv",
                "text/csv"
            )

if __name__ == "__main__":
    admin_page()
