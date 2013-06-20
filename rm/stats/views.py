"""
Views to do server-side stats help
"""
from django.http import HttpResponse
from django.views.generic import View

from rm.stats.utils import nobs, ttest, binary_superiority

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
        return HttpResponse(str(num))


class PowerCalcBinaryView(View):
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
        p1, p2 = int(self.request.POST.get('p1')), int(self.request.POST.get('p2'))
        power = float(self.request.POST.get('power'))
        alpha = float(self.request.POST.get('alpha'))
        num = binary_superiority(p1, p2, alpha, power) * 2
        return HttpResponse(str(num))
