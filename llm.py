import os

from openai import OpenAI


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


client = OpenAI(api_key=_require_env("OPENAI_API_KEY"))


def summarize(articles):
    if not articles:
        return "No se encontraron noticias hoy."

    text = "\n".join(f"- {a['title']}: {a.get('summary','')}" for a in articles)

    prompt = f"""\
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
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
