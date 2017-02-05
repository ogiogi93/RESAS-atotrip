# -*- coding: utf-8 -*-
import pandas as pd
import requests
import re
from config import key


class GetNHKMovie(object):

    NHK_API_URL = 'http://ld2016.nhk.jp/sparql'

    def remove_ken(self, pref_name):
        """
        県、府を除く
        :param pref_name:
        :return:
        """
        return re.sub('府|県', '', pref_name)

    def get_movie(self, ocupation=None, pref_name=None, num=None):
        pref_name = self.remove_ken(pref_name=pref_name)
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX nhkld: <http://ld2016.nhk.jp/nhkld/>
            PREFIX nhkld-area: <http://ld2016.nhk.jp/nhkld/area/>
            PREFIX nhkld-service: <http://ld2016.nhk.jp/nhkld/service/>
            PREFIX nhkld-genre: <http://ld2016.nhk.jp/nhkld/genre/>
            SELECT ?title ?contentUrl ?description
            WHERE
            {
                ?clip  rdf:type nhkld:ChiikiClip.
                ?clip  nhkld:title ?title.
                ?clip  nhkld:contentUrl ?contentUrl.
                ?clip  nhkld:prefecture ?prefecture.
                FILTER REGEX (?prefecture, '"""+pref_name+"""').
                ?clip  nhkld:description ?description .
            }
            """
        parameter = {
            'query': query,
            'key': key.nhk_api
        }
        nhk_movies = requests.get(self.NHK_API_URL, params=parameter).json()['results']['bindings']

        templist_title = []
        templist_url = []

        for nhk_movie in nhk_movies:
            templist_title.append(nhk_movie['title'])
            templist_url.append(nhk_movie['contentUrl'])
        df_title = pd.DataFrame(templist_title)
        df_url = pd.DataFrame(templist_url)

        # Dataが返ってこない場合抜ける
        if df_title.shape[0] == 0:
            return None

        # DataFrameをmergeし整形する
        df_title['index'] = df_title.index
        df_title = df_title[['index', 'value']]
        df_title.columns = ['index', 'title']
        df_url['index'] = df_url.index
        df_url = df_url[['index', 'value']]
        df_url.columns = ['index', 'url']

        df_nhk_movie = pd.merge(df_title, df_url, on=['index'])
        # データ数をnum行に絞る
        df_nhk_movie = df_nhk_movie.ix[0:num] if df_nhk_movie.shape[0] >= 5 else df_nhk_movie
        # DataFrameからtemplateで使用できるようにdictに変換する
        nhk_movie_list = []
        for index in df_nhk_movie.index:
            nhk_movie_dict = {}
            nhk_movie_dict['title'] = df_nhk_movie['title'].ix[index]
            nhk_movie_dict['url'] = df_nhk_movie['url'].ix[index]
            nhk_movie_list.append(nhk_movie_dict)

        return nhk_movie_list

