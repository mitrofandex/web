from django.http import HttpResponse


def test(request, *args, **kwargs):
    return HttpResponse('200 OK\n' + '\n'.join(request.META['QUERY_STRING'].split('&')), content_type='text/plain')
