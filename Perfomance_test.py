import json
import statistics
import pandas as pd
from python_test_v2.helper import *
import smtplib
import requests

__author__ = 'Aravind'

class ResponseTime(object):

    def __init__(self):

        print "process started"
        self.get_api_response_timeing=[]
        self.post_api_response_timeing=[]
        self.get_api_mean=[]
        self.get_api_stddev=[]
        self.post_api_mean= []
        self.post_api_stddev =[]

    def build(self):
        self.get_api_response_timing()
        print "process end"


    def email_notification(self,status):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            #Next, log in to the server
            server.ehlo()
            server.starttls()
            server.login(username, password)
            msg = "Hello! your API is Internal server error.., "+status+ "Thanks" # The /n separates the message from the headers
            server.sendmail(username, receivers, msg)
        #checks status while sendin the email if any error occurs handles exception
        except Exception:
            pass

    def get_api_response_timing(self):

        # Hit the dynamic page 10 times, time the response time
        for n in range(0,10):
            r = requests.get(service_kibana,  headers=headers)
            roundtripp = r.elapsed.total_seconds()
            if r.status_code ==200:
                self.get_api_response_timeing.append(roundtripp)
            elif r.status_code ==400:
                pass
            else:
                status="get method"
                self.email_notification(status)

            r = requests.post(service_kibana, data=json.dumps(headers_post))
            roundtripp = r.elapsed.total_seconds()
            if r.status_code ==200:
                self.post_api_response_timeing.append(roundtripp)
            elif r.status_code ==400:
                pass
            else:
                status="post method"
                self.email_notification(status)

        get_api_mean= statistics.mean(self.get_api_response_timeing)
        post_api_mean= statistics.mean(self.post_api_response_timeing)

        get_api_stddev=  statistics.stdev(self.get_api_response_timeing)
        post_api_stddev= statistics.stdev(self.post_api_response_timeing)

        self.get_api_mean.append(get_api_mean)
        self.post_api_mean.append(post_api_mean)
        self.post_api_stddev.append(post_api_stddev)
        self.get_api_stddev.append(get_api_stddev)

        ew = pd.ExcelWriter('ResponseTime.xlsx')
        df=pd.DataFrame({"GET_API":self.get_api_response_timeing,"POST_API":self.post_api_response_timeing}).to_excel(ew, sheet_name='APIResponseTime')
        df=pd.DataFrame({"GET_API_Mean":self.get_api_mean,"GET_API_Stddev":self.get_api_stddev,"POST_API_Mean":self.post_api_mean,"POST_API_Stddev":self.post_api_stddev}).to_excel(ew, sheet_name='Mean&Stddev')


if __name__ == '__main__':
    runner = ResponseTime()
    runner.build()