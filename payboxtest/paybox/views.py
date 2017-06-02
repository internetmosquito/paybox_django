from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from .paybox import Transaction


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'paybox/posts_list.html', {'posts': posts})


def manage_response(request):
    # Your order object
    order = get_object_or_404(Post, reference=request.GET.get('RE'))
    transaction = Transaction()
    notification = transaction.verify_notification(response_url=request.get_full_path(),
                                                   order_total=order.total_incl_tax)
    status = notification['status']   	 # Paybox Status Message
    if status == 'Success':
        order.status = 'PAID'
    order.save()
    # Paybox Requires a blank 200 response
    return HttpResponse('')


def error_response(request):
    status_code = request.GET.get('RC')
    transaction = Transaction()
    error_message = transaction.RESPONSE_CODES[status_code]
    return render(request, 'paybox/error.html', {'error_message': error_message})


def success_response(request):
    return render(request, 'paybox/success.html', {})


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