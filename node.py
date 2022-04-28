from multiprocessing import parent_process


class Node():
	def __init__(self,value,parent):
		self.value = value
		self.parent = parent
		self.children = []

		self.root = self.parent
		if not isinstance(self.parent,Root):
			self.root = self.parent.root

		self.id = self.root.numNodes
		self.root.numNodes += 1

		self.level = self.parent.level + 1
		if self.root.maxDepth < self.level:
			self.root.maxDepth = self.level

	def searchByValue(self,value):
		if self.value == value:
			return self
		if len(self.children) == 0:
			return None
		
		nodeFound = None
		for n in self.children:
			searchVal = n.searchByValue(value)
			if searchVal != None:
				nodeFound = searchVal
		return nodeFound

	def searchById(self,id):
		if self.id == id:
			return self
		if len(self.children) == 0:
			return None
		
		nodeFound = None
		for n in self.children:
			searchId = n.search(id)
			if searchId != None:
				nodeFound = searchId
		return nodeFound
	
	def addChild(self,value):
		child = Node(value, self)
		self.children.append(child)
		return child

	def getAllNodes(self):
		if len(self.children) == 0:
			return [self]
		nodeList = []
		for c in self.children:
			for n in c.getAllNodes():
				nodeList.append(n)
		nodeList.append(self)
		return nodeList

	def getNodesInLayer(self, targetLayer,currentLayer):
		if currentLayer == targetLayer:
			return [self]
		if len(self.children) == 0:
			return [None]
		nodeList = []
		for c in self.children:
			nextLayerList = c.getNodesInLayer(targetLayer,currentLayer+1)
			if nextLayerList != None:
				for n in c.getNodesInLayer(targetLayer,currentLayer=currentLayer+1):
					if n != None:
						nodeList.append(n)
		return nodeList
	
	
	def __str__(self):
		return "ID: {}\tValue: {}\tParentID: {}\tParentVal: {}".format(self.id,self.value,self.parent.id,self.parent.value)

class Root(Node):
	def __init__(self,value=None):
		self.value = value 
		self.parent = None
		self.children = []
		self.level = 0
		self.maxDepth = 0
		self.id=0
		self.numNodes=1
	
	def getNodesInLayer(self, targetLayer):
		if self.maxDepth < targetLayer:
			return [None]
		return super(Root,self).getNodesInLayer(targetLayer,0)

	def __str__(self):
		return "ROOT ||  Val: {}\tMaxDepth: {}\tNumNodes: {}".format(self.value,self.maxDepth,self.numNodes)


root = Root(0)
for i in range(1,5):
	root.addChild(i)
for i in range(5,8):
	root.searchByValue(4).addChild(i)

for n in root.getNodesInLayer(3):
	print(n)