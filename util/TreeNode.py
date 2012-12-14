'''
Created on December 14, 2012

@author: stacywebb
'''

class TreeNodeField(dict):
    def __init__(self, name):
        self._name = name
        self._content = None
        
    def name(self):
        return self._name
    
    def content(self):
        return self._content
    
    def set_property(self, attrname, attrvalue):
        self.__setitem__(attrname, attrvalue)
        
    def set_content(self, content):
        self._content = content
        
    def __str__(self):
        result = self._name 
        if self._content == None:
            result += '[<None>]'
        else:
            result += '[' + str(self._content) + ']'
        result += super(dict, self).__str__()
        return result

class TreeNodeFactory(object):
    '''
    Creates a TreeNode
    '''
    
    def __init__(self, name, fieldnames=[]):
        self.name = name
        self.fields = [TreeNodeField(fieldname) for fieldname in fieldnames]
        
    def addFieldDefinition(self, tnField):
        self.fields.append(tnField)   
        
    def create(self, treeNodeName):
        return TreeNode(self.name, self.fields, treeNodeName)
    
    def __str__(self):
        result = 'Factory ' + self.name + '['
        result += ', '.join([str(field) for field in self.fields])
        result += ']'
        return result


class TreeNode(object):
    '''
    TreeNode is a composite node
    '''
    def __init__(self, typeName, name, fields):
        self.parent = None
        self.children = []
        
        self.typeName = typeName
        self.name = name
        
        self.valueDict = dict()

        self.fields = fields
        
        
    def addChild(self, treeNode):
        treeNode.parent = self
        self.children.append(treeNode)
        return treeNode
    
    def delete(self):
        self.parent.children.remove(self)
        
    def depth(self):
        depth = 0
        now = self
        while now != None:
            depth += 1
            now = now.parent
        return depth
     
    def fqn(self):
        result = ""
        now = self
        while now != None:
            if len(result) > 0:
                result = '.' + result
            result = self.name + result
            now = now.parent
        return result
        
    def insertChild(self, i, treeNode):
        treeNode.parent = self
        self.chidren.insert(treeNode)
        return treeNode
    
    
