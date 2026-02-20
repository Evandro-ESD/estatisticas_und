import pytest
import pandas as pd
from pathlib import Path
import tempfile

from app.processador import ProcessadorDados


@pytest.fixture
def dados_teste():
    """Cria dados de teste"""
    return pd.DataFrame({
        'Nome': ['João', 'Maria', 'José'],
        'Idade': [25, 30, 35],
        'Cidade': ['SP', 'RJ', 'BH']
    })


@pytest.fixture
def arquivo_teste(dados_teste):
    """Cria arquivo Excel temporário para teste"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        dados_teste.to_excel(tmp.name, index=False)
        yield Path(tmp.name)
    Path(tmp.name).unlink()


def test_carregar_dados(arquivo_teste):
    """Testa carregamento de dados"""
    processador = ProcessadorDados(arquivo_teste)
    assert processador.carregar_dados() == True
    assert processador.df is not None
    assert len(processador.df) == 3


def test_limpar_dados(arquivo_teste):
    """Testa limpeza de dados"""
    processador = ProcessadorDados(arquivo_teste)
    processador.carregar_dados()
    processador.limpar_dados()
    assert processador.df is not None


def test_calcular_estatisticas(arquivo_teste):
    """Testa cálculo de estatísticas"""
    processador = ProcessadorDados(arquivo_teste)
    processador.carregar_dados()
    stats = processador.calcular_estatisticas()

    assert 'total_linhas' in stats
    assert stats['total_linhas'] == 3
    assert 'colunas' in stats
    assert len(stats['colunas']) == 3