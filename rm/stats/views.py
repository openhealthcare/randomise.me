"""
Views to do server-side stats help
"""
from django.http import HttpResponse
from django.views.generic import View

from rm.stats.utils import nobs, ttest

class PowerCalcView(View):
    """
    Run a power calculation
    """
    def post(self, *args, **kwargs):
        """
        Calculate the required number of participants
        for the variables given

        Return: str(int)
        Exceptions: None
        """
        effect, alpha, power = [float(self.request.POST.get(k))
                                for k in ['effect-size', 'alpha', 'power']]
        num = ttest(effect=effect, alpha=alpha, power=power)

        # estimated, impressive = [int(self.request.POST.get(k))
        #                          for k in ['impressive', 'estimated']]
        # num = nobs(estimated=estimated, impressive=impressive)
        return HttpResponse(str(num))
