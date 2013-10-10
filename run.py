import traceback
import tests

from engine.decorators import ApiTest,SimpleTest
from engine.tests import ApiTestTask,SimpleTestTask
from engine.executors import SingleThreadExecutor
from engine.api_clients import WikiaPhpClient,V1Client

executor = SingleThreadExecutor()
client_map = {
    "wikia.php": WikiaPhpClient("http://callofduty.wikia.com"),
    "v1": V1Client("http://callofduty.wikia.com/api/v1"),
    "test": V1Client("http://callofduty.wikia.com/api/test"),
}

testTasks = []

for test_def in ApiTest.tests:
  versions = test_def.versions or ['wikia.php', "v1", "test"]
  for version in versions:
    client = client_map[version]
    testTasks.append( ApiTestTask( test_def.invoker, client, test_def.api, test_def.action, test_def.parameters ) )

for test_def in SimpleTest.tests:
  testTasks.append( SimpleTestTask( test_def.invoker, test_def.api, test_def.action ) )

for testResult in executor.execute(testTasks):
  if testResult.ok():
    print "%s: %s (%d assertions)" % (testResult.test, testResult.status(), len(testResult.asserts))
  else:
    print "%s: %s" % (testResult.test, testResult.status())
    if testResult.error:
      print testResult.error
      trace = traceback.extract_tb(testResult.trace,3)
      for e in trace:
        print "%s %s %s %s" % e
