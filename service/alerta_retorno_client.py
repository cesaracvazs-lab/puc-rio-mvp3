import os
from datetime import date
from typing import Any, Optional

import requests
from fastapi import HTTPException

ALERTA_RETORNO_URL = os.getenv("ALERTA_RETORNO_URL", "http://127.0.0.1:8001").rstrip("/")
ALERTA_RETORNO_TIMEOUT = float(os.getenv("ALERTA_RETORNO_TIMEOUT", "5"))


def calcular_retorno(
    paciente_id: int,
    ultima_visita: date,
    situacao: str,
) -> Optional[dict[str, Any]]:
    payload = {
        "paciente_id": paciente_id,
        "ultima_visita": ultima_visita.isoformat(),
        "situacao": situacao,
    }

    try:
        resposta = requests.post(
            f"{ALERTA_RETORNO_URL}/alertas/calcular-retorno",
            json=payload,
            timeout=ALERTA_RETORNO_TIMEOUT,
        )
        resposta.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível calcular o retorno na API de Alertas.",
        ) from exc

    return resposta.json()
