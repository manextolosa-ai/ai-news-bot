import os
import time

from openai import OpenAI, RateLimitError


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

    def _fallback(reason: str) -> str:
        lines = [
            "No pude generar el briefing con OpenAI (cuota/billing).",
            f"Motivo: {reason}",
            "",
            "Titulares de hoy:",
        ]
        for a in articles[:10]:
            lines.append(f"- {a.get('title','(sin título)')} ({a.get('link','')})")
        return "\n".join(lines)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            msg = str(e)
            if "insufficient_quota" in msg:
                return _fallback("insufficient_quota: revisa Billing/créditos de OpenAI")
            time.sleep(2**attempt)

    return _fallback("Rate limit temporal (reintentos agotados)")
