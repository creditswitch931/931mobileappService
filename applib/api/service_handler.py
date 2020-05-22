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

__all__ = ['ServiceHandler', 'AirtimeHandler', "IkejaPrePaidHandler"]

# +-------------------------+-----------------------------+
# +-------------------------+-----------------------------+

class ServiceHandler:
    """
        Service scafold for all API integration 
    """ 
    __readonlyFields__ = []


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
        
        return {
            "trans_ref": self.request_ref,
            "trans_desc": self.resp_obj.params['responseDesc'],
            "trans_code": self.resp_obj.params['responseCode'],
            "trans_params": h.dump2json(self.req_data),
            "trans_resp": h.dump2json(self.resp_obj.params),
            "user_mac_address": self.kwargs['mac_address'],
            "user_id": self.kwargs['user_id'],
            "trans_type_id": self.kwargs['ref_id'],
            "trans_amount": self.form_data['amount']
        }


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
                ("out", "\n\r"),
                ("cmd", 'center'),
                ('out', self.__ServiceName__),
                ("cmd", "left"), 
                ('out', "Date: {}".format(self.get_date())),
                ("cmd", "center"),
                ("out", "__" * 15 )
            ]
 

    def printout_footer(self):
        # include seller Id at the footer always 
        # may be the mac_address is also sufficient

        return [
                ('out', '\n\r'), # print our a space before displaying the other
                ("cmd", "center"),
                ("out", "_" * 15 ),
                ("out", 'Mac Address: {}'.format(self.kwargs['mac_address'])),
                ("out", "Login Id: {}".format(self.kwargs['login_id'])),
                ("out", "\n\r"),
                ("out", "***Thanks For your patronage***"),                
                ("out", "POWERED BY CREDIT SWITCH"),
                ("out", "\n\r\n\r\n\r")
            ]


    def init_form(self):
        _Form = getattr(f, self.__formCls__)
        form_ins = _Form()
        form_ins.init_func()
        fh = FormHandler(form_ins)

        return fh.render()


    def get_service_form(self):
        
        # this method generates the service form 
        # and also specifies the readonly defaults of the form 
        # based on the response of the validation process 
        # can also resend the init_form based on the status below. 
        raise NotImplementedError


    def get_response(self):
        raise NotImplementedError


    def get_service_form(self, formname):     
        
        _Form = getattr(f, formname)
        
        # set field parameters from the validate output
        _data  = {}

        for obj in self.resp_obj.params['data']:
            for k, v in obj.items():
                _data[k] = v

        fm = FormHandler(_Form(**_data), 
                         readonly_field=self.__readonlyFields__)

        return fm.render()



class AirtimeHandler(ServiceHandler):

    __name__ = 'Airtime'
    __url__ = "/api/service/vending"
    __formCls__ = 'Airtime'
    __form_label__ = "Send"
    __ServiceName__ = "Airtime Service"
    __ServiceCode__ = ""
    
    def call_service(self):
        return airtime_service.airtime_vending(
                self.kwargs['login_id'], 
                self.form_data["amount"],
                self.form_data["phone"],
                self.__ServiceCode__, # provider e.g mtn, airtel, globacom, 9mobile 
                self.request_ref
            )
 
    def vend_service(self):

        self.request_ref = h.random_num(12)

        api_resp =  self.call_service()
        self.req_data = {"login_id": self.kwargs['login_id'], 
                         'amount': self.form_data['amount'],
                         "phone": self.form_data['phone'], 
                         "network": self.__ServiceCode__,
                         'recipient': self.form_data['phone']
                        }
        
        self.data = api_resp[1]

        self.resp_obj.api_response_format(api_resp[1])
        self.save_transactions()

        if self.resp_obj.status():
            self.resp_obj.add_params('API_forms', self.init_form() )
            self.resp_obj.add_params("API_formCls", self.__formCls__ )
            self.resp_obj.add_params('API_url_path', self.__url__)
            self.resp_obj.add_params('btn_label', self.__form_label__)



    def printout(self):
        cmd = "cmd"
        out = "out"
        body = [
            (cmd, "center"), 
            (out, "NETWORK: {}".format(self.req_data['network'])),            
            (out, "RECEIPIENT: " + self.req_data['phone'] + ""),            
            (out, "AMOUNT: " + h.currency_formatter(float(self.req_data['amount'])) + " NGN"),                        
            (out, "Trans Ref: {}".format(self.data['tranxReference'])),            
            (out, "Confirmation Code: " + self.data['confirmCode']),
            (out, "mReference: " + self.data['mReference']),                        
            (out, '\n\r'),
            (out, "Status: " + self.resp_obj.params['responseDesc'].upper()),
            (cmd, "center")            
            
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
            ("Status", self.resp_obj.params['responseDesc'].upper())
        ]  


class MtnHandler(AirtimeHandler):
    __ServiceCode__ = "mtn"


class _9MobileHandler(AirtimeHandler):
    __ServiceCode__ = "9mobile"

class AirtelHandler(AirtimeHandler):
    __ServiceCode__ = "airtel"
 
class GlobacomHandler(AirtimeHandler):
    __ServiceCode__ = "globacom"
 

 

class IkejaPrePaidHandler(ServiceHandler):
    __name__ = "IkejaPrePaid"
    __url__ = "/api/service/validate"
    # __formCls__ = "IkejaPrePaid"
    __formCls__ = "ElectricityValidate"
    __form_label__ = "Validate"
    __ServiceName__ = "Ikeja Disco Prepaid"
    __ServiceCode__ = "E01E"
    __vendform__ = "IkejaPrePaid"
    __readonlyFields__ = []
      

    def validate_service(self):
        
        validate_resp = power_service.electricity_validate(
                                            self.kwargs['login_id'], 
                                            self.form_data["meterNumber"], 
                                            self.__ServiceCode__
                                        )

        temp_resp = validate_resp[1]
        
        if validate_resp[0] == 200:
            if temp_resp['statusCode'] == '00':                                
                self.resp_obj.api_response_format(temp_resp['detail'])
                self.resp_obj.add_message(temp_resp['statusDescription'])
                self.resp_obj.success()

            else:
                self.resp_obj.api_response_format(temp_resp)

        else:
            self.resp_obj.api_response_format(temp_resp)
 

        if self.resp_obj.status():
            self.resp_obj.add_params("API_url_path", "/api/service/vending")
            self.resp_obj.add_params("API_forms", self.get_service_form(self.__vendform__))
            self.resp_obj.add_params("API_formCls", self.__vendform__)
            self.resp_obj.add_params('btn_label', "Send")
            

    def call_service(self):
        return power_service.ikeja_prepaid(self.kwargs['login_id'], 
                        self.form_data['meterNumber'],
                        self.__ServiceCode__,
                        self.form_data["amount"],
                        self.request_ref,
                        self.form_data['customerDtNumber'],
                        self.form_data.get('providerRef') or "89128942039"
                    )


    def vend_service(self):
        self.request_ref = h.random_num(12)
         
        api_resp = self.call_service()

        self.req_data = {"login_id": self.kwargs['login_id'], 
                         "meterNumber": self.form_data['meterNumber'],
                         "service_id": self.__ServiceCode__,
                         'amount': self.form_data['amount'],
                         "reference_id": self.request_ref,
                         "customerDtNumber": self.form_data['customerDtNumber'],
                         'recipient': self.form_data['meterNumber']
                        } 
         
        self.data = api_resp[1]

        self.resp_obj.api_response_format(self.data)
        self.save_transactions()
        
        if self.resp_obj.status():
            self.resp_obj.add_params('API_forms', self.init_form() )
            self.resp_obj.add_params("API_formCls", self.__formCls__)
            self.resp_obj.add_params('API_url_path', self.__url__)
            self.resp_obj.add_params('btn_label', "Validate")


    def printout(self):
        cmd = "cmd"
        out = "out"
 
        body = [
            (cmd, "center"),
            (out, "\n\r"),
            (out, self.__ServiceName__),
            (cmd, "center"),
            (out, "Meter No: " + self.req_data['meterNumber']),
            (cmd, "center"),
            (out, "Amount: " + h.currency_formatter(float(self.req_data['amount'])) + " NGN"),
            (out, "\n\r"),              
            (cmd, "left"),
            (out, "Unit Cost: {}".format(self.data['detail'].get('unitCost'))),
            (out, "Units: {}".format(self.data['detail'].get('units'))),
            (out, "Vat: {}".format(self.data['detail'].get('vat'))),
            (cmd, 'center'),
            (out, "\n\r"),
            (out, "Token"),
            (out, self.data['detail'].get("token")),
            (out, "\n\r"),
            (cmd, "left"),
            (out, "Trans Ref: {}".format(self.data['detail']['tranxId'])),
            (out, 'Status: {}'.format(self.resp_obj.params['responseDesc'].upper()))

        ]

        return body


    def get_response(self):       

        _resp = self.data['detail']

        return [
            ("Disco", self.__ServiceName__),
            ("Name", _resp['name']),
            ("Meter Number", self.req_data['meterNumber']),
            ("Account ID", _resp['accountId']),
            ("Amount",  _resp['amount'] + " NGN"),
            ("Unit Cost", _resp.get('unitCost')),
            ("Units", _resp.get("units")),
            ('Vat', _resp.get('vat')),
            ("Token", _resp.get("token")),
            ("Trans Ref", _resp['tranxId']),
            ("Status", self.resp_obj.params['responseDesc'].upper())            
        ]



class EkoPrePaidHandler(IkejaPrePaidHandler):

    __name__ = "EkoPrePaid" 
    __ServiceName__ = "Eko Disco Prepaid"
    __ServiceCode__ = 'E05E'
    __vendform__ = 'EkoPrePaid'
    __readonlyFields__ = ["customerDtNumber", "name", 
                         "address", "meterNumber", "customerAccountType",
                         "providerRef"]
    

    def call_service(self):
        return power_service.eko_prepaid(self.kwargs['login_id'], 
                        self.form_data['meterNumber'],
                        self.__ServiceCode__,
                        self.form_data["amount"],
                        self.request_ref,
                        self.form_data['customerDtNumber'],
                        self.form_data.get('providerRef') or "89128942039"
                    )

class IbadanPrePaidHandler(IkejaPrePaidHandler):          
    
    __name__ = "IbadanPrePaid"      
    __ServiceName__ = "Ibadan Disco Prepaid"
    __ServiceCode__ = "E07E"
    __vendform__ = 'IbadanPrePaid'
    __readonlyFields__ = []


    def call_service(self):
        return power_service.ibadan_prepaid(self.kwargs['login_id'], 
                        self.form_data['meterNumber'],
                        self.__ServiceCode__,
                        self.form_data["amount"],
                        self.request_ref,
                        self.form_data['customerDtNumber'],
                        (self.form_data.get('providerRef') or "89128942039")
                    )

# class AbujaPrePaidHandler(IkejaPrePaidHandler):      
#     # __url__ = "/api/service/validate"
#     # __formCls__ = "ElectricityValidate"
#     # __form_label__ = "Validate"
#     __name__ = "AbujaPrePaid"
#     __ServiceName__ = "Abuja Disco Prepaid"
#     __ServiceCode__ = "E07E"
#     __vendform__ = 'AbujaPrePaid'



class DataHandler(AirtimeHandler):
    __name__ = 'Data'
    __url__ = "/api/service/vending"
    __formCls__ = 'Data'
    __form_label__ = "Send"
    __ServiceName__ = "Data Subscription"

    def call_service(self):
        return data_service.data_vending(self.kwargs['login_id'], 
                                         self.form_data['amount'], 
                                         self.form_data['phone'], 
                                         self.__ServiceCode__, 
                                         self.request_ref
                                        )


class MtnDataHandler(DataHandler):
    __name__ = 'Mtn Data'
    __ServiceName__ = "MTN Data Sub"
    __ServiceCode__ = "mtn"
    __formCls__ = 'MtnData'


class AirtelDataHandler(DataHandler):
    __name__ = "Airtel Data"
    __ServiceCode__ = "airtel"
    __ServiceName__ = "Airtel Data Sub"
    __formCls__ = 'AirtelData'

class GloDataHandler(DataHandler):
    __name__ = "Globacom Data"
    __ServiceCode__ = "globacom"
    __ServiceName__ = "Glo Data Sub"
    __formCls__ = 'GloData'

class NMobDataHandler(DataHandler):
    __name__ = "Globacom Data"
    __ServiceCode__ = "9mobile"
    __ServiceName__ = "Glo Data Sub"
    __formCls__ = 'NMobileData'
 


class StartimesTvHandler(ServiceHandler):

    __name__ = 'Startimes'
    __url__ = "/api/service/validate"
    __formCls__ = 'ValidateIUC'
    __form_label__ = "Validate"
    __ServiceName__ = "Startimes Subscription"
    __vendform__ = "Startimes"
    __readonlyFields__ = ["customerName", 'balance', "smartCardCode"]


    def validate_service(self):
        
        output = cable_service.startimes_validate(self.kwargs['login_id'], 
                                                  self.form_data['customerNo'])


        self.resp_obj.api_response_format(output[1])

        if self.resp_obj.status():
            self.resp_obj.add_params("API_url_path", "/api/service/vending")
            self.resp_obj.add_params("API_forms", self.get_service_form(self.__vendform__))
            self.resp_obj.add_params("API_formCls", self.__vendform__)
            self.resp_obj.add_params('btn_label', "Send")
             
    
  

    def vend_service(self):

        self.request_ref = h.random_alphanum(16)
         
        api_resp = cable_service.startimes_vending(self.kwargs['login_id'], 
                                               self.form_data['smartCardCode'], 
                                               self.form_data['amount'],
                                               self.request_ref)

        self.req_data = {"login_id": self.kwargs['login_id'], 
                         "smartCardCode": self.form_data['smartCardCode'],
                         'amount': self.form_data['amount'],
                         "reference_id": self.request_ref,
                         'recipient': self.form_data['smartCardCode']
                        } 
        
        self.data = api_resp[1]


        self.resp_obj.api_response_format(self.data)
        self.save_transactions()
        
        if self.resp_obj.status():
            self.resp_obj.add_params('API_forms', self.init_form())
            self.resp_obj.add_params("API_formCls", self.__formCls__)
            self.resp_obj.add_params('API_url_path', self.__url__)
            self.resp_obj.add_params('btn_label', "Validate")


   
    def printout(self):
        cmd = "cmd"
        out = "out"
 
        body = [
            (cmd, "center"),            
            (out, self.__ServiceName__),            
            (out, "Smart Card No: " + self.req_data['smartCardCode']),            
            (out, "Amount: " + h.currency_formatter(float(self.req_data['amount'])) + " NGN"),
            (out, "\n\r"),              
            (cmd, "left"),
            (out, "Trans Ref: {}".format(self.data['transactionNo'])),
            (out, 'Status: {}'.format(self.resp_obj.params['responseDesc'].upper()))
        ]

        return body


    def get_response(self):
        
        _resp = self.data
        
        # {'statusCode': '00', 'statusDescription': 'successful', 
        # 'details': {'name': 'MR & MRS XD MICHAEL', 'address': '71 XAVIER CRESCENT ', 
        # 'accountId': '0110347638', 'providerRef': '150168371668'}, 
        # 'transactionNo': 8856937547}

        return [
            ("Cable TV ", self.__ServiceName__),
            ("Name", self.form_data['customerName']),
            ("Smart Card No", self.req_data['smartCardCode']),
            ("Amount", "{} NGN".format(self.form_data['amount'])),                        
            ("Trans Ref", _resp['transactionNo']),
            ("Status", self.resp_obj.params['responseDesc'].upper())            
        ]



class DsTvHandler(ServiceHandler):
    __name__ = 'Dstv'
    __url__ = "/api/service/validate"
    __formCls__ = 'DstvValidation'
    __form_label__ = "Validate"
    __ServiceName__ = "Dstv Subscription"
    __vendform__ = "Dstv"
    __readonlyFields__ = ["amount", "customerNo", "customerName" ]
    __ServiceCode__ = "dstv"
    __ServicePlanGrp__ = "dstvpackage"


    def validate_service(self):
        
        output = cable_service.multichoice_validate(self.kwargs['login_id'], 
                                                    self.form_data['smartCardCode'], 
                                                    self.__ServiceCode__
                                                    )

        # {'statusCode': '00', 'statusDescription': 
        # {'customerNo': 283375350, 'accountStatus': 'OPEN', 'firstname': '', 
        # 'lastname': 'MOBILE', 'customerType': 'SUD', 'invoicePeriod': 1, 
        # 'dueDate': '2018-09-29T00:00:00+01:00'}}
        
        if output[1]['statusCode'] == "00":

            self.resp_obj.api_response_format(output[1]['statusDescription'])
            self.resp_obj.success()
            self.resp_obj.add_message("smart card validated successsfully.")

            # derive the amount based on the productcode here 
            firstname = output[1]["statusDescription"]["firstname"]
            lastname = output[1]["statusDescription"]["lastname"]

            # get the service amount here 
             
            qry = m.ServicePlan.get_extrafield(code=self.form_data['service_plans'],
                                               group_name=self.__ServicePlanGrp__
                                               )
            
            print(qry)

            # self.form_data['service_plans']

            self.resp_obj.params['data'].extend([
                    {"amount": qry.extra_field},
                    {"productCodes": self.form_data['service_plans']},
                    {"customerName": ('{} {}'.format(firstname, lastname)).strip()},
                    {"invoicePeriod": 1}
                ]
            )
        else:
            self.resp_obj.failed()
            self.resp_obj.add_message("operation failed")

        
        if self.resp_obj.status():
            self.resp_obj.add_params("API_url_path", "/api/service/vending")
            self.resp_obj.add_params("API_forms", self.get_service_form(self.__vendform__))
            self.resp_obj.add_params("API_formCls", self.__vendform__)
            self.resp_obj.add_params('btn_label', "Send")
            

    def vend_service(self):
         
        _func = cable_service.multichoice_vending
        self.request_ref = h.random_alphanum(16)        


        self.form_data['amount'] = float(self.form_data['amount']) * self.form_data['invoicePeriod']
        
        output = _func(self.kwargs['login_id'], self.form_data['customerNo'], 
                       self.form_data['customerName'], self.__ServiceCode__,
                       self.form_data['amount'], self.form_data['invoicePeriod'], 
                       self.form_data['productCodes'], self.request_ref
                    )         

        self.data = output[1]

        self.req_data = {"login_id": self.kwargs['login_id'], 
                         "customerNo": self.form_data['customerNo'], 
                         "CustomerName": self.form_data['customerName'], 
                         "ServiceCode": self.__ServiceCode__,
                         "amount": self.form_data['amount'], 
                         'Invoice Period': self.form_data['invoicePeriod'], 
                         'productcode' : self.form_data['productCodes'], 
                         "request_ref": self.request_ref,
                         'recipient': self.form_data['customerNo']
                        } 
         
        if self.data['statusCode'] == '00':
            self.resp_obj.api_response_format(self.data['statusDescription'])
            self.resp_obj.success()
            self.resp_obj.add_message(self.data['statusDescription']['message'])

        else:
            self.resp_obj.failed()
            self.resp_obj.add_message("Transaction failed.")

        self.save_transactions()                       

        if self.resp_obj.status():
            self.resp_obj.add_params('API_forms', self.init_form())
            self.resp_obj.add_params("API_formCls", self.__formCls__)
            self.resp_obj.add_params('API_url_path', self.__url__)
            self.resp_obj.add_params('btn_label', "Validate")


    def printout(self):
        cmd = 'cmd'
        out = 'out'

        return [
            (out, '\n\r'),
            (cmd, "center"),                                   
            (out, "Smart Card No: " + self.form_data['customerNo']), 
            (out, "Customer Name: " + self.form_data['customerName']),
            (out, "Amount: " + h.currency_formatter(float(self.form_data['amount'])) + " NGN"),
            (out, '\n\r'),
            (out, 'Trans Ref: {}'.format(self.request_ref)),
            (out, "Trans No: {}".format(self.data['statusDescription']['transactionNo'])),
            (out, 'Status: {}'.format(self.resp_obj.params['responseDesc'].upper()))
        ]           


    def get_response(self):
        
        return [
            ("Cable TV ", self.__ServiceName__),
            ("Name", self.form_data['customerName']),
            ("Smart Card No", self.form_data['customerNo']),
            ("Amount",  "{} NGN".format(self.form_data['amount'])),                        
            ("Trans Ref", self.request_ref),
            ("Trans No", self.data['statusDescription']['transactionNo']),
            ("Status", self.resp_obj.params['responseDesc'].upper())            
        ]




class GoTvHandler(DsTvHandler):
    __name__ = 'Gotv'
    __url__ = "/api/service/validate"
    __formCls__ = 'GotvValidation'
    __vendform__ = "Gotv"
    __form_label__ = "Validate"
    __ServiceName__ = "Gotv Subscription"
    __readonlyFields__ = ["customerNo", "customerName", "amount"]
    __ServiceCode__ = "gotv"
    __ServicePlanGrp__ = "gotvplan"
 
 

    