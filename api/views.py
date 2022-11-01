import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .scrapers.facebook import Facebook
from .scrapers.instagram import Instagram
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
        f.auth('ricardoandresalvarez62341@outlook.com', 'Andres62341')
        f.scrape_friends()
        f.scrape_followers()
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
        i = Instagram()
        i.auth("dorkcoon", "Andres62341")
        i.scrape_followers()
        i.scrape_following()
        # i.send_messages()
        i.quit()
