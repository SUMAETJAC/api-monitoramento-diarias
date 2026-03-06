import pandas as pd
from flask import Flask, request, send_file
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Link do Google Sheets convertido para CSV
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1P_ucOWBHnVJ1FdwzRN7i_WiUkwFvuyyoKPAPFcu_ycE/export?format=csv&gid=0"

@app.route('/download', methods=['GET'])
def download_dados():
    try:
        # 1. Lê os dados da planilha
        df = pd.read_csv(URL_PLANILHA)
        
        # 2. Captura os filtros que virão do botão do Power BI
        ano = request.args.get('ano', 'Todos')
        mes = request.args.get('mes', 'Todos')
        comarca = request.args.get('comarca', 'Todos')
        rubrica = request.args.get('rubrica', 'Todos')
        tipo = request.args.get('tipo', 'Todos')
        unidade = request.args.get('unidade', 'Todos')
        
        # 3. Aplica os filtros nas colunas de texto exatas
        if comarca != 'Todos' and 'Comarca' in df.columns:
            df = df[df['Comarca'] == comarca]
            
        if rubrica != 'Todos' and 'Rubrica Dotação' in df.columns:
            df = df[df['Rubrica Dotação'] == rubrica]
            
        if tipo != 'Todos' and 'TipoDiaria' in df.columns:
            df = df[df['TipoDiaria'] == tipo]
            
        if unidade != 'Todos' and 'Unidade' in df.columns:
            df = df[df['Unidade'] == unidade]
            
        # 4. Tratamento Inteligente para Ano e Mês (Lendo a coluna Data Empenho)
        if (ano != 'Todos' or mes != 'Todos') and 'Data Empenho' in df.columns:
            # Converte a coluna para o formato de data do Brasil (dd/mm/yyyy)
            datas = pd.to_datetime(df['Data Empenho'], format='%d/%m/%Y', errors='coerce')
            
            if ano != 'Todos':
                df = df[datas.dt.year == int(ano)]
                # Atualiza a variável datas para o novo tamanho da tabela
                datas = pd.to_datetime(df['Data Empenho'], format='%d/%m/%Y', errors='coerce')
                
            if mes != 'Todos':
                # No Power BI o mês geralmente vai como número (1 a 12)
                df = df[datas.dt.month == int(mes)]
                
        # 5. Converte para Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Diárias')
        output.seek(0)
        
        # 6. Envia o arquivo para download
        return send_file(
            output, 
            download_name="Relatorio_Diarias_Filtrado.xlsx", 
            as_attachment=True, 
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        return f"Ocorreu um erro ao processar os dados: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)