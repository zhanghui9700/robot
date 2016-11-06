#-*- coding=utf-8 -*-

import importlib

from django.http import JsonResponse
from django.views.generic import View


class I18N(View):

    def _load_translate(self):
        trans = []
        mod_name = "biz.i18n.translate"
        _m = importlib.import_module(mod_name)
        for sub_name in [sub for sub in _m.__all__]:
            _module = importlib.import_module("{0}.{1}".format(mod_name, sub_name))
            if _module:
                trans.append(_module)

        return trans
        

    def get(self, request, *args, **kwargs):  
        data = {}
       
        for trans in self._load_translate():
            prefix, mod = trans.__name__.rsplit('.', 1)
            i18n = getattr(trans, "get_i18n", None)
            if i18n:
                if mod == "overall":
                    data.update(i18n())
                else:
                    data.setdefault(mod, i18n()) 

        return JsonResponse(data)