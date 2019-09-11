def is_allowed_origin(request):
    allowed_origin = ['https://localhost:3000',
                      'https://arcanrun.github.io/budget-manager']
    try:
        if request.META['HTTP_ORIGIN'] in allowed_origin:
            return True
        else:
            return False
    except Exception:
        return False
