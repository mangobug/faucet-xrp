from django.conf.urls import patterns, url

from xrp.faucet.views import faucet, claim_reward


urlpatterns = patterns('',

    url( r'^$',
        faucet,
        {'template_name': 'faucet/faucet.html'},
        name = 'faucet' ),

    url( r'^claim/$',
        claim_reward,
        {'template_name': 'faucet/success.html'},
        name = 'claim_reward' ),
)
