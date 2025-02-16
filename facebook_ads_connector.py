import os
import pandas as pd
from flask import Flask, jsonify, request
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
from datetime import datetime

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
        
        # Transformar os dados em um DataFrame
        data = []
        for campaign in campaigns:
            campaign_data = {
                'campaign_name': campaign.get('campaign_name', 'N/A'),
                'impressions': campaign.get('impressions', 0),
                'clicks': campaign.get('clicks', 0),
                'spend': campaign.get('spend', 0),
                'cpc': campaign.get('cpc', 0),
                'cpm': campaign.get('cpm', 0),
                'ctr': campaign.get('ctr', 0),
                'actions': campaign.get('actions', [])
            }
            data.append(campaign_data)
        
        return pd.DataFrame(data)
    
    except FacebookRequestError as e:
        return pd.DataFrame({'error': [str(e)]})

@app.route('/facebook_ads_data', methods=['GET'])
def facebook_ads_data():
    start_date = request.args.get('start_date', (datetime.now().strftime('%Y-%m-%d')))
    end_date = request.args.get('end_date', (datetime.now().strftime('%Y-%m-%d')))
    
    df = get_campaign_data(start_date, end_date)
    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

