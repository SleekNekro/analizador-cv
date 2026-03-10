import streamlit as st
import tempfile
import os
from extractor import extraer_texto_pdf
from analyzer import analizar_cv
from rag import crear_indice, consultar_cv

st.set_page_config(
    page_title="Analizador de CVs con IA",
    page_icon="📄",
    layout="wide"
)

# CSS externo
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("<h1>📄 Analizador de CVs con IA</h1>", unsafe_allow_html=True)
st.markdown("Análisis inteligente de tu CV con procesamiento 100% local.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📂 Sube tu CV")
    archivo = st.file_uploader("Selecciona un PDF", type=["pdf"])

    st.markdown("### 💼 Oferta de trabajo")
    oferta = st.text_area("Pega aquí la oferta (opcional)", height=180)

    analizar = st.button("🔍 Analizar CV")

    if "resultado" in st.session_state:
        r = st.session_state["resultado"]
        st.divider()
        st.markdown("### 📋 Resumen rápido")
        st.markdown(f"""
        <div class='sidebar-info'>
            <b>🛠️ Habilidades técnicas</b><br>
            {len(r['habilidades_tecnicas'])} detectadas<br><br>
            <b>🤝 Habilidades blandas</b><br>
            {len(r['habilidades_blandas'])} detectadas<br><br>
            <b>💪 Puntos fuertes</b><br>
            {len(r['puntos_fuertes'])} identificados<br><br>
            <b>⚠️ Puntos a mejorar</b><br>
            {len(r['puntos_mejorar'])} identificados
        </div>
        """, unsafe_allow_html=True)

        if r["compatibilidad"] and r["compatibilidad"] > 0:
            color = "#22c55e" if r["compatibilidad"] >= 70 else "#f59e0b" if r["compatibilidad"] >= 50 else "#ef4444"
            st.markdown(f"""
            <div class='card' style='text-align:center'>
                <h3>📊 Compatibilidad</h3>
                <div class='compat-score' style='color:{color}'>{r["compatibilidad"]}%</div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    if analizar and archivo:
        with st.spinner("Extrayendo texto del PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(archivo.read())
                ruta_tmp = tmp.name
            texto = extraer_texto_pdf(ruta_tmp)
            os.unlink(ruta_tmp)

        if not texto:
            st.error("❌ No se pudo extraer texto del PDF. ¿Es un PDF escaneado?")
        else:
            with st.spinner("Indexando CV con RAG..."):
                indice = crear_indice(texto)
                st.session_state["indice"] = indice

            with st.spinner("Analizando con IA..."):
                resultado = analizar_cv(texto, oferta)
                st.session_state["resultado"] = resultado

            st.rerun()

    elif analizar and not archivo:
        st.warning("⚠️ Sube un PDF antes de analizar")

    if "resultado" in st.session_state:
        r = st.session_state["resultado"]

        st.success("✅ Análisis completado")

        st.markdown(f"""
        <div class='card'>
            <h3>👤 Perfil detectado</h3>
            <p>{r['perfil']}</p>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            tags_tec = " ".join([f"<span class='tag'>🔧 {h}</span>" for h in r['habilidades_tecnicas']])
            st.markdown(f"""
            <div class='card'>
                <h3>🛠️ Habilidades técnicas</h3>
                {tags_tec}
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            tags_bland = " ".join([f"<span class='tag'>🤝 {h}</span>" for h in r['habilidades_blandas']])
            st.markdown(f"""
            <div class='card'>
                <h3>🤝 Habilidades blandas</h3>
                {tags_bland}
            </div>
            """, unsafe_allow_html=True)

        col_c, col_d = st.columns(2)
        with col_c:
            puntos = "".join([f"<p>✅ {p}</p>" for p in r['puntos_fuertes']])
            st.markdown(f"""
            <div class='card'>
                <h3>💪 Puntos fuertes</h3>
                {puntos}
            </div>
            """, unsafe_allow_html=True)

        with col_d:
            mejoras = "".join([f"<p>🔸 {p}</p>" for p in r['puntos_mejorar']])
            st.markdown(f"""
            <div class='card'>
                <h3>⚠️ Puntos a mejorar</h3>
                {mejoras}
            </div>
            """, unsafe_allow_html=True)

        sugerencias = "".join([f"<p>→ {s}</p>" for s in r['sugerencias']])
        st.markdown(f"""
        <div class='card'>
            <h3>💡 Sugerencias de mejora</h3>
            {sugerencias}
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### 💬 Pregunta sobre tu CV")
        pregunta = st.text_input("¿Qué quieres saber?",
                                  placeholder="Ej: ¿Qué experiencia tengo con bases de datos?")

        if st.button("💬 Preguntar"):
            if pregunta and "indice" in st.session_state:
                with st.spinner("Buscando en tu CV..."):
                    respuesta = consultar_cv(st.session_state["indice"], pregunta)
                st.markdown(f"""
                <div class='card'>
                    <h3>🤖 Respuesta</h3>
                    <p>{respuesta}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Escribe una pregunta primero")
    else:
        st.markdown("""
        <div class='card' style='text-align:center; padding: 3rem'>
            <h3>👈 Sube tu CV para empezar</h3>
            <p style='color:#64748b'>El análisis tarda entre 30 y 60 segundos</p>
        </div>
        """, unsafe_allow_html=True)