# -*- coding: utf-8 -*-

from django.db import connection


class GetSubsidy(object):
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
        #cursor.execute(
        #    "SELECT * FROM subsidy WHERE pref_name = '" + pref_name + "' AND city = '" + city_name + "'")
        cursor.execute(
            "SELECT subsidy::int, content, url FROM subsidy WHERE pref_name = '" + pref_name + "' LIMIT " + str(num) + "")
        return list(self.dictfetchall(cursor))
