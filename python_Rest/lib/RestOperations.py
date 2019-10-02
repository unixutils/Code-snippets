#/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1
import json


class RestOperations:
    
    def __init__(self, apiEndPoint, **kwargs):
        self.apiEndPoint = apiEndPoint
        self.kwargs = kwargs
    
    def SendGetReq(self):
        auth = self.CallAuth(self.kwargs)
        try:
            RespGetReq = requests.get(self.apiEndPoint, auth = auth)
        except Exception as SendGetReqException:
            print("Exception while sending GetRequest", SendGetReqException)
        return RespGetReq
    
    def SendPostReq(self):
        if 'PostData' not in self.kwargs:
            raise TypeError("request type 'Post' requries PostData")
        else:
            PostData = self.kwargs.get('PostData')
        auth = self.CallAuth(self.kwargs)
        try:
            RespPostReq = requests.post(self.apiEndPoint, PostData, auth = auth)
        except Exception as SendPostReqException:
            print("Exception while sending PostRequest", SendPostReqException)
        return RespPostReq
    
    def ReadFile(self, ParamsFilePath):
        self.ParamsFilePath = ParamsFilePath
        try:
            ParamsFile = file.open(ParamsFilePath)
            ParseParamsfromFile(ParamsFile)
        except Exception as ReadFileException:
            print("Exception while reading ParamsFile", ReadFileException)
            
    def ParseParamsfromFile(self, ParamsFile):
        self.ParamsFile = ParamsFile
        try:
            json.load(ParamsFile)
        except Exception as ParamsFileException:
            print("Exception while parsing ParamsFile", ParamsFileException)
            
    def CallAuth(self, OptionalAttrs):
        authType = self.ValidateAuthAttrs(OptionalAttrs)
        if not authType:
            auth = None            
        elif authType == 'token':
            auth = HTTPBearerAuth(OptionalAttrs.get('token'))
        elif authType == 'basic':
            auth = HTTPBasicAuth(OptionalAttrs.get('username'), OptionalAttrs.get('password'))
        elif authType  == 'digest':
            auth = HTTPDigestAuth(OptionalAttrs.get('username'), OptionalAttrs.get('password'))
        elif authType  == 'oa1':
            auth = OAuth1(OptionalAttrs.get('AppKey'), OptionalAttrs.get('AppSecret'), OptionalAttrs.get('UserToken'), OptionalAttrs.get('UserSecret'))
        return auth
    
    def ValidateAuthAttrs(self, OptionalAttrs):
        if 'authType' not in OptionalAttrs:
            authType = None
        else:
            if OptionalAttrs.get('authType') not in ['token', 'digest', 'basic', 'oa1']:
                raise ValueError("Unknown authType received", OptionalAttrs.get('authType'))
            else:
                if OptionalAttrs.get('authType') == 'token' and 'token' not in OptionalAttrs:
                    raise ValueError("authType 'token' requires token")
                elif OptionalAttrs.get('authType') == 'basic' and not all(attr in OptionalAttrs for attr in ['username', 'password']):
                    raise ValueError("authType 'basic' requires username, password")
                elif OptionalAttrs.get('authType') == 'digest' and not all(attr in OptionalAttrs for attr in ['username', 'password']):
                    raise ValueError("authType 'digest' requires username, password")
                elif OptionalAttrs.get('authType') == 'oa1' and not all(attr in OptionalAttrs for attr in ['AppKey', 'AppSecret', 'UserToken' 'UserSecret']):
                    raise ValueError("authType 'oa1' requires AppKey, AppSecret, UserToken, UserSecret")
                else:
                    authType = OptionalAttrs.get('authType')
        return authType

class HTTPBearerAuth(requests.auth.AuthBase):
    '''requests() does not support HTTP Bearer tokens authentication, create one'''
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r
