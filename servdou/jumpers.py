import json
import random
import traceback

from django.core import serializers
from django.http import JsonResponse, FileResponse
from django.middleware.csrf import get_token
from django.template.context_processors import csrf

from django.views.decorators.http import require_http_methods

from servdou.models import Chengyu


@require_http_methods(["POST"])
def add_idiom(request):
    response = {}
    try:
        idiom = Chengyu.objects.filter(word=request.POST.get('word'))
        if idiom.count() > 0:
            idiom = idiom[0]
            idiom.pos+=1
            print(request.POST.get('word'), 'already existed')
            if request.POST.get('meaning') is None or request.POST.get('meaning') == '':
                idiom.save()
                response['msg'] = 'no meaning'
                response['error_num'] = 1
                return JsonResponse(response)
            elif idiom.meaning == request.POST.get('meaning'):
                idiom.save()
                response['msg'] = 'meaning the same'
                response['error_num'] = 2
                return JsonResponse(response)
            else:
                idiom.meaning = request.POST.get('meaning')
                idiom.save()
                response['msg'] = 'updated'
                response['error_num'] = 3
                return JsonResponse(response)
        else:
            idiom = Chengyu(
                word=request.POST.get('word'),
                meaning=request.POST.get('meaning')
            )
            idiom.save()
            response['msg'] = 'success'
            response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_idiom(request):
    response = {}
    # cnt = request.GET.get('count')
    # prev = request.GET.get('prev')
    # print('Getting idioms, cnt:', cnt, ', prev:', prev)
    # if cnt is not None:
    #     try:
    #         cnt = int(cnt)
    #     except:
    #         cnt = 10
    # else:
    #     cnt = 10
    # if prev is not None:
    #     try:
    #         prev = int(prev)
    #     except:
    #         prev = 0
    # else:
    #     prev = 0
    try:
        idiom = Chengyu.objects.all().order_by('-pos')
        # idiom = Chengyu.objects.all()[prev:prev+cnt]
        # print(idiom[0].id)
        response['list'] = json.loads(serializers.serialize("json", idiom))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def download_ido(request):
    print('Download idioms!')
    try:
        idiom = Chengyu.objects.all()
        iods = [{'pk': ido.id, 'idiom': ido.word, 'mean': ido.meaning} for ido in idiom]
        # for ido in idiom:
        #     iods[ido.id] =
        with open('ido.json', 'w')as jf:
            json.dump(iods, jf)
        jf = open('ido.json', 'rb')
        response = FileResponse(jf)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="idioums.json"'
        return response
    except Exception as e:
        response = {'msg': str(e), 'error_num': 1}
        return JsonResponse(response)


@require_http_methods(["GET"])
def show_last_idiom(request):
    response = {}
    try:
        idiom = Chengyu.objects.last()
        # print(idiom)
        response['idiom'] = {'pk': idiom.id, 'fields': {'word': idiom.word, 'meaning': idiom.meaning}, }
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_idiom(request):
    response = {}
    word = request.GET.get('word')
    assert isinstance(word,str)
    word=word.strip()
    print('Searching', word)
    try:
        idiom = Chengyu.objects.filter(word=word)
        print(idiom.count())
        for ido in idiom:
            print(ido.word, ido.meaning)
        if idiom.count() == 0:
            response['msg'] = 'no such idiom'
            response['error_num'] = 1
            return JsonResponse(response)
        response['idiom'] = {'pk': idiom[0].id, 'fields': {'word': idiom[0].word, 'meaning': idiom[0].meaning}, }
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def del_idiom(request):
    response = {}
    wordid = request.POST.get('iid')
    print('Searching', wordid)
    try:
        idiom = Chengyu.objects.get(id=wordid)
        print(idiom.word)
        if idiom is None:
            response['msg'] = 'no such idiom'
            response['error_num'] = 1
            return JsonResponse(response)
        idiom.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def edi_idiom(request):
    response = {}
    wordid = request.POST.get('iid')
    print('Searching', wordid, 'for edit')
    try:
        idiom = Chengyu.objects.get(id=wordid)
        print(idiom.word)
        if idiom is None:
            response['msg'] = 'no such idiom'
            response['error_num'] = 1
            return JsonResponse(response)
        if request.POST.get('meaning') is None or request.POST.get('meaning') == '':
            response['msg'] = 'no meaning'
            response['error_num'] = 2
            return JsonResponse(response)
        elif idiom.meaning == request.POST.get('meaning'):
            response['msg'] = 'meaning the same'
            response['error_num'] = 3
            return JsonResponse(response)
        else:
            idiom.meaning = request.POST.get('meaning')
            idiom.save()
            response['msg'] = 'updated'
            response['error_num'] = 0
            return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 4
    return JsonResponse(response)


@require_http_methods(["POST"])
def mov_idiom(request):
    response = {}
    # print(request.POST)
    # print(request.FILES)
    # print(request.body)
    form_json = request.body.decode()
    dt = json.loads(form_json)
    wordid = dt['iid']
    print('mov_idiom: Searching', wordid, 'for mov')
    try:
        idiom = Chengyu.objects.get(id=wordid)
        print(idiom.word)
        if idiom is None:
            response['msg'] = 'no such idiom'
            response['error_num'] = 1
            return JsonResponse(response)
        else:
            if dt['addp']:
                idiom.pos += 1
            else:
                idiom.pos -= 1
            idiom.save()
            print('mov_idiom: idiom', idiom.word, 'pos =', idiom.pos)
            response['msg'] = 'updated'
            response['error_num'] = 0
            return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 4
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_upl_add(request):
    response = {}
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    print('Attempt to access upload from', ip, end='. ')
    try:
        if request.GET.get('pid') == '5723':
            csrfTk = str(csrf(request)['csrf_token'])[5:-5]
            csrfTk = [c for c in csrfTk]
            random.shuffle(csrfTk)
            csrfTk = ''.join(csrfTk)
            # print(csrfTk)
            # print(csrfTk['csrf_token'])
            # print(type(csrfTk['csrf_token']))
            # request.META["CSRF_COOKIE_USED"] = True
            # i=get_token(request)  # 或request.META["CSRF_COOKIE_USED"] = True   新加产生token
            # print(i)
            print('Validated! return true api')
            response['addr'] = 'api/czuey'
            response['csrft'] = csrfTk
            response['upl'] = True
            response['error_num'] = 0
            return JsonResponse(response)
        else:
            print('Reject, return fake api')
            response['upl'] = False
            response['addr'] = 'api/upload'
            response['error_num'] = 0
            return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['upl'] = False
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", 'POST'])
def upl_handler(request):
    # request.META["CSRF_COOKIE_USED"] = True
    # i=get_token(request)  # 或request.META["CSRF_COOKIE_USED"] = True   新加产生token
    # print(i)
    # print('upl_handler',request)
    # if request.method == 'GET':
    #     print('GET', request)
    #     request.META["CSRF_COOKIE_USED"] = True
    #     get_token(request)  # 或request.META["CSRF_COOKIE_USED"] = True   新加产生token

    response = {}
    if request.method == 'POST':
        try:
            # print('POST', request)
            data = request.FILES.get('file').read().decode()
            act = request.POST.get('act')
            print('upl_handler:', act)
            # assert isinstance(data,bytes)
            # print(data.decode())
            # print(type(data.decode()))
            idioums = json.loads(data)
            print('upl_handler: file got')
            # todo check!
            if act == 'mrg':
                add = ins = null_meaning = 0
                for ido in idioums:
                    idiom = Chengyu.objects.filter(word=ido['idiom'])
                    if idiom.count() > 0:
                        idou = idiom[0]
                        if ido['mean'] != '':
                            idou.meaning = ido['mean']
                            idou.pos+=1
                            idou.save()
                            ins += 1
                        else:
                            null_meaning += 1
                            idou.pos+=1
                            idou.save()
                    else:
                        idiom = Chengyu(
                            word=ido['idiom'],
                            meaning=ido['mean']
                        )
                        idiom.save()
                        add += 1
                response['msg'] = 'Merged'
                response['ins'] = ins
                response['add'] = add
                response['null_meaning'] = null_meaning
                response['error_num'] = 0
                print('upl_handler:', add, 'added', ins, 'inserted', null_meaning, 'no_meaning')
            elif act == 'add':
                add = existed = 0
                for ido in idioums:
                    idiom = Chengyu.objects.filter(word=ido['idiom'])
                    if idiom.count() > 0:
                        existed += 1
                        idiom[0].pos+=1
                        idiom[0].save()
                    else:
                        idiom = Chengyu(
                            word=ido['idiom'],
                            meaning=ido['mean']
                        )
                        idiom.save()
                        add += 1
                response['msg'] = 'Added'
                response['existed'] = existed
                response['add'] = add
                response['error_num'] = 0
                print('upl_handler:', add, 'added', existed, 'existed')
            elif act == 'clr':
                print('upl_handler:', 'clear database')
                idioms = Chengyu.objects.all()
                for idi in idioms:
                    idi.delete()
                for ido in idioums:
                    idiom = Chengyu(
                        word=ido['idiom'],
                        meaning=ido['mean']
                    )
                    idiom.save()
                response['msg'] = 'Cleared'
                response['ins'] = 0
                response['add'] = len(idioums)
                response['error_num'] = 0
                print('upl_handler:', len(idioums), 'idioums added')
            else:
                response['msg'] = 'Unsupported method'
                response['error_num'] = 2
        except Exception as e:
            traceback.print_exc()
            print('upl_handler: error:', e)
            response['msg'] = str(e)
            response['error_num'] = 1
    else:
        response['msg'] = 'Please POST'
        response['error_num'] = 1
    return JsonResponse(response)
