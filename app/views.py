from django.http import HttpResponse
from levels_app.models import TaskTemplate


def home(request):
    ts = TaskTemplate.objects.get(name='chest_1000')
    print(ts.rewards)
    return HttpResponse("home")
