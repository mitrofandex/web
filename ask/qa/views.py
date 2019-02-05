from django.http import HttpResponse


def test(request, *args, **kwargs):
    return HttpResponse('\n'.join(request.GET.urlencode().split('&')))
