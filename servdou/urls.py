from django.conf.urls import url
import servdou.jumpers as api

urlpatterns = [
    url(r'add_idiom$', api.add_idiom, ),
    url(r'show_idioms$', api.show_idiom, ),
    url(r'get_last_idiom$', api.show_last_idiom, ),
    url(r'get_idiom$', api.get_idiom, ),
    url(r'get_idioms$', api.get_idioms, ),
    url(r'del_idiom$', api.del_idiom, ),
    url(r'edi_idiom$', api.edi_idiom, ),
    url(r'download_ido', api.download_ido, ),
    url(r'get_upl', api.get_upl_add, ),
    url(r'czuey', api.upl_handler, ),
    url(r'mov_idiom', api.mov_idiom, ),
]
