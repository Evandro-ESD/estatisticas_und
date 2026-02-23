#!/usr/bin/env python3
"""
Script principal para processamento de dados estatísticos
"""

import argparse
import logging
from pathlib import Path

from app.processador import ProcessadorDados
from app.config import ARQUIVO_ESTATISTICAS

from app.services.graficos import GraficoService

logger = logging.getLogger(__name__)


def main():
    """Função principal do programa"""

    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Processa dados do arquivo Excel')
    parser.add_argument('--arquivo', type=str, help='Caminho alternativo para o arquivo Excel')
    parser.add_argument('--sheet', type=str, default=0, help='Nome ou índice da planilha')
    parser.add_argument('--salvar', action='store_true', help='Salvar dados processados')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')

    args = parser.parse_args()

    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Definir arquivo a ser processado
    arquivo = Path(args.arquivo) if args.arquivo else ARQUIVO_ESTATISTICAS

    # Inicializar processador
    processador = ProcessadorDados(arquivo)

    # Carregar dados
    if not processador.carregar_dados(sheet_name=args.sheet):
        logger.error("Falha ao carregar dados. Encerrando.")
        return 1

    '''
    # Limpar dados
    processador.limpar_dados()

    # Calcular estatísticas
    stats = processador.calcular_estatisticas()

    # Mostrar resumo
    print(processador.resumo_dados())

    # Salvar se solicitado
    if args.salvar:
        caminho_salvo = processador.salvar_dados_processados()
        print(f"\n✅ Dados salvos em: {caminho_salvo}")
    
    '''

    ##

    print(processador.total_presos_por_guarnicao())

    df = processador.agregar_por_coluna(
        coluna_valor="PRESOS/APREENDIDOS",
        colunas_grupo=["TIPO DE SERVIÇO", "MÊS"],
        operacao="sum"
    )

    df = processador.agregar_por_coluna(
        coluna_valor="VEÍCULOS RECUPERADOS",
        colunas_grupo=["MÊS"],
        operacao="mean"
    )

    df = processador.agregar_por_coluna(
        coluna_valor="PRESOS/APREENDIDOS",
        colunas_grupo=["TIPO DE SERVIÇO"],
        operacao="count",
        remover_zeros=False
    )

    grafico_service = GraficoService()

    categorias, data_series, series_labels = \
        processador.preparar_dados_barras_por_mes(
            coluna_valor="PRESOS/APREENDIDOS"
        )

    grouped_bar_chart(
        categories=categorias,
        data_series=data_series,
        series_labels=series_labels,
        title="Presos/Apreendidos por Mês e Serviço",
        ylabel="Quantidade"
    )



    '''
           # VEÍCULOS RECUPERADOS
    '''
    df_agrupado_presos = processador.agregar_por_coluna(
        coluna_valor="PRESOS/APREENDIDOS",
        colunas_grupo=["TIPO DE SERVIÇO", 'MÊS'],
        operacao="sum"
    )

    grafico_service.gerar(
        df=df_agrupado_presos,
        coluna_x="TIPO DE SERVIÇO",
        coluna_y="PRESOS/APREENDIDOS",
        titulo="Total de Presos por Tipo de Serviço"
    )

    '''
        # VEÍCULOS RECUPERADOS
    '''
    df_agrupado_veiculos = processador.agregar_por_coluna(
        coluna_valor="VEÍCULOS RECUPERADOS",
        colunas_grupo=["TIPO DE SERVIÇO", 'MÊS'],
        operacao="sum"
    )

    grafico_service.gerar(
        df=df_agrupado_veiculos,
        coluna_x="TIPO DE SERVIÇO",
        coluna_y="VEÍCULOS RECUPERADOS",
        titulo="Total de veículos recuperados por Tipo de Serviço"
    )
    

    ##

    return 0


if __name__ == "__main__":
    exit(main())