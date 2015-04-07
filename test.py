import urllib, urllib2, cookielib

cookie_jar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)

# acquire cookie
url_1 = 'http://www.bkstr.com/webapp/wcs/stores/servlet/BuybackMaterialsView?langId=-1&catalogId=10001&storeId=10051&schoolStoreId=15828'
req = urllib2.Request(url_1)
rsp = urllib2.urlopen(req)

# do POST
url_2 = 'http://www.elskling.se/timpriser'
values = dict(timpriser='2015-04-01', seomr='se0123')
data = urllib.urlencode(values)
req = urllib2.Request(url_2, data)
rsp = urllib2.urlopen(req)
content = rsp.read()

if "se1Arr"  in content:
	print "success"
#print content

startIndex = content.index("se1Arr")
print startIndex

# OUTPUT: Title:&nbsp;&nbsp;Statics & Strength of Materials for Arch (w/CD)<br />
