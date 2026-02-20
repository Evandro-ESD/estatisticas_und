import matplotlib.pyplot as plt
import logging
from pathlib import Path

from app.config import GRAFICOS_DIR

logger = logging.getLogger(__name__)


class GraficoService:
    """
    Serviço responsável por geração de gráficos.
    """

    def __init__(self):
        self.output_dir = GRAFICOS_DIR / "graficos"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gerar(
        self,
        df,
        coluna_x: str,
        coluna_y: str,
        titulo: str,
        tipo: str = "bar",
        ordenar: bool = True,
        salvar: bool = True,
        nome_arquivo: str = None
    ) -> Path | None:

        if df.empty:
            raise ValueError("DataFrame vazio para geração de gráfico")

        if ordenar:
            df = df.sort_values(coluna_y, ascending=False)

        plt.figure(figsize=(10, 6))

        if tipo == "bar":
            plt.bar(df[coluna_x].astype(str), df[coluna_y])
        elif tipo == "line":
            plt.plot(df[coluna_x], df[coluna_y])
        else:
            raise ValueError("Tipo de gráfico inválido")

        plt.title(titulo)
        plt.xlabel(coluna_x)
        plt.ylabel(coluna_y)
        plt.xticks(rotation=45)
        plt.tight_layout()

        caminho = None

        if salvar:
            if not nome_arquivo:
                nome_arquivo = titulo.lower().replace(" ", "_")

            caminho = self.output_dir / f"{nome_arquivo}.png"
            plt.savefig(caminho)
            logger.info(f"Gráfico salvo em {caminho}")

        plt.show()

        return caminho