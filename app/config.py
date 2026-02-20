from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

OUTPUTS_DIR = BASE_DIR / 'outputs'
GRAFICOS_DIR = OUTPUTS_DIR / "graficos"
RELATORIOS_DIR = OUTPUTS_DIR / "relatorios"


ARQUIVO_ESTATISTICAS = RAW_DATA_DIR / 'estatistiscas_upp.xlsx'

ENCODING = 'utf-8'
SHEET_NAME = 0
NA_VALUES = ['NA', 'N/A', 'Missing', '']

for dir_path in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OUTPUTS_DIR,
    GRAFICOS_DIR,
    RELATORIOS_DIR
]:
    dir_path.mkdir(parents=True, exist_ok=True)