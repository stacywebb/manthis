"""
A class which defines a composite object which can store
hieararchical dictionaries with names.

This class is same as a hiearchical dictionary, but it
provides methods to add/access/modify children by name, 
like a Composite.


Stacy E. Webb    <stacy@stacywebb.com>

"""
__author__ = "Stacy E. Webb"
__version__ = "0.8"


def normalize(val):
    """ Normalize a string so that it can be used as an attribute
    to a Python object """
    
    if val.find('-') != -1:
        val = val.replace('-','_')

    return val

def denormalize(val):
    """ De-normalize a string """
    
    if val.find('_') != -1:
        val = val.replace('_','-')

    return val


def splitLongName(longName):
    return longName.split('.')

def trimLeftLongName(longName):
    tokens = splitLongName(longName)
    return '.'.join(tokens[1:])
     
def trimRightLongName(longName):
    tokens = splitLongName(longName)
    return '.'.join(tokens[0:-1])

class SpecialDict(dict):
    """ A dictionary type which allows direct attribute
    access to its keys """

    def __getattr__(self, name):

        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self.get(name)
        else:
            # Check for denormalized name
            name = denormalize(name)
            if name in self:
                return self.get(name)
            else:
                raise AttributeError,'no attribute named %s' % name

    def __setattr__(self, name, value):

        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self:
            self[name] = value
        else:
            # Check for denormalized name
            name2 = denormalize(name)
            if name2 in self:
                self[name2] = value
            else:
                # New attribute
                self[name] = value
        
class CompositeDict(SpecialDict):
    """ A class which works like a hierarchical dictionary.
    This class is based on the Composite design-pattern """
    
    ID = 0
    
    def __init__(self, name=''):

        if name:
            self._name = name
        else:
            self._name = ''.join(('id#',str(self.__class__.ID)))
            self.__class__.ID += 1
        
        self._children = []
        # Link  back to father
        self._father = None
        self[self._name] =  SpecialDict()

    def __getattr__(self, name):

        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self.get(name)
        else:
            # Check for denormalized name
            name = denormalize(name)
            if name in self:
                return self.get(name)
            else:
                # Look in children list
                child = self.findChild(name)
                if child:
                    return child
                else:
                    attr = getattr(self[self._name], name)
                    if attr: return attr
                    
                    raise AttributeError,'no attribute named %s' % name
    
    def __setChildDict(self, child):
        """ Private method to set the dictionary of the child
        object 'child' in the internal dictionary """
        
        d = self[self._name]
        d[child.getName()] = child.getDict()

    def addChild(self, name, force=False):
        """ Add a new child 'child' with the name 'name'.
        If the optional flag 'force' is set to True, the
        child object is overwritten if it is already there.

        This function returns the child object, whether
        new or existing """
        
        if type(name) != str:
            raise ValueError, 'Argument should be a string!'
        
        child = self.getChild(name)
        if child:
            # print 'Child %s present!' % name
            # Replace it if force==True
            if force:
                index = self.getIndex(child)
                if index != -1:
                    child = self.__class__(name)
                    self._children[index] = child
                    child.setParent(self)
                    
                    self.__setChildDict(child)
            return child
        else:
            child = self.__class__(name)
            child.setParent(self)
            
            self._children.append(child)
            self.__setChildDict(child)

            return child
        
    def addChildObject(self, child):
        """ Add the child object 'child'. If it is already present,
        it is overwritten by default """
        
        currChild = self.getChild(child.getName())
        if currChild:
            index = self.getIndex(currChild)
            if index != -1:
                self._children[index] = child
                child.setParent(self)
                # Unset the existing child's parent
                currChild.setParent(None)
                del currChild
                
                self.__setChildDict(child)
        else:
            child.setParent(self)            
            self._children.append(child)
            self.__setChildDict(child)
            
    def findChild(self, name):
        """ Return the child with the given name from the tree """

        # Note - this returns the first child of the given name
        # any other children with similar names down the tree
        # is not considered.
        
        for child in self.getAllChildren():
            if child.getName() == name:
                return child

    def findChildren(self, name):
        """ Return a list of children with the given name from the tree """

        # Note: this returns a list of all the children of a given
        # name, irrespective of the depth of look-up.
        
        children = []
        
        for child in self.getAllChildren():
            if child.getName() == name:
                children.append(child)

        return children

    def getAllChildren(self):
        """ Return the list of all children of this object """
        
        l = []
        for child in self._children:
            l.append(child)
            l.extend(child.getAllChildren())
            
        return l
    
    def getAllNames(self):
        """ Returns array of all name parts """
        result = []
        node = self
        while not node.isRoot():
            result.insert(0, node.getName())
            node = node.getParent()
        result.insert(0, node.getName())
        return result
        

    def getAttribute(self, name):
        """ Return value of an attribute from the contained dictionary """
        
        return self[self._name][name]

    def getAttributeDict(self):
        """ Return dictionary of simple (non-composite) attributes """
        result = {}
        dict = self.getDict()
        for key in dict.keys():
            value = dict.get(key)
            if value.__class__.__name__ != 'SpecialDict':
                result[key] = value
        return result
    
    def getChild(self, name):
        """ Return the immediate child object with the given name """
        
        for child in self._children:
            if child.getName() == name:
                return child
    
    def getChildren(self):
        """ Return the list of immediate children of this object """
        
        return self._children

    def getDepth(self):
        depth = 0
        nowNode = self
        while not nowNode.isRoot():
            depth += 1
            nowNode = nowNode.getParent()
        return depth

    def getDict(self):
        """ Return the contained dictionary """
        
        return self[self._name]

    def getIndex(self, child):
        """ Return the index of the child ConfigInfo object 'child' """
        
        if child in self._children:
            return self._children.index(child)
        else:
            return -1

    def getLongName(self):
        result = ''
        node = self
        while not node.isRoot():
            if len(result) > 0:
                result = '.' + result
            result = node.getName() + result
            node = node.getParent()
        if len(result) > 0:
            result = '.' + result
        result = node.getName() + result
        return result

    def getName(self):
        """ Return the name of this ConfigInfo object """

        return self._name
    
    def getComponentByLongName(self, longName):
        """ Return component by its long name """
        result = None
        steps = longName.split('.')
        lastStep = steps[-1]
        currentNode = self
        for step in steps:
            currentNode = currentNode.getChild(step)
            if not currentNode:
                result = None
                break
            if step == lastStep:
                result = currentNode
        return result
            
    def getParent(self):
        """ Return the person who created me """

        return self._father

    def getProperty(self, child, key):
        """ Return the value for the property for child
        'child' with key 'key' """

        # First get the child's dictionary
        childDict = self.getInfoDict(child)
        if childDict:
            return childDict.get(key, None)
            
    def getPropertyDict(self):
        """ Return the property dictionary """
        
        d = self.getChild('__properties')
        if d:
            return d.getDict()
        else:
            return {}
    
    def getTrailingLongNamePart(self, longName):
        return self.splitLongName(longName)[-1]
    
    def insertByLongName(self, insertPath, name):
        """ Insert at 'long name' position in composite
            Assume it doesn't preexist """
        result = None
        parentLongName = trimRightLongName(insertPath)
        parentNode = self.getComponentByLongName(parentLongName)
        if parentNode:
            lastNamePart = self.getTrailingLongNamePart(insertPath)
            candidateNode = parentNode.getChild(lastNamePart)
            if candidateNode:
                raise IndexError,'node already exists %s' % insertPath
            else:
                result = parentNode.addChild(name)
        else:
            raise IndexError,'invalid path to insert position %s' % insertPath
        return result
    
    def isLeaf(self):
        """ Return whether I am a leaf component or not """
 
        # I am a leaf if I have no children
        return not self._children
 
    def isChildExists(self, name):
        """ Does child of name exist for this node """
        return self.getChild(name) != None
    
    def isNodeExists(self, longName):
        """ Check with this node exists """
        return self.getComponentByLongName(longName) != None
    
    def isRoot(self):
        """ Return whether I am a root component or not """

        # If I don't have a parent, I am root
        return not self._father
        
    def setAttribute(self, name, value):
        """ Set a name value pair in the contained dictionary """
        
        self[self._name][name] = value
        
    def setDict(self, d):
        """ Set the contained dictionary """
        
        self[self._name] = d.copy()
            
    def setName(self, name):
        """ Set the name of this ConfigInfo object to 'name' """        

        self._name = name
    
    def setParent(self, father):
        """ Set the parent object of myself """

        # This should be ideally called only once
        # by the father when creating the child :-)
        # though it is possible to change parenthood
        # when a new child is adopted in the place
        # of an existing one - in that case the existing
        # child is orphaned - see addChild and addChild2
        # methods !
        self._father = father
        
    def setProperty(self, child, key, value):
        """ Set the value for the property 'key' for
        the child 'child' to 'value' """

        # First get the child's dictionary
        childDict = self.getInfoDict(child)
        if childDict:
            childDict[key] = value    

    def visit(self, visitor):
        visitor.visit(self)
        for child in self.getChildren():
            child.visit(visitor)
        visitor.visitOver(self)

if __name__=="__main__":
    window = CompositeDict('Window')
    frame = window.addChild('Frame')
    tfield = frame.addChild('TextField')
    tfield.setAttribute('size','20')
    
    btn = frame.addChild('Button1')
    btn.setAttribute('label','Submit')

    btn = frame.addChild('Button2')
    btn.setAttribute('label','Browse')

    print window
    print window.Frame
    print window.Frame.Button1
    print window.Frame.Button2
    print window.Frame.Button1.label
    print window.Frame.Button2.label 
    
    print tfield.getLongName()
    
    print window.Frame.Button1.getDepth()