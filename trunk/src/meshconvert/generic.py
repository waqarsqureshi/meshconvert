#! /usr/bin/env python

import logging

logger=logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

class reader(object):
	indexed = False

	def __init__(self, file):
		"Opens file for reading"
		self.f = open(file, "r")
		self.lineno = 0
		self.logger=logging.getLogger(__name__)

	def getline(self):
		"Reads a line from file"
		self.lineno += 1
		line = self.f.readline()
		if (line == ""):
			raise IOError
		line = line.rstrip()
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("Reading line %d: %s" % (self.lineno, line))
		return line

class node(object):
	def __init__(self, x, y, z, label='1', color='0'):
		"Mesh node"
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.color = color
		if logger.isEnabledFor(logging.DEBUG):
			logger.debug("found node label=%s (%s,%s,%s) color=%s" % (self.label, self.x, self.y, self.z, self.color))

class indexedElement(object):
	def __init__(self, type, list, label='1', color='0'):
		"Indexed mesh element.  Vertex indices start from 1"
		self.type = type
		self.list = list
		self.label = label
		self.color = color
		if logger.isEnabledFor(logging.DEBUG):
			logger.debug("found element label=%s (%s) color=%s" % (self.label, ",".join(self.list), self.color))

