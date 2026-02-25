import pandas as pd
from pathlib import Path
import logging

from app.config import ARQUIVO_ESTATISTICAS, PROCESSED_DATA_DIR, NA_VALUES


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProcessadorDados2:
    """Classe para processar dados do arquivo Excel"""

    def __init__(self, path_file: Path = ARQUIVO_ESTATISTICAS):
        self.path_file = path_file
        self.df = None
        self.estatisticas = {}

    def carregar_dados(self, **kwargs) -> bool:
        """
        Carrega dados do arquivo Excel

        Args:
            **kwargs: Parâmetros adicionais para pd.read_excel

        Returns:
            bool: True se carregou com sucesso
        """
        try:
            if not self.path_file.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {self.path_file}")

            logger.info(f"Carregando arquivo: {self.path_file}")

            # Parâmetros padrão
            params = {
                'sheet_name': 0,
                'na_values': NA_VALUES,
                **kwargs
            }

            self.df = pd.read_excel(self.path_file, **params)

            logger.info(f"Dados carregados: {self.df.shape[0]} linhas, {self.df.shape[1]} colunas")
            #logger.info(f"Colunas: {list(self.df.columns)}")

            return True

        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return False