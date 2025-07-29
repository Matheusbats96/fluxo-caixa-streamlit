import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import RECEITA_MENSAL, MESES, IMPOSTOS_PCT, CONTINGENCIA_PCT, DESPESAS

class FluxoCaixa:
    def __init__(self, receita, meses, impostos_pct, contingencia_pct, despesas):
        self.receita = receita
        self.meses = meses
        self.impostos_pct = impostos_pct
        self.contingencia_pct = contingencia_pct
        self.despesas = despesas

    def gerar_dataframe(self, inicio=datetime(2025, 8, 1)):
        datas = [inicio + relativedelta(months=i) for i in range(self.meses)]
        df = pd.DataFrame(index=datas)
        df.index.name = 'Mês'
        df['Receita'] = self.receita

        for nome, valor in self.despesas.items():
            df[nome] = valor

        cols = list(self.despesas.keys())
        df['Subtotal Custos'] = df[cols].sum(axis=1)
        df['Contingência'] = df['Subtotal Custos'] * self.contingencia_pct
        df[f'Impostos ({int(self.impostos_pct*100)}%)'] = df['Receita'] * self.impostos_pct

        totais = cols + ['Contingência', f'Impostos ({int(self.impostos_pct*100)}%)']
        df['OPEX Total'] = df[totais].sum(axis=1)
        df['Lucro Operacional'] = df['Receita'] - df['OPEX Total']

        return df

    def exportar_csv(self, df, caminho='fluxo_caixa.csv'):
        df.to_csv(caminho, index=True)

    def exportar_excel(self, df, caminho='fluxo_caixa.xlsx'):
        df.to_excel(caminho, index=True)