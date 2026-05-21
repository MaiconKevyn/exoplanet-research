from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
LITERATURE_DIR = DATA_DIR / "literature"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"
FRONTEND_DATA_DIR = PROJECT_ROOT / "frontend" / "src" / "data"

