"""
Marathi2India API bridge — BHASHINI ULCA inference endpoint.
Keep all credentials in server environment variables, never in browser JavaScript.
Before use, fill the values in .env using the BHASHINI pipeline configuration response
for your account and selected language pair.
"""
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Marathi2India BHASHINI Bridge", version="0.1.0")

# Replace this with your deployed PWA's exact origin before production.
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:8000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source: str = "mar_Deva"
    target: str = "eng_Latn"

@app.get("/")
def health():
    return {"service": "Marathi2India BHASHINI Bridge", "ready": bool(os.getenv("BHASHINI_CALLBACK_URL"))}

@app.post("/api/translate")
def translate(req: TranslateRequest):
    callback_url = os.getenv("BHASHINI_CALLBACK_URL", "").strip()
    auth_header = os.getenv("BHASHINI_AUTH_HEADER", "").strip()
    auth_value = os.getenv("BHASHINI_AUTH_VALUE", "").strip()
    service_id = os.getenv("BHASHINI_TRANSLATION_SERVICE_ID", "").strip()

    if not all([callback_url, auth_header, auth_value, service_id]):
        raise HTTPException(
            status_code=503,
            detail="Server configuration incomplete. Add BHASHINI_CALLBACK_URL, BHASHINI_AUTH_HEADER, BHASHINI_AUTH_VALUE and BHASHINI_TRANSLATION_SERVICE_ID from your own BHASHINI pipeline config."
        )

    # Language codes in this app use IndicTrans2-style labels. ULCA pipelines often
    # require short ISO codes (e.g. mr, en, hi); map them explicitly here.
    code_map = {
        "mar_Deva": "mr", "eng_Latn": "en", "hin_Deva": "hi",
        "ben_Beng": "bn", "guj_Gujr": "gu", "pan_Guru": "pa",
        "asm_Beng": "as", "kan_Knda": "kn", "mal_Mlym": "ml",
        "tam_Taml": "ta", "tel_Telu": "te", "ory_Orya": "or",
        "san_Deva": "sa", "npi_Deva": "ne", "mai_Deva": "mai",
        "gom_Deva": "gom", "brx_Deva": "brx", "doi_Deva": "doi",
        "kas_Deva": "ks", "kas_Arab": "ks", "mni_Beng": "mni",
        "mni_Mtei": "mni", "sat_Olck": "sat", "snd_Arab": "sd",
        "snd_Deva": "sd", "urd_Arab": "ur"
    }
    src = code_map.get(req.source)
    tgt = code_map.get(req.target)
    if not src or not tgt:
        raise HTTPException(status_code=400, detail="Unsupported language code.")

    payload = {
        "pipelineTasks": [{
            "taskType": "translation",
            "config": {
                "language": {"sourceLanguage": src, "targetLanguage": tgt},
                "serviceId": service_id
            }
        }],
        "inputData": {"input": [{"source": req.text}]}
    }
    try:
        response = requests.post(
            callback_url,
            headers={auth_header: auth_value, "Content-Type": "application/json"},
            json=payload,
            timeout=90
        )
        response.raise_for_status()
        data = response.json()
        result = data["pipelineResponse"][0]["output"][0]["target"]
        return {"translation": result}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"BHASHINI request failed: {exc.__class__.__name__}")
    except (KeyError, IndexError, TypeError, ValueError):
        raise HTTPException(status_code=502, detail="Unexpected BHASHINI response. Check service ID, language pair, and pipeline configuration.")
