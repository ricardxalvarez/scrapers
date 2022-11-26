import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .scrapers.facebook import Facebook
from .scrapers.instagram import Instagram
from .scrapers.tiktok import Tiktok
# Create your views here.


class FacebookScraper(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request):
    #     return JsonResponse({"status": True, "content": "backend working!!"})

    def post(self, request):
        jd = json.loads(request.body)
        print(jd)
        f = Facebook()
        try:
            jd["email"]
            jd["password"]
        except KeyError:
            return JsonResponse({"status": False, "content": 'Make sure of sending email and password'})
        f.auth(jd["email"], jd["password"])
        try:
            if (jd["is_friends_checked"] == True):
                f.scrape_friends()
        except KeyError:
            pass
        try:
            if (jd["is_followers_checked"] == True):
                f.scrape_followers()
        except KeyError:
            pass
        try:
            if (jd["is_specific_checked"] == True):
                f.add_users_to_set(jd["specific_users"])
        except KeyError:
            pass
        f.send_messages()
        f.quit()
        return JsonResponse({"status": True, "content": "backend working!!"})


class InstagramScraper(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        print(jd)
        try:
            jd["username"]
            jd["password"]
        except KeyError:
            return JsonResponse({"status": False, "content": 'Make sure of sending email and password'})
        i = Instagram()
        i.auth(jd["username"], jd["password"])
        try:
            if (jd["is_followers_checked"] == True):
                i.scrape_followers()
        except KeyError:
            pass
        try:
            if (jd["is_following_checked"] == True):
                i.scrape_following()
        except KeyError:
            pass
        try:
            if (jd["is_specific_checked"] == True):
                i.add_users_to_set(jd["specific_users"])
        except KeyError:
            pass
        i.send_messages()
        i.quit()
        return JsonResponse({"status": True, "content": "backend working!!"})


class TiktokScraper(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        print(jd)
        try:
            jd["username"]
            jd["password"]
        except KeyError:
            return JsonResponse({"status": False, "content": 'Make sure of sending username and password keys'})
        t = Tiktok()
        t.auth("ricardoandresalvarez62341@outlook.com", "Andres62341$")
        t.scrape_following()
        t.send_messages()
        # t.quit()
        return JsonResponse({"status": True, "content": "backend working!!"})
