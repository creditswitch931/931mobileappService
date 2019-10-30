# +-------------------------+-----------------------------+
# Written By   : Uzodinma Jeff
# +-------------------------+-----------------------------+
# Filename     : service_handler.py
# +-------------------------+-----------------------------+
# Description  : Code to handle service integrations and 
#              : service renderings for all mobile agents.
# +-------------------------+-----------------------------+
# Company Name :  Ecardex Ltd 
# +-------------------------+-----------------------------+


# +-------------------------+-----------------------------+
import datetime 
# +-------------------------+-----------------------------+

from api_services import (airtime_service, cable_service, 
                          data_service, power_service,
                          api_lib)

from .resp_handler import FormHandler 

import applib.forms  as f 
from applib import model as m  
from applib.lib import helper as h 


# +-------------------------+-----------------------------+
# +-------------------------+-----------------------------+

__all__ = ['ServiceHandler', 'AirtimeHandler', "ElectricityHandler"]

# +-------------------------+-----------------------------+
# +-------------------------+-----------------------------+

class ServiceHandler:
    """
        Service scafold for all API integration 
    """ 

    def __init__(self, form_data, resp, **extra_data):
        self.form_data = form_data
        self.kwargs = extra_data
        self.resp_obj = resp

    def vend_service(self):
        """
            Handle the service rendering part            
        """
        raise NotImplementedError

    
    def validate_service(self):
        """
            Handle the service rendering part            
        """
        raise NotImplementedError

    
    def trans_params(self):
        raise NotImplementedError


    def save_transactions(self):
        m.Transactions.save(**self.trans_params())


    def printout(self):
        # always implement this methods in order to define the printout layer 
        raise NotImplementedError

    def get_date(self):
        return datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S %p")

    def get_printout(self):
        return (self.printout_header() + 
                self.printout() + 
                self.printout_footer())

    def printout_header(self):        
        return [
                ("cmd", "center"), 
                ("image", h.get_logo()),
                ("out", "\r"),
                ("cmd", 'center'),
                ('out', self.__ServiceName__),
                ("cmd", "left"), 
                ('out', "Date: {}".format( self.get_date() ) ),
                ("out", "_+" * 15 ),

            ]


    def printout_footer(self):
        # include seller Id at the footer always 
        # may be the mac_address is also sufficient

        return [
                ("cmd", "center"),
                ("out", "***Thanks For your patronage***"),
                ("cmd", "center"), 
                ("out", "POWERED BY CREDIT SWITCH"),
                ("out", "\n\r\n\r\n\r\n\r")                
            ]


    def init_form(self):
        raise NotImplementedError


    def get_service_form(self):
        
        # this method generates the service form 
        # and also specifies the readonly defaults of the form 
        # based on the response of the validation process 
        # can also resend the init_form based on the status below. 
        raise NotImplementedError


    def get_response(self):
        raise NotImplementedError




class AirtimeHandler(ServiceHandler):

    __name__ = 'airtime'
    __url__ = "/api/service/vending"
    __formCls__ = 'Airtime'
    __form_label__ = "Send"
    __ServiceName__ = "Airtime Service"
    
    def vend_service(self):

        self.request_ref = h.random_num(12)
        
        func = airtime_service.airtime_vending
        api_resp = func(self.kwargs['login_id'], 
                        self.form_data["amount"],
                        self.form_data["phone"],
                        self.kwargs['name'], # provider e.g mtn, airtel, globacom, 9mobile 
                        self.request_ref
                    )

        self.req_data = {"login_id": self.kwargs['login_id'], 
                         'amount': self.form_data['amount'],
                         "phone": self.form_data['phone'], 
                         "network": self.kwargs["name"]
                        }
        

        # {'statusCode': '00', 'statusDescription': 'successful', 
        #  'mReference': '933306100502', 'tranxReference': '150069864',
        #  'recipient': '08023238912', 'amount': '500.00', 
        #  'confirmCode': '5db96bfdbc585', 
        #  'transactionDate': '2019-10-30 10:54:53'}  
        
        self.data = api_resp[1]

        self.resp_obj.api_response_format(api_resp[1])
        self.save_transactions()


    def init_form(self):
        # return an empty form back to the mobile client
        fh = FormHandler(f.Airtime())
        return fh.render() 


    def printout(self):
        cmd = "cmd"
        out = "out"

        body = [
            (cmd, "center"),
            (out, "\n\r"),
            (out, "NETWORK: {}".format(self.req_data['network'])),
            (cmd, "center"),
            (out, "RECEIPIENT: " + self.req_data['phone'] + ""),
            (cmd, "center"),
            (out, "AMOUNT: " + h.currency_formatter(float(self.req_data['amount'])) + " NGN"),
            (out, "\n\r"),
            (cmd, "center"),  
            (out, "Trans Ref: {}".format(self.data['tranxReference'])),
            (cmd, "center"), 
            (out, "Confirmation Code: " + self.data['confirmCode']),
            (cmd, "center"), 
            (out, "mReference: " + self.data['mReference']),            
            (cmd, "left"), 
            (out, "Transaction Response: " + self.resp_obj.params['responseDesc'].upper()),
            (cmd, "center"),
            (out, "_+" * 15 ),
            (out, "\n")
        ]

        return body


    def get_response(self):
        return [
            ("NETWORK", self.req_data['network'] ),
            ("RECEIPIENT", self.req_data['phone']),
            ("AMOUNT", self.data["amount"] + " NGN"),
            ("Trans Ref", self.data['tranxReference']),
            ("Confirmation Code", self.data['confirmCode']),
            ("mReference", self.data['mReference']),
            ("Tranaction Response Desc", self.resp_obj.params['responseDesc'].upper())
        ]


    def trans_params(self):
        
        return {
            "trans_ref": self.request_ref,
            "trans_desc": self.resp_obj.params['responseDesc'],
            "trans_code": self.resp_obj.params['responseCode'],
            "trans_params": h.dump2json(self.req_data),
            "trans_resp": h.dump2json(self.resp_obj.params),
            "user_mac_address": self.kwargs['mac_address'],
            "user_id": self.kwargs['user_id'],
            "trans_type_id": self.kwargs['ref_id'],            
        }
         




class ElectricityHandler(ServiceHandler):
    __name__ = "electricity"
    __url__ = "/api/service/validate"
    __formCls__ = "ElectricityValidate"
    __form_label__ = "Validate"
    __ServiceName__ = "ELECTRIC BILL PAYMENT"


    def get_service_form(self):
        pass
    


