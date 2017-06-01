from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from .paybox import Transaction


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'paybox/posts_list.html', {'posts': posts})


def manage_response(request):
    # Your order object
    order = get_object_or_404(Post, reference=request.GET.get('RE'))

    transaction = Transaction()
    notification = transaction.verify_notification(response_url=request.get_full_path(), order_total=order.total_incl_tax)

    order.payment = notification['success']	  	 # Boolean
    order.payment_status = notification['status']   	 # Paybox Status Message
    order.payment_auth_code = notification['auth_code'] # Authorization Code returned by Payment Center
    order.save()

    # Paybox Requires a blank 200 response
    return HttpResponse('')


def error_response(request):
    import ipdb; ipdb.set_trace()
    # Your order object
    order = get_object_or_404(Post, reference=request.GET.get('RE'))

    transaction = Transaction()
    notification = transaction.verify_notification(response_url=request.get_full_path(), order_total=order.total)

    order.payment = notification['success']	  	 # Boolean
    order.payment_status = notification['status']   	 # Paybox Status Message
    order.payment_auth_code = notification['auth_code'] # Authorization Code returned by Payment Center
    order.save()

    # Paybox Requires a blank 200 response
    return HttpResponse('')


def make_payment(request, order_reference):
    # Your order object
    order = get_object_or_404(Post, reference=order_reference)
    amount = int(order.total_incl_tax) * 100
    transaction = Transaction(
        production=False,
        PBX_TOTAL=amount,
        PBX_PORTEUR='dev.alejandrovillamarin@gmail.com',
        PBX_TIME=order.created_date,
        PBX_CMD=str(order.reference))

    form_values = transaction.post_to_paybox()

    return render(request, 'paybox/payment.html', {
        'action': form_values['action'],
        'mandatory': form_values['mandatory'],
        'accessory': form_values['accessory'],
    })
    # return render(request, 'paybox/make_payment.html', {})