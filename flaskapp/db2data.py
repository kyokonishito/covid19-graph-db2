import requests
import json
import logging
import traceback
import datetime
import time
import pandas as pd
log_fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_fmt, level=logging.DEBUG)


class Db2dataTool:
    userid = None
    passwd = None
    dbname = None
    crn = None
    url = None
    token = None

    def __init__(self, db2info):
        self.userid = db2info['USERID']
        self.passwd = db2info['PASSWD']
        self.dbname = db2info['DBNAME']
        self.crn = db2info['CRN']
        self.url = db2info['URL']

    def __handleError(self, msg):
        logging.error(msg)
        result = {}
        result['status'] = 'ERROR'
        result['message'] = json.dumps(msg)
        return json.dumps(result)

    def __verifyDate(self, datestr):
        try:
            newDate = datetime.datetime.strptime(datestr, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def getData(self, fromdate, todate):
        result = self.getToken()
        resjson = json.loads(result)
        if resjson['status'] == 'ERROR':
            return result
        
        result = self.doQuery(fromdate, todate)
        resjson = json.loads(result)
        if resjson['status'] == 'ERROR':
            return result
        
        result = self.getSQLResults(resjson['message'], fromdate, todate)
        return result


    def getSQLResults(self, id, fromdate, todate):
        # time.sleep(1)
        #REST API の　　URL 作成
        REST_API_URL = self.url
        service_name = '/dbapi/v4/sql_jobs/%s'%(id)
        host = REST_API_URL + service_name

        # request header作成
        headers = {}
        headers ['content-type'] = "application/json"
        headers ['x-deployment-id']=self.crn
        headers ['X-DB-Profile'] = "BLUDB"
        # headerにアクセストークンをセット
        headers ['authorization'] =  'Bearer ' + self.token

        start = time.time()
        df = pd.DataFrame()
        while True:
            try:
                r = requests.get(host, headers=headers,  verify = False)
            except Exception as err:
                return self.__handleError(traceback.format_exc())

            # Check error
            if (r.status_code != 200):
                message = r.json()['errors']
                return self.__handleError(message)

            if r.json()["status"] == "failed":
                message = r.json()["results"][0]["error"]
                return self.__handleError(message)
            
            if len(r.json()["results"]) > 0 :
                if r.json()["results"][0]["rows_count"] > 0:
                    print(r.json()["results"][0]["rows_count"])
                    if len(df) < 1:
                        df = pd.DataFrame(data=r.json()["results"][0]["rows"] , columns =['labels', 'data'])
                    else:
                        df = df.append(r.json()["results"][0]["rows"])

            if r.json()["status"] == "completed":
                break             

            if time.time() - start > 180: 
                message = "sql_jobs timeout 3min"
                return self.__handleError(message)
        
        try:
            if len(df) < 1:
                message = "No result data from %s to %s. "%(fromdate, todate)
                return self.__handleError(message)
            
            df['data'] = df['data'].astype(int)
            resultdata = {}
            resultdata['labels'] = df['labels'].values.tolist()
            resultdata['data'] = df['data'].values.tolist()
        except Exception as err:
                return self.__handleError(traceback.format_exc())

        result = {}
        result['status'] = 'SUCCESS'
        result['message'] = resultdata
        return json.dumps(result)

    def doQuery(self, fromdate, todate):
        if not (self.__verifyDate(fromdate) or self.__verifyDate(todate)):
            return self.__handleError("Date format is invalid")

        #REST API の　　URL 作成
        REST_API_URL = self.url
        service_name = '/dbapi/v4/sql_jobs'
        host = REST_API_URL + service_name

        # request header作成
        headers = {}
        headers ['content-type'] = "application/json"
        headers ['x-deployment-id']=self.crn
        headers ['X-DB-Profile'] = "BLUDB"
        # headerにアクセストークンをセット
        headers ['authorization'] =  'Bearer ' + self.token

        
        sqlstr = "SELECT 公表_年月日, count(公表_年月日) AS 人数 FROM NISHITO.COVID_19_東京 WHERE  公表_年月日 BETWEEN '%s' AND '%s' GROUP BY 公表_年月日;" % (
            fromdate, todate)

        body ={
           "commands":  sqlstr,
           "limit"  : 1000000,
           "separator": ";",
           "stop_on_error":"no"
        }

        # Call the RESTful service
        try:
            r = requests.post(host, headers=headers,  json=body, verify = False)
        # print( r.status_code)
        except Exception as err:
            return self.__handleError(traceback.format_exc())

        # Check error
        if (r.status_code != 201): # There was an error with the authentication
            message = r.json()['errors']
            return self.__handleError(message)
        
        result ={}
        result['status'] = 'SUCCESS'
        result['message'] = r.json()["id"]
        return json.dumps(result)

    def getToken(self):
        # REST API の　　URL 作成
        REST_API_URL = self.url
        service_name = '/dbapi/v4/auth/tokens'
        host = REST_API_URL + service_name

        # request header作成
        headers = {}
        headers['content-type'] = "application/json"
        headers['x-deployment-id'] = self.crn

        # parameter dbアクセス用のuid, pwを指定
        params = {}
        params['userid'] = self.userid
        params['password'] = self.passwd

        result = {}

        # Call the RESTful service
        try:
            r = requests.post(host, headers=headers,  data=json.dumps(params))
        except Exception as err:
            return self.__handleError(traceback.format_exc())

        # Check for Invalid credentials
        if (r.status_code == 401):  # There was an error with the authentication
            message = r.json()['errors']
            return self.__handleError(message)

        # Check for anything other than 200/401
        if (r.status_code != 200):  # Some other failure
            message = r.json()['errors']
            return self.__handleError(message)

        # Retrieve the access token
        try:
            access_token = r.json()['token']
            # print(r.json())
        except:
            return self.__handleError(r.json())

        result['status'] = 'SUCCESS'
        result['message'] = access_token
        self.token = access_token
        return json.dumps(result)
