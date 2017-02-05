# -*- coding: utf-8 -*-
import pandas as pd
from django.db import connection


class GetData(object):
    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def get_subisidy(self, pref_name=None, city_name=None, num=5):
        """
        助成金情報を取得する
        :param pref_name:
        :param city_name:
        :return:
        """
        cursor = connection.cursor()
        # cursor.execute(
        #    "SELECT * FROM subsidy WHERE pref_name = '" + pref_name + "' AND city = '" + city_name + "'")
        cursor.execute(
            "SELECT subsidy::int, content, url FROM subsidy WHERE pref_name = '" + pref_name + "' LIMIT " + str(
                num) + "")
        return list(self.dictfetchall(cursor))

    def get_sarary(self, pref_name=None):
        """
        都道府県ごとの平均給料を取得する
        :param pref_name:
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sarary")
        return pd.DataFrame(list(self.dictfetchall(cursor)))

    def get_main_content(self):
        """
        メインコンテンツ
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT id, main_title, main_text, main_picture, content.pref_name,pref_code, content.city_name, city_code  FROM content INNER JOIN resas_code ON content.pref_name=resas_code.pref_name and content.city_name = resas_code.city_name")
        return list(self.dictfetchall(cursor))

    def get_detail_content(self, id):
        """
        詳細コンテンツ
        :return:
        """
        id = str(id)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM content WHERE id= " + id + "")
        return list(self.dictfetchall(cursor))
