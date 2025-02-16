import os
import pandas as pd
from flask import Flask, jsonify, request
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
from datetime import datetime
from datetime import datetime, timedelta


# Configuração do Facebook Ads API
ACCESS_TOKEN = 'EAAQdoNHPnUwBO66BALlKOqwnjFeZABis1fBivE38gfFuyxJPlacnN349TVdKYc4pbjxpgMqQOKnvZByhbmZClBS0bULHkmkjc8f5iVToANSaDo67xLNUav6xHjdOZB5VIsdnZAyrBv0KicdWz1iHaVjuC9jyGf0EXVUluvzpoc9ZBVF8d50rgpicB06Geg7pLh'
AD_ACCOUNT_ID = 'act_667578474707036'
APP_ID = '1158476458859852'
APP_SECRET = '7e677de42f76fc8ca00caf6ff976e09d'

# Inicializar API do Facebook
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

app = Flask(__name__)

def get_campaign_data(start_date, end_date):
    try:
        # Acessar a conta de anúncios
        account = AdAccount(AD_ACCOUNT_ID)
        
        # Definição de parâmetros da API
        params = {
            'level': 'campaign',
            'fields': ['campaign_name', 'impressions', 'clicks', 'spend', 'cpc', 'cpm', 'ctr', 'actions'],
            'time_range': {'since': start_date, 'until': end_date}
        }
        
        # Obtendo os insights da campanha
        campaigns = account.get_insights(params=params)
        
        # Lista para armazenar os dados processados
        data = []
        
        for campaign in campaigns:
            actions_list = campaign.get('actions', [])
            
            # Criar estrutura para armazenar os diferentes tipos de ações
            action_types = {
                'resultados_cliques_no_link': 0,
                'resultados_conversas_mensagem': 0
            }
            
            # Mapear as ações específicas para colunas nomeadas corretamente
            for action in actions_list:
                action_type = action.get('action_type', '').lower()
                action_value = int(action.get('value', 0))  # Garantir conversão para int
                
                if action_type == 'link_click':
                    action_types['resultados_cliques_no_link'] = action_value
                elif action_type == 'onsite_conversion.messaging_conversation_started_7d':
                    action_types['resultados_conversas_mensagem'] = action_value
            
            # Construir objeto final de dados
            campaign_data = {
                'campaign_name': campaign.get('campaign_name', 'N/A'),
                'impressions': int(campaign.get('impressions', 0)),
                'clicks': int(campaign.get('clicks', 0)),
                'spend': float(campaign.get('spend', 0)),
                'cpc': float(campaign.get('cpc', 0)),
                'cpm': float(campaign.get('cpm', 0)),
                'ctr': float(campaign.get('ctr', 0)),
                **action_types  # Adiciona as ações processadas
            }
            
            data.append(campaign_data)
        
        return data
    
    except FacebookRequestError as e:
        return {"error": str(e)}

@app.route('/facebook_ads_data', methods=['GET'])
def facebook_ads_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Se os parâmetros de data não forem passados, definir um valor padrão (últimos 7 dias)
    if not start_date or not end_date:
        today = datetime.now()
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

    data = get_campaign_data(start_date, end_date)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)