import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from app.config import ARQUIVO_ESTATISTICAS, PROCESSED_DATA_DIR, NA_VALUES

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProcessadorDados:
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

    def limpar_dados(self) -> None:
        """Limpa e prepara os dados"""
        if self.df is None:
            raise ValueError("Dados não carregados. Execute carregar_dados() primeiro.")

        logger.info("Iniciando limpeza dos dados...")

        # Remover linhas totalmente vazias
        self.df.dropna(how='all', inplace=True)

        # Remover colunas totalmente vazias
        self.df.dropna(axis=1, how='all', inplace=True)

        # Padronizar nomes de colunas
        # retirado pq comentei a função _padronizar_nome_coluna
        # #self.df.columns = [self._padronizar_nome_coluna(col) for col in self.df.columns]
        self.df.columns = [col for col in self.df.columns]

        # Remover duplicatas
        self.df.drop_duplicates(inplace=True)

        logger.info(f"Limpeza concluída: {self.df.shape[0]} linhas restantes")

    '''
    
    def _padronizar_nome_coluna(self, nome: str) -> str:
        """Padroniza nomes de colunas"""
        if not isinstance(nome, str):
            return f"coluna_{nome}"

        return (nome.lower()
                .strip()
                .replace(' ', '_')
                .replace('ç', 'c')
                .replace('ã', 'a')
                .replace('õ', 'o')
                .replace('á', 'a')
                .replace('é', 'e')
                .replace('í', 'i')
                .replace('ó', 'o')
                .replace('ú', 'u'))
    '''

    def calcular_estatisticas(self) -> Dict[str, Any]:
        """Calcula estatísticas básicas dos dados"""
        if self.df is None:
            raise ValueError("Dados não carregados")

        logger.info("Calculando estatísticas...")

        self.estatisticas = {
            'total_linhas': len(self.df),
            'total_colunas': len(self.df.columns),
            'colunas': list(self.df.columns),
            'tipos_dados': self.df.dtypes.to_dict(),
            'valores_ausentes': self.df.isnull().sum().to_dict(),
            'percentual_ausentes': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'memoria_uso': self.df.memory_usage(deep=True).sum() / 1024 ** 2  # MB
        }

        # Estatísticas para colunas numéricas
        colunas_numericas = self.df.select_dtypes(include=['number']).columns
        if len(colunas_numericas) > 0:
            self.estatisticas['estatisticas_numericas'] = self.df[colunas_numericas].describe().to_dict()

        return self.estatisticas

    def salvar_dados_processados(self, nome_arquivo: Optional[str] = None) -> Path:
        """Salva dados processados em diferentes formatos"""
        if self.df is None:
            raise ValueError("Dados não carregados")

        if nome_arquivo is None:
            nome_arquivo = f"dados_processados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"

        # Salvar como CSV
        csv_path = PROCESSED_DATA_DIR / f"{nome_arquivo}.csv"
        self.df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        logger.info(f"Dados salvos em: {csv_path}")

        # Salvar como Excel
        excel_path = PROCESSED_DATA_DIR / f"{nome_arquivo}.xlsx"
        self.df.to_excel(excel_path, index=False)
        logger.info(f"Dados salvos em: {excel_path}")

        return csv_path

    def resumo_dados(self) -> str:
        """Gera um resumo dos dados"""
        if not self.estatisticas:
            self.calcular_estatisticas()

        resumo = f"""
{'=' * 50}
📊 RESUMO DOS DADOS
{'=' * 50}

📈 DIMENSÕES:
  • Linhas: {self.estatisticas['total_linhas']:,}
  • Colunas: {self.estatisticas['total_colunas']}

📋 COLUNAS:
  {', '.join(self.estatisticas['colunas'])}

💾 MEMÓRIA:
  • Uso: {self.estatisticas['memoria_uso']:.2f} MB

🔍 VALORES AUSENTES:
"""

        for col, total in self.estatisticas['valores_ausentes'].items():
            if total > 0:
                percentual = self.estatisticas['percentual_ausentes'][col]
                resumo += f"  • {col}: {total} ({percentual:.1f}%)\n"

        return resumo

    def total_veiculos_recuperados(self):

        logger.info("VEÍCULOS RECUPERADOS ")

        res = self.df.loc[(self.df['VEÍCULOS RECUPERADOS'].notna()) & (self.df['VEÍCULOS RECUPERADOS'] != 0),'VEÍCULOS RECUPERADOS']
        return res

    def total_presos_por_guarnicao(self):

        if self.df is None:
            raise ValueError("Execute carregar_dados() antes de processar.")

        df = self.df.copy()

        df['PRESOS/APREENDIDOS'] = pd.to_numeric(
            df['PRESOS/APREENDIDOS'],
            errors='coerce'
        )

        df_filtrado = df[
            (df['PRESOS/APREENDIDOS'].notna()) &
            (df['PRESOS/APREENDIDOS'] != 0)
            ]

        resultado = (
            df_filtrado
            .groupby(['TIPO DE SERVIÇO', 'MÊS'])['PRESOS/APREENDIDOS']
            .sum()
            .reset_index()
        )

        return resultado
    #####################

    def agregar_por_coluna(
            self,
            coluna_valor: str,
            colunas_grupo: list,
            operacao: str = "sum",
            remover_zeros: bool = True,
            remover_nulos: bool = True
    ) -> pd.DataFrame:
        """
        Agrega uma coluna numérica por grupos definidos.

        Args:
            coluna_valor (str): Nome da coluna numérica a ser agregada
            colunas_grupo (list): Lista de colunas para agrupamento
            operacao (str): Operação de agregação ('sum', 'mean', 'count', 'max', 'min')
            remover_zeros (bool): Remove valores zerados antes da agregação
            remover_nulos (bool): Remove valores nulos antes da agregação

        Returns:
            pd.DataFrame: DataFrame agregado
        """

        if self.df is None:
            raise ValueError("Dados não carregados")

        if coluna_valor not in self.df.columns:
            raise ValueError(f"Coluna '{coluna_valor}' não encontrada")

        # Garantir tipo numérico
        df_filtrado = self.df.copy()

        df_filtrado[coluna_valor] = pd.to_numeric(
            df_filtrado[coluna_valor],
            errors="coerce"
        )

        df_filtrado = self.df.copy()

        if remover_nulos:
            df_filtrado = df_filtrado[df_filtrado[coluna_valor].notna()]

        if remover_zeros:
            df_filtrado = df_filtrado[df_filtrado[coluna_valor] != 0]

        if operacao not in ["sum", "mean", "count", "max", "min"]:
            raise ValueError("Operação inválida")

        resultado = (
            df_filtrado
            .groupby(colunas_grupo)[coluna_valor]
            .agg(operacao)
            .reset_index()
        )

        return resultado


    ###  ###########################
    def preparar_dados_barras_por_mes(self, coluna_valor: str):

        if self.df is None:
            raise ValueError("Dados não carregados")

        ORDEM_MESES = [
            "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL",
            "MAIO", "JUNHO", "JULHO", "AGOSTO",
            "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
        ]

        agregado = self.agregar_por_coluna(
            coluna_valor=coluna_valor,
            colunas_grupo=["MÊS", "TIPO DE SERVIÇO"],
            operacao="sum",
            remover_zeros=False
        )

        agregado["MÊS"] = agregado["MÊS"].str.strip().str.upper()

        pivot = (
            agregado
            .pivot(index="MÊS", columns="TIPO DE SERVIÇO", values=coluna_valor)
            .fillna(0)
        )

        pivot = pivot.reindex(
            [m for m in ORDEM_MESES if m in pivot.index]
        )

        return (
            list(pivot.index),
            list(pivot.columns),
            [pivot[col].tolist() for col in pivot.columns]
        )





