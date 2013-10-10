class ApiTest:
  tests = []
  def __init__(self, api, action,  parameters = {}, versions = ["wikia.php", "v1"]):
    self.versions = versions
    self.api = api
    self.action = action
    self.parameters = parameters

  def __call__( self, f ):
    self.invoker = f
    ApiTest.tests.append( self )
    return f

  def get_api(self): return self.api
  def get_action(self): return self.actiuon
  def get_parameters(self): return self.parameters
  def get_versions(self): return self.versions

class SimpleTest:
  tests = []
  def __init__( self, api, action ):
    self.api = api
    self.action = action

  def __call__( self, f ):
    self.invoker = f
    SimpleTest.tests.append( self )
    return f

