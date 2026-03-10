# 📄 Analizador de CVs con IA

Aplicación web local que analiza CVs en PDF usando inteligencia artificial generativa.
Extrae habilidades, detecta puntos fuertes y débiles, sugiere mejoras y calcula
la compatibilidad con una oferta de trabajo.

Todo el procesamiento es **100% local**. Ningún dato sale del equipo.

---

## 🛠️ Stack técnico

| Componente | Tecnología |
|---|---|
| Interfaz | Streamlit |
| Modelo LLM | Ollama + Qwen3:8b |
| Embeddings | nomic-embed-text |
| RAG | LlamaIndex |
| Vector store | Qdrant |
| Extracción PDF | pdfplumber |

---

## 🚀 Instalación y ejecución

### Opción A — Manual (recomendada para desarrollo)

**1. Clona el repositorio**
```bash
git clone https://github.com/SleekNekro/analizador-cv
cd analizador-cv
```

**2. Crea el entorno e instala dependencias**
```bash
conda create -n proyectocv python=3.11
conda activate proyectocv
pip install -r requirements.txt
```

**3. Instala Ollama y descarga los modelos**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

**4. Arranca Qdrant**
```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
```

**5. Lanza la aplicación**
```bash
streamlit run main.py
```

Abre el navegador en `http://localhost:8501`

---

### Opción B — Docker Compose

**1. Clona el repositorio**
```bash
git clone https://github.com/SleekNekro/analizador-cv
cd analizador-cv
```

**2. Lanza todos los servicios**
```bash
docker compose up
```

**3. Descarga los modelos en el contenedor de Ollama**
```bash
docker exec ollama ollama pull qwen3:8b
docker exec ollama ollama pull nomic-embed-text
```

Abre el navegador en `http://localhost:8501`

---

## 📖 Uso

1. Sube tu CV en formato PDF
2. (Opcional) Pega una oferta de trabajo
3. Pulsa **Analizar CV**
4. Consulta el análisis completo y la puntuación de compatibilidad
5. Usa el chat para hacer preguntas concretas sobre tu CV

---

## 🔒 Privacidad

Todo el procesamiento ocurre en local. Los CVs no se envían a ningún servidor externo,
cumpliendo con el RGPD.

---

## 👤 Autor

**Iker Pérez Mata** · [GitHub](https://github.com/SleekNekro) · [LinkedIn](https://www.linkedin.com/in/iker-perez-mata03)