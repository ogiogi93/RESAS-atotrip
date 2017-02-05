# -*- coding: utf-8 -*-
import pandas as pd
import requests
from config import key


class GetResas(object):

    def __init__(self):
        self.header = {'X-API-KEY': key.resas_api}
        self.url = 'https://opendata.resas-portal.go.jp'

    def get_resas(self, url, parameter):
        """
        RESASからデータを取得する
        :return:
        """
        url = self.url + url
        return requests.get(url, params=parameter, headers=self.header).json()['result']


    def get_population(self, pref_code="1"):
        """
        都道府県別人口情報を取得する
        :param pref_code:
        :return:
        """
        parameter = {
            'prefCode': pref_code
        }
        url = '/api/v1/municipality/company/perYear'
        populations = self.get_resas(url=url, parameter=parameter)

        #　年ごとに値が入っているので、listに格納する
        pref_name = populations['prefName']
        population_list = []
        for population in populations['data']:
            temp = pref_name, population['year'], population['value']
            population_list.append(temp)

        # DataFrameに格納する
        df_population = pd.DataFrame(population_list, columns=['pref_name', 'year', 'value'])

        return df_population.to_json(orient='records')

    def get_predict_population(self, pref_code=None, pref_name=None, city_code=None, city_name=None):
        """
        人口増減予測を可視化する
        :param pref_code:
        :param pref_name:
        :param city_code:
        :param city_name:
        :return:
        """
        parameter = {
            'prefCode': pref_code,
            'cityCode': city_code
        }
        url = '/api/v1/population/sum/perYear'
        populations = self.get_resas(url=url, parameter=parameter)

        population_list = []
        for population in populations['line']['data']:
            temp = pref_name, city_name, population['year'], population['value']
            population_list.append(temp)

        # DataFrameに格納する
        df_population = pd.DataFrame(population_list, columns=['pref_name', 'city_name','year', 'value'])

        return df_population.to_json(orient='records')

    def get_local_event(self, city_code, num=None):
        """
        ローカルイベント情報を取得する
        :param city_code:
        :return:
        """
        parameter = {
            'cities': city_code
        }
        url = '/api/v1/partner/asutomo/event'
        df_event = pd.DataFrame(self.get_resas(url=url, parameter=parameter))

        local_event_list_count = df_event.shape[0]
        # num行に絞る
        df_event = df_event.ix[0:num] if df_event.shape[0] >= num else df_event

        # DataFrameからtemplateで使用できるようにdictに変換する
        local_event_list = []
        for index in df_event.index:
            local_event_dict = {}
            local_event_dict['event_title'] = df_event['event_title'].ix[index]
            local_event_dict['event_content'] = df_event['event_content'].ix[index]
            local_event_dict['event_period_began_on'] = df_event['event_period_began_on'].ix[index]
            local_event_dict['event_period_ended_on'] = df_event['event_period_ended_on'].ix[index]
            local_event_dict['thumb_image'] = df_event['thumb_image'].ix[index]
            local_event_dict['info_homepage'] = df_event['info_homepage'].ix[index]

            local_event_list.append(local_event_dict)

        return local_event_list, local_event_list_count
