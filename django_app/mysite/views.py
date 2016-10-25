from django.shortcuts import render


def error(request):
    error_message = request.POST.get('error_message')
    context = {
        'error_message': error_message
    }
    return render(request, 'common/error.html', context)
