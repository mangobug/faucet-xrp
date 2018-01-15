import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from xrp.base.models import TimeStampAwareModel
# Create your models here.


class Faucet( TimeStampAwareModel ):
    """
    Faucet model
    """

    user = models.ForeignKey(User)
    coins = models.DecimalField(max_digits = 12, decimal_places = 8)


    def __unicode__(self):
        return _("%s") % (self.user)

    class Meta:
        app_label = "faucet"
        verbose_name = "faucet"
        verbose_name_plural = "faucets"


class Instance( TimeStampAwareModel ):
    """
    Instance model
    """

    faucet = models.ForeignKey(Faucet)
    timer = models.DateTimeField()
    temp_coins = models.DecimalField(max_digits = 12, decimal_places = 8)


    def __unicode__(self):
        return _("%s") % (self.faucet.user)

    def get_timer(self):
        """
        Returns the time in a particular format
        """
        return '%s' % (self.timer.strftime("%B %d, %Y %H:%M:%S"))

    def reset_timer(self):
        """
        Reset timer once reward is claimed
        """
        self.timer = datetime.datetime.now()
        self.save()
        return True

    class Meta:
        app_label = "faucet"
        verbose_name = "instance"
        verbose_name_plural = "instances"
