
ACCESS_KEY = 'AKIAZIRM6OHCCX33V7F7'
SECRET_KEY = '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'
REGION = "us-west-2"
QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/636823171524/my_que_t'

# stage 
#API_URL = 'http://ec2-18-191-238-218.us-east-2.compute.amazonaws.com:81/ELEVATEPHP/public/index1.php/api/company([[cmpid]])'
#API_URL_MAIN = 'http://ec2-18-191-238-218.us-east-2.compute.amazonaws.com:81/ELEVATEPHP/public/index1.php/api'

#live  
#API_URL = 'https://esignapi.elevate-holistics.com/ELEVATEPHP/public/index1.php/api/company([[cmpid]])'
#API_URL_MAIN= 'https://esignapi.elevate-holistics.com/ELEVATEPHP/public/index1.php/api'

#live Abst
API_URL = 'http://54.163.218.186/ELEVATEPHP/public/index1.php/api/company([[cmpid]])'
API_URL_MAIN= 'http://54.163.218.186/ELEVATEPHP/public/index1.php/api'


# https://esignapi.elevate-holistics.com/ELEVATEPHP/public/index1.php/api/company([[cmpid]])
# https://esignapi.elevate-holistics.com/ELEVATEPHP/public/index1.php/api
temp_folder = "temp"
debug = True

bucket = "dcbdb209393048bdaf49c63c3b27f5f1-cmp"


def getAPIURL(cmpid: int):
    return API_URL.replace("[[cmpid]]", str(cmpid))


