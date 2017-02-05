# -*- coding: utf-8 -*-
from django.shortcuts import render
from main.get_resas_data import GetResas
from main.nhk import GetNHKMovie
from main.get_subsidy import GetSubsidy


def top_page(request):
    """
    トップページ
    :param request:
    :return:
    """
    return render(request, "main/index.html")


def detail_page(request):
    """
    詳細ページを表示する
    :param request:
    :return:
    """
    pref_code = request.GET.get('pref_code')
    pref_name = request.GET.get('pref_name')
    city_code = request.GET.get('city_code')
    city_name = request.GET.get('city_name')
    local_events, local_event_count = GetResas().get_local_event(city_code=city_code, num=4)
    # population = {}
    population = GetResas().get_predict_population(pref_code=pref_code, pref_name=pref_name, city_code=city_code,
                                                   city_name=city_name)
    nhk_movies = GetNHKMovie().get_movie(pref_name=pref_name, num=2)
    subsidies = GetSubsidy().get_subisidy(pref_name=pref_name, city_name=city_name, num=5)

    context = {
        'population': population,
        'nhk_movies': nhk_movies,
        'pref_name': pref_name,
        'city_name': city_name,
        'local_events': local_events,
        'local_event_count': local_event_count,
        'subisdies': subsidies,
    }
    return render(request, 'main/detail.html', context)
