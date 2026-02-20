#!/usr/bin/env python3
"""
Script principal para processamento de dados estatísticos
"""

import argparse
import logging
from pathlib import Path

from app.processador import ProcessadorDados
from app.config import ARQUIVO_ESTATISTICAS

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

    #print(processador.total_presos())

    print(processador.total_presos_por_guarnicao())

    return 0


if __name__ == "__main__":
    exit(main())