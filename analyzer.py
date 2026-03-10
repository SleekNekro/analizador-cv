import ollama


def analizar_cv(texto_cv: str, oferta: str = "") -> dict:
    prompt_base = f"""
Eres un experto en recursos humanos. Analiza el siguiente CV y responde en español.

CV:
{texto_cv}
"""

    prompt_oferta = f"""
Oferta de trabajo:
{oferta}

Puntúa la compatibilidad del CV con la oferta del 1 al 100.
""" if oferta else ""

    prompt_completo = prompt_base + prompt_oferta + """
Responde con este formato exacto:

PERFIL: (resumen en 2-3 líneas)
HABILIDADES TÉCNICAS: (lista separada por comas)
HABILIDADES BLANDAS: (lista separada por comas)
PUNTOS FUERTES:
- (punto 1)
- (punto 2)
PUNTOS A MEJORAR:
- (punto 1)
- (punto 2)
SUGERENCIAS:
- (sugerencia 1)
- (sugerencia 2)
COMPATIBILIDAD: (número del 1 al 100, solo si hay oferta)
"""

    respuesta = ollama.chat(
        model="qwen3:8b",
        messages=[{"role": "user", "content": prompt_completo}]
    )

    return parsear_respuesta(respuesta["message"]["content"])


def parsear_respuesta(texto: str) -> dict:
    resultado = {
        "perfil": "",
        "habilidades_tecnicas": [],
        "habilidades_blandas": [],
        "puntos_fuertes": [],
        "puntos_mejorar": [],
        "sugerencias": [],
        "compatibilidad": None
    }

    lineas = texto.split("\n")
    seccion_actual = None

    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("PERFIL:"):
            resultado["perfil"] = linea.replace("PERFIL:", "").strip()
        elif linea.startswith("HABILIDADES TÉCNICAS:"):
            habs = linea.replace("HABILIDADES TÉCNICAS:", "").strip()
            resultado["habilidades_tecnicas"] = [h.strip() for h in habs.split(",")]
        elif linea.startswith("HABILIDADES BLANDAS:"):
            habs = linea.replace("HABILIDADES BLANDAS:", "").strip()
            resultado["habilidades_blandas"] = [h.strip() for h in habs.split(",")]
        elif linea.startswith("PUNTOS FUERTES:"):
            seccion_actual = "puntos_fuertes"
        elif linea.startswith("PUNTOS A MEJORAR:"):
            seccion_actual = "puntos_mejorar"
        elif linea.startswith("SUGERENCIAS:"):
            seccion_actual = "sugerencias"
        elif linea.startswith("COMPATIBILIDAD:"):
            try:
                num = linea.replace("COMPATIBILIDAD:", "").strip()
                resultado["compatibilidad"] = int(''.join(filter(str.isdigit, num)))
            except:
                pass
        elif linea.startswith("-") and seccion_actual:
            resultado[seccion_actual].append(linea[1:].strip())

    return resultado