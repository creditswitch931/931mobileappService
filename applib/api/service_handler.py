
from api_services import (airtime_service, cable_service, 
                          data_service, power_service,
                          api_lib)

from .resp_handler import FormHandler 

import importlib


__all__ = ['ServiceHandler', 'AirtimeHandler']



class ServiceHandler:
    """
        Service scafold for all API integration 
    """
    def __init__(self, form, data):
        pass

    
    def get_forms(self):
        """
            get the forms properties
        """
        pass


    def process_forms(self):
        """
            Process the submitted form before calling the service API
        """
        pass


    def vend_service(self):
        """
            
        """

    def save_transactions(self, kwargs):
        pass


    def print_structure(self):
        # always implement this methods in order to define the printout layer 
        raise NotImplemented




class AirtimeHandler(ServiceHandler):

    __name__ = 'airtime'
    __url__ = '/api/process'
    __formCls__ = 'Airtime'
    


  





