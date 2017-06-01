from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Post
from .paybox import Transaction


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'paybox/posts_list.html', {'posts': posts})


def make_payment(request, order_reference):
    import ipdb; ipdb.set_trace()
    # Your order object
    order = get_object_or_404(Post, reference=order_reference)

    transaction = Transaction(
        production=False,
        PBX_TOTAL=order.total_incl_tax,
        PBX_PORTEUR='dev.alejandrovillamarin@gmail.com',
        PBX_TIME=order.created_date,
        PBX_CMD=order.reference)

    form_values = transaction.post_to_paybox()

    return render(request, 'paybox/payment.html', {
        'action': form_values['action'],
        'mandatory': form_values['mandatory'],
        'accessory': form_values['accessory'],
    })
    # return render(request, 'paybox/make_payment.html', {})