import requests
from engine.decorators import ApiTest,SimpleTest
from engine.asserts import AssertThat

@ApiTest( "Articles", "Details" )
def testGetDetails( response ):
  AssertThat(response).not_null()
  AssertThat(response).is_dict()
  AssertThat(response["items"]).equals([])
  AssertThat(response).get("items").equals([]) # same as above
  AssertThat(response["basepath"]).not_null()

@ApiTest( "Articles", "List" )
def testGetDetails( response ):
  AssertThat(response).not_null()
  AssertThat(response).is_dict()
  AssertThat(response["basepath"]).not_null()
  AssertThat(response).get("items").is_list()
  AssertThat(response).get("items.1").is_dict()
  AssertThat(response).get("items.1.ns").equals(0)

@SimpleTest( "Wikis", "List" )
def testSomeSimpleStuff():
  response = requests.get("http://wikia.com/api/v1/Wikis/List").json()
  AssertThat(response).is_dict()
  AssertThat(response).get("items").is_list()
  AssertThat(response).get("items.0").is_dict()
  AssertThat(response).get("items.0.language").equals("en")


