import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from xrp.faucet.models import Faucet, Instance

# Create your views here.
@login_required
def faucet(request, template_name):
    """
    $XRP faucet
    """

    user_instance = Instance.objects.get(faucet__user = request.user)

    data = {
        "instance": user_instance,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

@login_required
def claim_reward(request, template_name):
    """
    Claim reward form
    """
    instance = Instance.objects.get(faucet__user = request.user)
    time = datetime.datetime.now() - instance.timer
    print time
    instance.reset_timer()

    instance.faucet.coins += instance.temp_coins
    instance.faucet.save()
    instance.temp_coins = 0
    instance.save()

    data = {

    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))
