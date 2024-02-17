from django.utils.decorators import method_decorator


def class_view_decorator(function_decorator):
    def decorator(view_object):
        view_object.dispatch = method_decorator(function_decorator)(view_object.dispatch)
        return view_object

    return decorator
