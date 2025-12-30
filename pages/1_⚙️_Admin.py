import streamlit as st
import pandas as pd
from utils.database import GameDB

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
                    import matplotlib.pyplot as plt
                    
                    wordcloud = WordCloud(width=800, height=400, background_color='black', 
                                         colormap='magma', max_words=50).generate(palabras)
                    
                    fig, ax = plt.subplots()
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)

            with col2:
                import plotly.express as px
                st.markdown("**🚗 ¿Quién se comprará un coche?**")
                coche_counts = data['Comprara Coche'].value_counts()
                if "Saltado" in coche_counts: coche_counts = coche_counts.drop("Saltado")
                if not coche_counts.empty:
                    fig_coche = px.pie(values=coche_counts.values, names=coche_counts.index, hole=.3)
                    fig_coche.update_layout(showlegend=False, height=300, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_coche, use_container_width=True)

            st.divider()
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("**📢 Próxima Gran Noticia**")
                noticia_counts = data['Noticia Proximamente'].value_counts()
                if "Saltado" in noticia_counts: noticia_counts = noticia_counts.drop("Saltado")
                if not noticia_counts.empty:
                    fig_noticia = px.bar(noticia_counts, x=noticia_counts.index, y=noticia_counts.values)
                    st.plotly_chart(fig_noticia, use_container_width=True)

            with col4:
                st.markdown("**💪 Mayor Cambio Físico**")
                fisico_counts = data['Cambio Fisico'].value_counts()
                if "Saltado" in fisico_counts: fisico_counts = fisico_counts.drop("Saltado")
                if not fisico_counts.empty:
                    fig_fisico = px.bar(fisico_counts, x=fisico_counts.index, y=fisico_counts.values,
                                       color_discrete_sequence=['#ff4b2b'])
                    st.plotly_chart(fig_fisico, use_container_width=True)

            st.divider()
            st.markdown("**💭 Expectativas para 2026**")
            for idx, row in data.iterrows():
                if row['Expectativa 2026'] != "Saltado":
                    with st.expander(f"Ver lo que espera {row['Jugador']}"):
                        st.write(f"**Vibe:** {row.get('Mood Vibe', 'N/A')}")
                        st.write(f"**Expectativa:** {row['Expectativa 2026']}")
                        st.write(f"**Momento Top 2025:** {row.get('Momento Top 2025', 'N/A')}")

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
