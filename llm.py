import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(articles):
    text = "\n".join(
        f"- {a['title']}: {a['summary']}" for a in articles
    )

    prompt = f"""
Eres un analista de inteligencia artificial.

Convierte estas noticias en un briefing diario claro:

- Máximo 10 puntos
- Clasifica por impacto: ALTO / MEDIO / BAJO
- Elimina ruido
- Sé directo

Noticias:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
