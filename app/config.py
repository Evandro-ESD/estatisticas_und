from pathlib import Path

# ===============================
# ROOT DO PROJETO
# ===============================
BASE_DIR = Path(__file__).resolve().parents[1]  # app/
PROJECT_ROOT = BASE_DIR.parent                 # DADOS/

# ===============================
# DIRETÓRIOS
# ===============================
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
GRAFICOS_DIR = OUTPUTS_DIR / "graficos"
RELATORIOS_DIR = OUTPUTS_DIR / "relatorios"

# ===============================
# ARQUIVOS
# ===============================
ARQUIVO_ESTATISTICAS = RAW_DATA_DIR / "estatistiscas_upp.xlsx"

# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================
ENCODING = "utf-8"
SHEET_NAME = 0
NA_VALUES = ["NA", "N/A", "Missing", ""]

# ===============================
# GARANTIR CRIAÇÃO DE PASTAS
# ===============================
for path in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OUTPUTS_DIR,
    GRAFICOS_DIR,
    RELATORIOS_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)