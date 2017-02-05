# -*- coding: utf-8 -*-
import pandas as pd
from django.shortcuts import render
from main.get_resas_data import GetResas
from main.nhk import GetNHKMovie
from main.get_data import GetData

PREF_CODES = ['13', '14']


def fix_text(text):
    return text.strip()


def top_page(request):
    """
    トップページ
    :param request:
    :return:
    """
    contents = GetData().get_main_content()
    print(contents)
    context = {
        'contents': contents
    }
    return render(request, "main/index.html", context)


def detail_page(request):
    """
    詳細ページを表示する
    :param request:
    :return:
    """
    id = request.GET.get('id')
    pref_code = request.GET.get('pref_code')
    pref_name = request.GET.get('pref_name')
    city_code = request.GET.get('city_code')
    city_name = request.GET.get('city_name')
    local_events, local_event_count = GetResas().get_local_event(city_code=city_code, num=4)
    # population = {}
    # 指定された地域の情報を取得する
    df_population = GetResas().get_predict_population(pref_code=pref_code, pref_name=pref_name, city_code=city_code,
                                                      city_name=city_name)
    # 都会情報も含める
    for pref_code in PREF_CODES:
        pref_name2 = '東京都' if pref_code == '13' else '神奈川'
        temp = GetResas().get_predict_population(pref_code=pref_code, pref_name=pref_name2)
        df_population = pd.concat([df_population, temp], axis=0)

    # 平均給料情報を取得する　
    df_sarary = GetData().get_sarary(pref_name=None)

    # merge用にtextを修正する
    df_population['pref_name'] = df_population['pref_name'].apply(fix_text)
    df_sarary['pref_name'] = df_sarary['pref_name'].apply(fix_text)
    df_population2 = df_population.reset_index(drop=True)

    result = pd.merge(df_sarary, df_population2, on='pref_name', how='right')
    result = result.to_json(orient='records')

    nhk_movies = GetNHKMovie().get_movie(pref_name=pref_name, num=2)
    subsidies = GetData().get_subisidy(pref_name=pref_name, city_name=city_name, num=5)
    content = GetData().get_detail_content(id=id)[0]

    context = {
        'result': result,
        'nhk_movies': nhk_movies,
        'pref_name': pref_name,
        'city_name': city_name,
        'local_events': local_events,
        'local_event_count': local_event_count,
        'subisdies': subsidies,
        'content': content
    }
    return render(request, 'main/detail.html', context)
