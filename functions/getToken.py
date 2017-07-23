#!/usr/bin/python
import ConfigParser
import urllib
import json
import base64

admin_file='/Pedro/python/functions/admin.conf'
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.request.urlopen(get_url).read()
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        data = {}
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read()
        return json.loads(r_data)['result']

if __name__ == "__main__":
    api_key = "vB0Co7lu1WKshoZQCXATRtF8" 
    api_secert = "fe40610b9c050958fc932e9edac337f9"
    bdr = BaiduRest("9805556", api_key, api_secert)
    cf = ConfigParser.ConfigParser()
    cf.read(admin_file)
    cf.set('token','key',bdr.token_str)
    cf.write(open(admin_file,"w"))
#    print(bdr.token_str)
    print('Write token key to admin.conf successsfully !')
