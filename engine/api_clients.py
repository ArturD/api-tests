import requests

def log( line ):
  import sys
  #sys.stderr.write("%s\n" % line)

class ApiClientReposnse:
  def __init__(self, success, response ):
    self.success   = success
    self.resposnse = response

  def is_success(self):
    return self.success

  def get_response(self):
    return self.response


class ApiClientBase:
  def get(self, api, action, parameters):
    url = self.build_url(api, action, parameters)
    log("fetch: %s" % url)
    response = requests.get(url)
    try:
      return response.json()
    except Exception as e:
      raise IOError( "Cannot parse json from %s ..." % response.text[0:30] )

class WikiaPhpClient(ApiClientBase):
  def __init__( self, url_root ):
    self.url_root = url_root

  def build_url( self, api, action, parameters ):
    url = "%s/wikia.php?controller=%sApi&method=get%s" % (self.url_root,api,action)
    for parameter_name in parameters:
      url += "&%s=%s" % (parameter_name, parameters[parameter_name])
    return url

class V1Client(ApiClientBase):
  def __init__( self, url_root ):
    self.url_root = url_root

  def build_url( self, api, action, parameters ):
    url = "%s/%s/%s?" % (self.url_root,api,action)
    for parameter_name in parameters:
      url += "&%s=%s" % (parameter_name, parameters[parameter_name])
    return url
