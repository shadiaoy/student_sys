import time
from django.urls import reverse
#from django.utils.deprecation import MiddlewareMixin
class MiddlewareMixin(object):
    def __init__(self,get_response=None):
        self.get_response=get_response
        super(MiddlewareMixin,self).__init__()

    def __call__(self,request):
        response=None
        if hasattr(self,'process_request'):
            response=self.process_request(request)
        if not response:
            response=self.get_response(request)
        if hasattr(self,'process_response'):
            response=self.process_response(request,response)
        return response

class TimeItMiddleware(MiddlewareMixin):
    def process_request(self,request):
        self.start_time=time.time()
        return
    def process_view(self,request,func,*args,**kwargs):
        if request.path != reverse('index'):
            return None

        start=time.time()
        response=func(request)
        costed=time.time() - start
        print('process view:{:.2f}s'.format(costed))
        return response
    def process_exception(self,request,exception):
        pass
    def process_template_response(self,request,response):
        return response
    def process_response(self,request,response):
        costed=time.time()-self.start_time
        print('request to response cost:{:.2f}s'.format(costed))
        return response
