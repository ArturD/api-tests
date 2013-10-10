import sys, traceback
from asserts import AssertScope

class TestResult():
  def __init__(self, test, asserts, error = None, trace = []):
    self.test = test
    self.asserts = asserts
    self.error = error
    self.trace = trace

  def status(self):
    if self.error:
      return "Error"
    failed = [ x for x in self.asserts if not x.success()]
    if len(failed) > 0:
      return "Failed %s/%s" % (len(failed), len(self.asserts))
    return "Ok"

  def ok(self):
    return self.status() == "Ok"

class ApiTestTask:
  def __init__(self, func, api_client, api, action, params):
    self.api_client = api_client
    self.api = api
    self.action = action
    self.params = params
    self.func = func

  def execute(self):
    with AssertScope() as scope:
      try:
        api_result = self.api_client.get(self.api,self.action,self.params)
        self.func( api_result )
        return TestResult( self, scope.asserts )
      except Exception as e:
        stack = sys.exc_info()[2]
        return TestResult( self, scope.asserts, e, stack )

  def __unicode__(self):
    return "%s::%s Test" % (self.api, self.action)

  def __str__(self):
    return self.__unicode__();

class SimpleTestTask:
  def __init__(self, func, api, action):
    self.api = api
    self.action = action
    self.func = func

  def execute(self):
    with AssertScope() as scope:
      try:
        self.func( )
        return TestResult( self, scope.asserts )
      except Exception as e:
        stack = sys.exc_info()[2]
        return TestResult( self, scope.asserts, e, stack )

  def __unicode__(self):
    return "%s::%s SimpleTest" % (self.api, self.action)

  def __str__(self):
    return self.__unicode__();
