import requests
BaseURL = 'http://candygram.neurology.emory.edu:8080/api/v1/'

### This is hard coded, but will pull/sync all the label and macro images for 
### the FOX collection and store it locally to allow us to test OCR

def HelloDolu( someOtherString) :
    print "HELLO DOLU!"
    print someOtherString
    print "Go Atlanta United"
    return 4


def ListItemsInGirderFolder( folderID, limit=500):
    url = BaseURL + 'item?folderId=' + folderID + ("&sort=lowerName&limit=%d&sortdir=1" % limit )
    ItemsInFolder = requests.request("GET",url).json()
    return ItemsInFolder
