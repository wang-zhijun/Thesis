#!/usr/bin/env python
from lxml import etree
from StringIO import StringIO
 
def parseBookXML(xmlFile):
	f = open(xmlFile)
	xml = f.read() 
	f.close()
	
	tree = etree.parse(StringIO(xml))

	context = etree.iterparse(StringIO(xml))
	book_dict = {}
	books = []
	for action, elem in context:
		if not elem.text:
			text = "None"
		else:
			text = elem.text
		print elem.tag + " => " + text
		book_dict[elem.tag] = text
		if elem.tag == "book":
			books.append(book_dict)
			book_dict = {}
	return books
 
if __name__ == "__main__":
    parseBookXML("example.xml")
