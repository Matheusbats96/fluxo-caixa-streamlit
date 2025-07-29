import argparse
import pandas as pd
from fluxo_caixa import FluxoCaixa
from config import RECEITA_MENSAL, MESES, IMPOSTOS_PCT, CONTINGENCIA_PCT, DESPESAS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inicio', type=str, default='2025-08-01')
    parser.add_argument('--exportar', choices=['csv','excel','none'], default='excel')
    args = parser.parse_args()

    fluxo = FluxoCaixa(RECEITA_MENSAL, MESES, IMPOSTOS_PCT, CONTINGENCIA_PCT, DESPESAS)
    inicio = pd.to_datetime(args.inicio)
    df = fluxo.gerar_dataframe(inicio=inicio)

    if args.exportar == 'csv':
        fluxo.exportar_csv(df)
        print('Exportado para fluxo_caixa.csv')
    elif args.exportar == 'excel':
        fluxo.exportar_excel(df)
        print('Exportado para fluxo_caixa.xlsx')
    else:
        print(df)