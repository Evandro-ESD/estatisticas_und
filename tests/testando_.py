import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from app.config import ARQUIVO_ESTATISTICAS
from app.processador import ProcessadorDados
from pathlib import Path

from app.services.graficos import GraficoService


# Definir arquivo a ser processado
arquivo = Path(ARQUIVO_ESTATISTICAS)

#
df = pd.read_excel(arquivo)
categories = ['GTPP I (OPERAÇÕES)', 'GTPP II (SERRA)']
DATA = df['TIPO DE SERVIÇO']
#DATA_MESES = list(set(df["MÊS"]))
DATA_MESES = tuple(set(df["MÊS"]))


guarni = ["GTPP I A", "GTPP I B", "GTPP I C", "GTPP I D"]

FILTRO = [item for item in guarni if item in list(DATA)]
#print(FILTRO)

print(10*"-")
print(DATA_MESES)
print(10*"-")

