#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
import json
import requests
import os,re,random,string
import hashlib
import time
import base64
from urllib import parse
from threading import Thread,Event
import logging
_LOGGER = logging.getLogger(__name__)

class XiaoaiTTS:
    def __init__(self, user, password): 
        requests.packages.urllib3.disable_warnings() 
        self.login_resutl=False
        self._CONFIGURING = {}
        self._user=user
        self._password=password        
        self.Service_Token=None
        self.deviceIds=None
        self.userId=None
        self._cookies={}
        self._request=requests.session() 
        self._headers={'Host': 'account.xiaomi.com',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9'}        
        self._LoginByPassord()        

    @property
    def Service_Token_Cookie(self):
        return self.Service_Token

    @property
    def Login_resutl(self):
        return self.login_resutl

    @property
    def deviceIds_miai(self):
        return self.deviceIds

    def request_app_setup(self,image_name):
        """Assist user with configuring the Fitbit dev application."""
        def fitbit_configuration_callback(callback_data):
            self._serviceLoginAuth2(callback_data.get('code')) 
            if self._serviceLoginAuth2_json['code']==0:
                if not self._login_miai():
                    _LOGGER.warning('login miai Failed')
                else:
                    if not self._get_deviceId():
                        _LOGGER.warning('get_deviceId Failed')
            elif self._serviceLoginAuth2_json['code']==70016:
                _LOGGER.warning('incorrect password')
            elif self._serviceLoginAuth2_json['code']==87001:
                _LOGGER.warning('incorrect codes') 
                self._LoginByPassord()                
            else:
                _LOGGER.error(self._serviceLoginAuth2_json)    
            if self.Service_Token != None and self.deviceIds != None:
                self.login_resutl = True     

    def _LoginByPassord(self):
        if not self._get_sign():
            _LOGGER.warning("get_sign Failed")
        else:
            if not self._serviceLoginAuth2():
                _LOGGER.warning('Request Login_url Failed')
            else:
                if self._serviceLoginAuth2_json['code']==0:
                    #logon success,run self._login_miai()
                    if not self._login_miai():
                        _LOGGER.warning('login miai Failed')
                    else:
                        if not self._get_deviceId():
                            _LOGGER.warning('get_deviceId Failed')
                    if self.Service_Token != None and self.deviceIds != None:
                        self.login_resutl = True                                                
                elif self._serviceLoginAuth2_json['code']==87001:
                    self._headers['Cookie']=self._headers['Cookie']+'; pwdToken={}'.format(self._cookies['pwdToken'])
                    try:
                        current_time= int(round(time.time() * 1000))              
                        r= self._request.get('https://account.xiaomi.com/pass/getCode?icodeType=login&{}'.format(current_time),headers=self._headers,timeout=3,cookies=self._cookies,verify=False)         
                        self._cookies['ick']=self._request.cookies.get_dict()['ick'] 
                        if os.access(path+'/images',os.W_OK):
                            with open(path+'/images'+'/miai{}.jpg'.format(current_time),'wb') as f:  
                                f.write(r.content)  
                                f.close() 
                            self.request_app_setup(current_time)
                    except IOError as e:
                        _LOGGER.warning(e)
                    except BaseException as e:
                        _LOGGER.warning(e)                         
                elif self._serviceLoginAuth2_json['code']==70016:
                    _LOGGER.error('incorrect password')

    def _get_sign(self): 
        url = 'https://account.xiaomi.com/pass/serviceLogin?sid=micoapi'
        pattern = re.compile(r'_sign":"(.*?)",')
        try:            
            r = self._request.get(url,headers=self._headers,timeout=3,verify=False)
            self._cookies['pass_trace']=self._request.cookies.get_dict()['pass_trace']
            self._sign=pattern.findall(r.text)[0]
            return True
        except BaseException as e:
            _LOGGER.warning(e) 
            return False 

    def _serviceLoginAuth2(self,captCode=None):
        url='https://account.xiaomi.com/pass/serviceLoginAuth2'
        self._headers['Content-Type']='application/x-www-form-urlencoded'
        self._headers['Accept']='*/*'
        self._headers['Origin']='https://account.xiaomi.com'
        self._headers['Referer']='https://account.xiaomi.com/pass/serviceLogin?sid=micoapi'           
        self._headers['Cookie']='pass_trace={};'.format(self._cookies['pass_trace'])        

        auth_post_data={'_json':'true',
                    '_sign':self._sign,
                    'callback':'https://api.mina.mi.com/sts',
                    'hash':hashlib.md5(self._password.encode('utf-8')).hexdigest().upper(),
                    'qs':'%3Fsid%3Dmicoapi',
                    'serviceParam':'{"checkSafePhone":false}',
                    'sid':'micoapi',
                    'user':self._user}                
   
        try:
            if captCode!=None:
                url='https://account.xiaomi.com/pass/serviceLoginAuth2?_dc={}'.format(int(round(time.time() * 1000)))
                auth_post_data['captCode']=captCode                
                self._headers['Cookie']=self._headers['Cookie']+'; ick={}'.format(self._cookies['ick'])
            r= self._request.post(url,headers=self._headers,data=auth_post_data,timeout=3,cookies=self._cookies,verify=False)
            self._cookies['pwdToken']=self._request.cookies.get_dict()['passToken']
            self._serviceLoginAuth2_json=json.loads(r.text[11:])
            return True
        except BaseException as e:
            _LOGGER.warning(e)  
            return False

    def _login_miai(self):
        serviceToken = "nonce={}&{}".format(self._serviceLoginAuth2_json['nonce'],self._serviceLoginAuth2_json['ssecurity'])
        serviceToken_sha1=hashlib.sha1(serviceToken.encode('utf-8')).digest()
        base64_serviceToken = base64.b64encode(serviceToken_sha1)        
        loginmiai_header={'User-Agent': 'MISoundBox/1.4.0,iosPassportSDK/iOS-3.2.7 iOS/11.2.5','Accept-Language': 'zh-cn','Connection': 'keep-alive'}
        url=self._serviceLoginAuth2_json['location']+"&clientSign="+parse.quote(base64_serviceToken.decode())
        try:            
            r = self._request.get(url,headers=loginmiai_header,timeout=3,verify=False)
            if r.status_code==200:
                self._Service_Token=self._request.cookies.get_dict()['serviceToken']
                self.userId=self._request.cookies.get_dict()['userId']
                return True
            else:
                return False
        except BaseException as e :
            _LOGGER.warning(e)
            return False              

    def _get_deviceId(self):
        url='https://api.mina.mi.com/admin/v2/device_list?master=1&requestId=CdPhDBJMUwAhgxiUvOsKt0kwXThAvY'
        get_deviceId_header={'Cookie': 'userId={};serviceToken={}'.format(self.userId,self._Service_Token)}
        try:            
            r = self._request.get(url,headers=get_deviceId_header,timeout=3,verify=False)            
            model={"Cookie": "userId={};serviceToken={}".format(self.userId,self._Service_Token),"deviceId":json.loads(r.text)['data']}
            self.Service_Token=model['Cookie']
            self.deviceIds=model['deviceId']     
            return True                           
        except BaseException as e :
            _LOGGER.warning(e)
            return False     

    def _text_to_speech(self,text,tts_cookie,deviceIds_miai,num=0):
        try:   
            url = "https://api.mina.mi.com/remote/ubus?deviceId={}&message=%7B%22text%22%3A%22{}%22%7D&method=text_to_speech&path=mibrain&requestId={}".format(self.deviceIds_miai[num]['deviceID'],parse.quote(text),''.join(random.sample(string.ascii_letters + string.digits, 30)))
            r = self._request.post(url,headers={'Cookie':tts_cookie},timeout=10,verify=False)
            if json.loads(r.text)['message'] == 'Success':
                return True 
            elif json.loads(r.text)['error'] == 'ubus error':
                _LOGGER.error(json.loads(r.text))
            elif json.loads(r.text)['error'] == 'Unauthorized':
                _LOGGER.error(json.loads(r.text))
                self.login_resutl = False
                return False                                         
            else: 
                _LOGGER.error(json.loads(r.text)) 
                # self.login_resutl = False
                return True
        except IndexError as e:
            _LOGGER.error('你没有那个音箱！')               
        except AttributeError as e:
            _LOGGER.warning(e)
        except BaseException as e :
            _LOGGER.warning(e)
        return True      

    def player_set_volume(self,volume,tts_cookie,deviceIds_miai,num=0):
        if volume>100:
            volume=100
        elif volume<0:
            volume=0
        try:   
            url = "https://api.mina.mi.com/remote/ubus?deviceId={}&message=%7b%22volume%22%3a{}%2c%22media%22%3a%22app_ios%22%7d&method=player_set_volume&path=mediaplayer&requestId={}".format(self.deviceIds_miai[num]['deviceID'],int(volume),''.join(random.sample(string.ascii_letters + string.digits, 30)))         
            r = self._request.post(url,headers={'Cookie':tts_cookie},timeout=10,verify=False)
            if json.loads(r.text)['message'] == 'Success':
                return True
            elif json.loads(r.text)['error'] == 'ubus error':
                _LOGGER.error(json.loads(r.text))            
            elif json.loads(r.text)['error'] == 'Unauthorized':
                _LOGGER.error(json.loads(r.text))
                self.login_resutl = False
                return False                                         
            else:  
                return False
        except IndexError as e:
            _LOGGER.error('你没有那个音箱！')
            return True                
        except AttributeError as e:
            _LOGGER.warning(e)
        except BaseException as e :
            _LOGGER.warning(e)     
        return True         

    def player_play_operation(self,operation,tts_cookie,deviceIds_miai,num=0):
        try:   
            url = "https://api.mina.mi.com/remote/ubus?deviceId={}&message=%7b%22action%22%3a%22{}%22%2c%22media%22%3a%22app_ios%22%7d&method=player_play_operation&path=mediaplayer&requestId={}".format(self.deviceIds_miai[num]['deviceID'],operation,''.join(random.sample(string.ascii_letters + string.digits, 30)))         
            r = self._request.post(url,headers={'Cookie':tts_cookie},timeout=10,verify=False)
            if json.loads(r.text)['message'] == 'Success':
                return True
            elif json.loads(r.text)['error'] == 'ubus error':
                _LOGGER.error(json.loads(r.text))
            elif json.loads(r.text)['error'] == 'Unauthorized':
                _LOGGER.error(json.loads(r.text))
                self.login_resutl = False
                return False                                         
            else:  
                return False
        except IndexError as e:
            _LOGGER.error('你没有那个音箱！')              
        except AttributeError as e:
            _LOGGER.warning(e)
        except BaseException as e :
            _LOGGER.warning(e)     
        return True 
    
    def speak(self, message, index_of_speaker=0):
        self._text_to_speech(message, self.Service_Token_Cookie, self.deviceIds_miai, index_of_speaker)
