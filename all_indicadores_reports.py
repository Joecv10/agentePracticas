# run_all_indicadores.py
from datetime import datetime
import os
import openai
import pandas as pd
import helpers
from pathlib import Path
from openai_utils import chat_completion_with_retry
from dotenv import load_dotenv
from prompt_helper import build_prompt
from typing import Callable, Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

# --------- configuración ----------
INDICADORES = [91, 92, 93, 94, 95, 96]
EXCEL_FILE = "files/encuesta.xlsx"   # ruta al archivo
REPORTS_DIR = Path("reports")
MODEL = "gpt-4.1"              # ajusta si quieres
TEMPERATURE = 0.4
os.makedirs(REPORTS_DIR, exist_ok=True)
# -----------------------------------


def generate_reports(excel_path: str | Path, progress_update: Optional[Callable[[float, str], None]] = None) -> list[Path]:

    df = pd.read_excel(excel_path)
    generated: list[Path] = []

    # little test
    total = len(INDICADORES)
    done = 0

    # ---------- procesar cada indicador ----------

    for num in INDICADORES:
        try:
            block = helpers.get_block(df, num)
        except ValueError:
            print(f"⚠️  Indicador {num} no encontrado, se omite.")
            continue

        # — filtramos carreras que respondieron "Sí" (ajusta si procede) —
        rows = [
            helpers.parse_row(block.iloc[i])
            for i in range(len(block))
            if str(block.iloc[i, 0]).strip().lower().startswith(("si", "sí"))
        ]
        if not rows:
            print(f"⚠️  Indicador {num}: sin filas válidas, se omite.")
            continue

        agg = helpers.aggregate_rows(rows)

    # ---------- prompt ----------
        prompt_system = "Eres un redactor académico. Usa el estilo formal del informe adjunto."
        prompt_user = build_prompt(num, agg)

        messages = [
            {"role": "system", "content": prompt_system},
            {"role": "user",   "content": prompt_user},
        ]

        report_text = chat_completion_with_retry(
            messages,
            model=MODEL,
            temperature=TEMPERATURE,
            max_retries=5,
            base_delay=2.0,
        )

    # ---------- guardar DOCX ----------
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        path = REPORTS_DIR / f"Informe_Indicador_{num}_{stamp}.docx"
        helpers.save_report_to_docx(report_text, path)
        generated.append(path)

        print(f"✅ Indicador {num}: informe listo → {path.name}")
        done += 1

        if callable(progress_update):
            pct = done / total
            progress_update(pct, f"Indicador {num} listo ({done}/{total})")

    return generated

    # stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # filename = f"Informe_Indicador_{num}_{stamp}.docx"
    # path     = os.path.join(REPORTS_DIR, filename)
    # helpers.save_report_to_docx(report_text, path)

    # print(f"✅  Indicador {num}: informe listo → {path}")


if __name__ == "__main__":
    import sys
    import openai
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if len(sys.argv) != 2:
        sys.exit("Uso: python run_all_indicadores.py ruta/encuesta.xlsx")
    generate_reports(sys.argv[1])
