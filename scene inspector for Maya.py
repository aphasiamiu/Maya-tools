import maya.cmds as cmds
from threading import Timer

selectedItems = []
#Check the object is freeze or not
def isFreeze(name):
    if cmds.getAttr('%s.%s' %(name,'translate'))[0] == (0.0, 0.0, 0.0) and cmds.getAttr('%s.%s' %(name,'rotate'))[0] == (0.0, 0.0, 0.0)and cmds.getAttr('%s.%s' %(name,'scale'))[0] == (1.0, 1.0, 1.0):
       return True
    
    else:
        return False

# Show the list of unfreezed items in the form
def addList(*arg):
    unfreezedItems = []
    # Get a list of unfreezedItems
    for i in cmds.ls(type='transform'):
        # check if the object is freezed and ignore the hidden objects
        if isFreeze(i)!= True and cmds.getAttr('%s.%s' %(i,'visibility')):
            unfreezedItems.append(i)
    cmds.textScrollList('unfreezedItem',edit=True,removeAll=True, append= unfreezedItems)
    cmds.text('CheckMessage',edit=True,label='%s items need to be fixed' %(len(unfreezedItems),))
    cmds.rowLayout('selectionChoice',e=True,visible=True)      

# TEST: return selected items number
'''
def selectedItem(*arg):
    selectedItems
    selectedItems = cmds.textScrollList('unfreezedItem',q=True, numberOfSelectedItems = True)
'''   
# TEST: print what items are selected
def ifSelected(*arg):
    global selectedItems
    selectedItems = cmds.textScrollList('unfreezedItem',q=True, selectItem= True)

def showError():
    cmds.text('msg',e=True,label='Nothing is selected! Please try again',visible=True)
    
# TEST: freeze the
def freezeTranslation(*arg):
    if not selectedItems:
        showError()
        return 0
    for i in selectedItems:
        cmds.makeIdentity(i, apply=True, translate=True)
    cmds.text('msg',e=True,label='All the selected object have been freezed transformation',visible=True)
    t=Timer(1.5,hideMessage)
    t.start()
        
def freezeRotation(*arg):
    if not selectedItems:
        showError()
        return 0
    for i in selectedItems:
        cmds.makeIdentity(i, apply=True, rotate=True)
    cmds.text('msg',e=True,label='All the selected object have been freezed rotation',visible=True)
    t=Timer(1.5,hideMessage)
    t.start()
    
        
def freezeScale(*arg):
    if not selectedItems:
        showError()
        return 0
    for i in selectedItems:
        cmds.makeIdentity(i, apply=True, scale=True)
    cmds.text('msg',e=True,label='All the selected object have been freezed scale',visible=True)
    t=Timer(1.5,hideMessage)
    t.start()

def freezeAll(*arg):
    if not selectedItems:
        showError()
        return 0
    for i in selectedItems:
        showError()
        cmds.makeIdentity(i, apply=True, scale=True,rotate=True, translate=True)
    cmds.text('msg',e=True,label='All the selected object have been freezed',visible=True)
    t=Timer(1.5,hideMessage)
    t.start()
    
def hideMessage():
    cmds.text('msg',e=True,visible=False)
    addList()
    
def selectAll(*arg):
    for i in range(0,cmds.textScrollList('unfreezedItem',q=True,numberOfItems=True)):
        cmds.textScrollList('unfreezedItem',e=True,selectIndexedItem=i+1)
    ifSelected() 
    
def deselectAll(*arg):
    cmds.textScrollList('unfreezedItem',e=True,deselectAll=True)
    ifSelected() 
#=========================== pivot function ===================================
pivotGlobal = []
def addPivotList(*arg):
    pivotList = []
    for i in cmds.ls(type='transform'):
        if cmds.objectType( cmds.listRelatives(i))=='mesh':
            if cmds.xform(i,q=True,worldSpace=True,rotatePivot=True)!= [0,0,0]:
                print i
                print cmds.xform(i,q=True,worldSpace=True,rotatePivot=True)
                pivotList.append(i)
    cmds.textScrollList('pivotList',e=True,removeAll=True,append=pivotList)
    cmds.rowLayout('pivotItems',e=True,visible=True)
    cmds.text('pivotNum',edit=True,label='%s items need to be fixed' %(len(pivotList),)) 

def ifSelectPivot(*arg):
    global pivotGlobal
    pivotGlobal = cmds.textScrollList('pivotList',q=True, selectItem= True)
    #print pivotGlobal


def setPivot(*arg):
    if not pivotGlobal:
        print 'if called'
        cmds.text('pivotMsg',e=True,label='No items selected!')
    else:
        for i in pivotGlobal:
            cmds.xform(i,worldSpace=True,pivots=[0,0,0])
        cmds.text('pivotMsg',e=True,label='All selected itmes have reset rotate Pivot')
def hidePivotMessage():
    cmds.text('PivotMsg',e=True,visible=False)
    addPivotList
    
def selectAllPivot(*arg):
    for i in range(0,cmds.textScrollList('pivotList',q=True,numberOfItems=True)):
        cmds.textScrollList('pivotList',e=True,selectIndexedItem=i+1)
    ifSelectPivot()
    
def deselectAllPivot(*arg):
    cmds.textScrollList('pivotList',e=True,deselectAll=True)
    ifSelectPivot()         
# ======================================== Overview function =========================================================
def freezeEverything(*arg):
    for i in cmds.ls(type='transform'):
        if cmds.nodeType(cmds.listRelatives(i))=='mesh':
            print i
            cmds.makeIdentity(i, apply=True, scale=True,rotate=True, translate=True)
    cmds.text('overviewMsg',e=True,label='Everything is freezed!',visible=True)
def setAllPivot(*arg):
    for i in cmds.ls(type='transform'):
        if cmds.nodeType(cmds.listRelatives(i))=='mesh':
            cmds.xform(i,worldSpace=True,pivots=[0,0,0])   
    cmds.text('overviewMsg',e=True,label='Every pivot is centered!',visible=True)   
def deleteAll(*arg):
    for i in cmds.ls(type='transform'):
        if not cmds.ls(i):
            return
        else:
            cmds.delete(i,constructionHistory=True)
    cmds.text('overviewMsg',e=True,label='All history is deleted!',visible=True)   
# ===================================== History function ==============================================================
historyGlobal = []
def checkHistory(*arg):
    historyList = []
    for i in cmds.ls(type='transform'):
        if cmds.nodeType(cmds.listRelatives(i))=='mesh' and cmds.listHistory(i,leaf=1) !=cmds.listRelatives(i):
            # check it's history itself
            if not cmds.listRelatives(i,parent=True):
                historyList.append(i)
    cmds.textScrollList('historyList',e=True,removeAll=True,append=historyList)
    cmds.text('historyNum',e=True,label='%s items need to be fixed' %(len(historyList),))
    cmds.rowLayout('historyItems',e=True,visible=True)

def ifSelectHistory(*arg):
    global historyGlobal
    historyGlobal = cmds.textScrollList('historyList',q=True, selectItem= True)
    print historyGlobal

def selectAllHistory(*arg):
    for i in range(0,cmds.textScrollList('historyList',q=True,numberOfItems=True)):
        cmds.textScrollList('historyList',e=True,selectIndexedItem=i+1)
    ifSelectHistory()
    
def deselectAllHistory(*arg):
    cmds.textScrollList('historyList',e=True,deselectAll=True)
    ifSelectHistory()    

def deleteSelectHistory(*arg):
    if not historyGlobal:
        cmds.text('historyMsg',e=True,label='No items selected!')
    else:
        for i in historyGlobal:
            cmds.delete(i,ch=True)
            # This script may not be used?
            if cmds.listHistory(i,leaf=1) !=cmds.listRelatives(i):
                mylist = cmds.listHistory(i, leaf=1)
                mylist.remove(cmds.listRelatives)
                cmds.delete(mylist)
        cmds.text('historyMsg',e=True,label='All selected itmes have delete history')    
#-----------------------------------------------------------------------------------------------------------------------
# Create the window layout
def createWindow():
    #see if the window exist
    if cmds.window('SceneInspector', exists=True):
        cmds.deleteUI('SceneInspector')
        
    #create window
    cmds.window('SceneInspector', backgroundColor=(0.4,0.4,0.4),title='Scene Inspector version1.5')
    # use columnLayout for now
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    #mainLayout = cmds.columnLayout(backgroundColor= (0.3,0.3,0.3),rowSpacing = 10.0)
    #-------------------------------------------------------------------------------
    # Overview
    overview = cmds.columnLayout(backgroundColor=(0.3,0.3,0.3), rowSpacing = 10.0,columnAttach=["both",30],columnWidth=270)
    cmds.text(label='')
    cmds.button(backgroundColor=(0.5,0.5,0.5),label='Freeze everything',command=freezeEverything)
    cmds.button(backgroundColor=(0.5,0.5,0.5),label='set all Pivot to center',command=setAllPivot)
    cmds.button(backgroundColor=(0.5,0.5,0.5),label='delete all history',command=deleteAll)
    cmds.text('overviewMsg',label='',visible=False)
    cmds.setParent('..')
    #-------------------------------------------------------------------------------
    # freezeLayout
    freezeLayout = cmds.columnLayout(backgroundColor=(0.3,0.3,0.3), rowSpacing = 10.0,columnAttach=["both",5],columnWidth=270)
    freezeBtn = cmds.button(backgroundColor=(0.5,0.5,0.5),label='Check my scene',command=addList)
    cmds.rowLayout('selectionChoice',numberOfColumns=3,visible=False)
    cmds.text('CheckMessage',label=' ')
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='selectAll',command=selectAll)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='deselectAll',command=deselectAll)
    cmds.setParent('..')
    cmds.textScrollList('unfreezedItem',allowMultiSelection=True,selectCommand=ifSelected)
    # cmds.button(label='Number of selection', command = selectedItem)
    
    # new buttons for freeze
    cmds.rowLayout('freezeChoice',numberOfColumns=5, columnWidth5=(50,60,60,40,50))
    cmds.text(label='Freeze:')
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Translate', command = freezeTranslation)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Rotation', command = freezeRotation)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Scale', command = freezeScale)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='All', command=freezeAll)
    cmds.setParent('..')
    cmds.text('msg',visible=False)
    cmds.setParent('..')
    
  
    #-------------------------------------------------------------------------
    # Pivot Layout
    pivotLayout = cmds.columnLayout(backgroundColor=(0.3,0.3,0.3), rowSpacing = 10.0,columnAttach=["both",5],columnWidth=270)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Check Pivot',command=addPivotList)
    cmds.rowLayout('pivotItems',numberOfColumns = 3,visible=False)
    cmds.text('pivotNum',label='Anything selected?')
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='selectAll',command=selectAllPivot)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='deselectAll',command=deselectAllPivot)
    cmds.setParent('..')
    cmds.textScrollList('pivotList',allowMultiSelection=True,selectCommand=ifSelectPivot)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Set rotate Pivot',command=setPivot)
    cmds.text('pivotMsg',label='')
    cmds.setParent('..')
    cmds.setParent('..')
    #-------------------------------------------------------------------------
    # History Layout
    historyLayout = cmds.columnLayout(backgroundColor=(0.3,0.3,0.3), rowSpacing = 10.0,columnAttach=["both",5],columnWidth=270)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='Check History',command=checkHistory)
    cmds.rowLayout('historyItems',numberOfColumns = 3,visible=False)
    cmds.text('historyNum',label=' ')
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='selectAll',command=selectAllHistory)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='deselectAll',command=deselectAllHistory)
    cmds.setParent('..')
    cmds.textScrollList('historyList',allowMultiSelection=True,selectCommand=ifSelectHistory)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(backgroundColor=(0.4,0.4,0.4),label='delete history',command=deleteSelectHistory)
    cmds.text('historyMsg',label='')
    cmds.setParent('..')
    
    cmds.tabLayout( tabs, edit=True, tabLabel=((overview, 'Overview'),(freezeLayout, 'Freeze'),(pivotLayout,'Pivot'),(historyLayout, 'History'),) )
    #ShowWindow
    cmds.showWindow('SceneInspector')
    
createWindow()