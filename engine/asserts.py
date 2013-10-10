import threading

class AssertScope:
  thread_local_scope = threading.local()

  def __init__( self ):
    self.asserts = []

  @staticmethod
  def current():
    return getattr(AssertScope.thread_local_scope, "current", None)

  def __enter__( self ):
    self.prev = getattr(AssertScope.thread_local_scope, "current", None)
    AssertScope.thread_local_scope.current = self
    return self

  def __exit__( self, type, value, traceback ):
    AssertScope.thread_local_scope.current = self.prev

class AssertionResult():
  def __init__( self, success, message ):
    self._success = success
    self._message = message

  def success(self):
    return self._success

  def message(self):
    return self._message


class AssertThat:
  def __init__( self, value ):
    self.value = value

  def equals( self, value ):
    if self.value == value:
      AssertScope.current().asserts.append( AssertionResult(True, "%s" % value) )
    else:
      AssertScope.current().asserts.append( AssertionResult(False, "%s != %s" % (value, self.value)) )

  def not_equals( self, value ):
    if self.value == value:
      AssertScope.current().asserts.append( AssertionResult(False, "%s" % value) )
    else:
      AssertScope.current().asserts.append( AssertionResult(True, "%s != %s" % (value, self.value)) )

  def is_a( self, _type ):
    if isinstance( self.value, _type ):
      AssertScope.current().asserts.append( AssertionResult(True, "%s is of type %s" % (self.value, _type)) )
    else:
      AssertScope.current().asserts.append( AssertionResult(False, "%s is not of type %s" % (self.value, _type)) )

  def is_list( self ):
    return self.is_a( list )

  def is_dict( self ):
    return self.is_a( dict )

  def not_null( self ):
    self.not_equals( None )

  def get( self, path ):
    value = self.value
    parts = path.split('.')
    for el in parts:
      if value == None:
        break
      v = None
      if hasattr( value, "has_key" ) and value.has_key(el):
        v = value[el]
      elif isinstance( value, list ) and el.isdigit():
        ind = int(el)
        if len(value) > ind:
          v = value[ind]
      value = v
    return AssertThat(value)

