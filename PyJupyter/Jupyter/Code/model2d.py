'''
Module to work with mechanical 2D models

History:
  1/07/2018 : First version
'''

# Python 2.7 compatibility
from __future__ import print_function
from __future__ import division

# Standard module imports
import numpy as np               # Import numpy for numeric calculations
import pylab as pl               # Import pylab
import matplotlib.pyplot as plt

# Non standard imports
import calc

version = '1/7/2018'

# Marker size for active points
active_size = 1  # Size of active markers

# Dimension units
lunit = 'm'

# Define normal mode outside colaboratory
colaboratory = False

# Define plots not being interative yet
iplots = False

#########################################################################################
# EXCEPTION CODE                                                                        # 
######################################################################################### 

class model2dEx(Exception):
    # Exception Methods ----------------------------------
    def __init__(self, msg=""):
        self.msg = msg
        print("\n** model2d exception")
        print('** ' + msg)
        print("\n")    

#########################################################################################
# DRAWING CODE                                                                          # 
#########################################################################################    

def setColaboratory(flag=True):
    """
    @setColaboratory
    setColaboratory(flag=True)
    Indicates that we are in Colaboartory
    Don't return anything
    """  
    global colaboratory
    colaboratory = flag 
    # Set flag also inside the calc module
    calc.setColaboratory(flag)
    
def interactivePlots(flag=True):
    """
    ----------------------------------------------------------------
    interactivePlots(flag)
    Activates interactive plotting on Jypyter
    Requires also setting the magic '%matplotlib notebook'
    Using the optinal parameter to False, return to inline mode
    
    Optional parametres:
        flag : Set interactive mode (defaults to True)
        
    Don't return anything
    ----------------------------------------------------------------
    """
    global iplots
    iplots = flag
    calc.interactivePlots(flag)    
 
#########################################################################################
# PRINTING CODE                                                                         # 
#########################################################################################      

def printSolid(solid):
    """
    ------------------------------------
    printSolid(solid)
    Prints information about a solid
    
    Parameter:
        solid : Solid to show
        
    Don't return anything    
    ------------------------------------
    """
    passive = solid['passive']
    active = solid['active']
    
    npassive = len(passive)
    print('Solid has',npassive,'passive traces')
    if npassive:
        for i in range (0,npassive):
            print('  Trace',i,':',passive[i])
    print()
    
    nactive = len(active)
    print('Solid has',nactive,'active points')
    if nactive:
        for key in active.keys():
            print(' ',key,' : ',active[key])
    print()        
            
    nobjects = len(solid)
    if nobjects == 2:
        print('Solid has no other elements')
        print()
        return
        
    print('Other elements in solid:')    
    for key in solid.keys():
        if (key != 'passive') and (key != 'active'):
            print(' ',key,' : ',solid[key])
    print()        
    
def printModel(model):
    """
    ---------------------------------------
    printModel(model)
    Prints information about a model
    
    Parameter:
        model : Model to show
    
    Don't return anything
    ---------------------------------------
    """
    nsolid = len(model)
    if nsolid == 0:
        print('Model has no solids')
        return
    for key in model.keys():
        print('Solid','"'+key+'"','information -----------------------------')
        print()
        printSolid(model[key])
        
#########################################################################################
# ZIP/UNZIP CODE                                                                        # 
#########################################################################################       

def zipPoints(lx,ly):
    """
    -----------------------------------------------------------------------
    zipPoints(lx,ly)
    Converts two lists of x and y coordinates in a list of (x,y) tuples
    
    Parameters:
        lx : list of x coordinates
        ly : list of y coordinates
        
    Returns a list of tuples  
    -----------------------------------------------------------------------    
    """
    if len(lx) != len(ly):
        raise model2dEx('Cannot zip different size lists')
    out = []
    for x,y in zip(lx,ly):
        tup = (x,y)
        out.append(tup)
    return out
    
def unzipPoints(lpoints):
    """
    unzipPoints(list)
    Converts a lists of (x,y) tuples in two list of x and y coordinates
    
    Parameters:
        list : list of (x,y) tuples
        
    Returns two lists xlist,ylist
    """
    lx = []
    ly = []
    for element in lpoints:
        lx.append(element[0])
        ly.append(element[1])
    return lx,ly    
   
#########################################################################################
# TRANSFORM CODE                                                                        # 
######################################################################################### 

def movePoint(point,increment):
    """
    ---------------------------------------------
    movePoint(point,increment)
    moves a point 
    
    Paramterers:
           point : original point tuple
       increment : displacement tuple
        
    Returns a point (xf,yf) so that:
        xf = point(x) + increment(x)
        yf = point(y) + increment(y)
    ---------------------------------------------
    """
    return (point[0]+increment[0],point[1]+increment[1])
    
def rotatePoint(point,angle):
    """
    ---------------------------------------------
    rotatePoint(point,angle)
    rotates a point arround the (0,0) origin
    
    Paramterers:
        point : original point tuple
        angle : rotation angle (in rads)
        
    Returns the rotated point tuple
    ---------------------------------------------
    """    
    x0 = point[0]
    y0 = point[1]
    x = x0*np.cos(angle)-y0*np.sin(angle)
    y = x0*np.sin(angle)+y0*np.cos(angle)
    return (x,y)
    
def moveSolid(solid,increment):
    """
    ------------------------------------------------
    moveSolid(solid,increment)
    moves all active and pasive points of a solid 
    
    Paramterers:
           solid : original solid
       increment : displacement tuple
        
    Returns a moved solid
    ------------------------------------------------
    """    
    newSolid = {}
    for key,element in solid.items():
        if key == 'passive':
            list = []
            for trace in element:
                newTrace = []
                for point in trace:
                    newPoint = movePoint(point,increment)
                    newTrace.append(newPoint)
                list.append(newTrace)
            newSolid[key] = list    
        elif key == 'active':
            dict = {}
            for keyA,pointA in element.items():
                dict[keyA] = movePoint(pointA,increment) 
            newSolid[key] = dict    
        else:
            newSolid[key]=element
    return newSolid
    
def rotateSolid(solid,angle):
    """
    ---------------------------------------------
    rotateSolid(solid,angle)
    rotates a solid arround the (0,0) origin
    
    Paramterers:
        solid : solid to rotate 
        angle : rotation angle (in rads)
        
    Returns the rotated solid
    ---------------------------------------------
    """   
    newSolid = {}
    for key,element in solid.items():
        if key == 'passive':
            list = []
            for trace in element:
                newTrace = []
                for point in trace:
                    newPoint = rotatePoint(point,angle)
                    newTrace.append(newPoint)
                list.append(newTrace)
            newSolid[key] = list    
        elif key == 'active':
            dict = {}
            for keyA,pointA in element.items():
                dict[keyA] = rotatePoint(pointA,angle) 
            newSolid[key] = dict    
        else:
            newSolid[key]=element
    return newSolid   
    
   
#########################################################################################
# RENDERING CODE                                                                        # 
#########################################################################################    

def setLenUnit(cad):
    """
    ---------------------------------------------
    setLenUnit(cad)
    Sets the string of the dimension units
    
    Paramterer:
        cad : Name of the units
        
    Don't return anything    
    ---------------------------------------------
    """   
    global lunit
    lunit = cad    

def setMarkerSize(size):
    """
    ---------------------------------------------
    setMarkerSize(size)
    Sets the size of the active point markers
    
    Paramterer:
        size : Size of markers
        
    Don't return anything    
    ---------------------------------------------
    """
    global active_size
    active_size = size

def showSolid(solid):
    """
    -------------------------------
    showSolid(solid)
    Reders a solid image
    
    Parameter:
       solid : Solid to show
       
    Don't return anything 
    -------------------------------    
    """
    
    # ToDo: Show active element positions
    # ToDo: Show other solid elements values
    
    xlist = []
    ylist = []
    colors = []
    
    # Pasive elements
    passive = solid['passive']
    if len(passive):
        for trace in passive:
            x,y = unzipPoints(trace)
            xlist.append(x)
            ylist.append(y)   
            colors.append('blue')
     
    # Active elements
    asz = active_size 
    active = solid['active']    
    if len(active):
        for key,point in active.items():
            x = point[0]
            y = point[1]
            x = [x-asz,x    ,x+asz,x    ,x-asz]
            y = [y    ,y-asz,y    ,y+asz,y    ]
            xlist.append(x)
            ylist.append(y)
            colors.append('green')
                 
    calc.plotnn(xlist,ylist,'Solid rendering','x ('+lunit+')','y ('+lunit+')',aspect=True,colors=colors)    
    
def addModel(xlist,ylist,colors,model,lingen=[],act=True):
    """
    Adds one model to the rendering
    Internal function
    """  
    asz = active_size 
    
    for key,solid in model.items():
        passive = solid['passive']
        if len(passive):
            for trace in passive:
                x,y = unzipPoints(trace)
                xlist.append(x)
                ylist.append(y)  
                colors.append('blue')
        active = solid['active']    
        if len(active) and act:
            for key,point in active.items():
                x = point[0]
                y = point[1]
                x = [x-asz,x    ,x+asz,x    ,x-asz]
                y = [y    ,y-asz,y    ,y+asz,y    ]
                xlist.append(x)
                ylist.append(y)
                colors.append('green')            
            
    if len(lingen):
        for line in lingen:
            x=[line[0][0],line[1][0]]
            y=[line[0][1],line[1][1]]
            xlist.append(x)
            ylist.append(y)
            colors.append('red')
    
def renderModel(model,lingen=[],active=True):
    """
    --------------------------------------------------------
    renderModel(model,lingen)
    Reders a model image
    
    Required parameters:
        model : Model to show
        
    Optional parameters:    
       lingen : Generation lines
       active : Render active points (defaults to True)
       
    Don't return anything 
    --------------------------------------------------------    
    """
    
    xlist = []
    ylist = []
    colors = []
    
    addModel(xlist,ylist,colors,model,lingen,active)

    calc.plotnn(xlist,ylist,'Model rendering','x ('+lunit+')','y ('+lunit+')',aspect=True,colors=colors)     

def renderSequence(models,lines=[],active=True):
    """
    ---------------------------------------------
    renderSequence(model,lines)
    Reders an image with a sequence of models
    
    Required parameters:
        models : Lost of models to show
        
    Optional parameters:    
         lines : List of generation lines
       
    Don't return anything 
    ---------------------------------------------    
    """
    
    xlist = []
    ylist = []
    colors = []
    
    if len(lines):
        for model,line in zip(models,lines):
            addModel(xlist,ylist,colors,model,line,active)
    else:
        for model in models:
            addModel(xlist,ylist,colors,model,act=active)

    calc.plotnn(xlist,ylist,'Model rendering','x ('+lunit+')','y ('+lunit+')',aspect=True,colors=colors)     