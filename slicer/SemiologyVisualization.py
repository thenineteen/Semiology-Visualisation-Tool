import csv
import logging
from pathlib import Path
from abc import ABC, abstractmethod

import numpy as np
import SimpleITK as sitk

import vtk, qt, ctk, slicer
import sitkUtils as su
from slicer.ScriptedLoadableModule import *


BLACK = 0, 0, 0
VERY_DARK_GRAY = 0.15, 0.15, 0.15
DARK_GRAY = 0.25, 0.25, 0.25
GRAY = 0.5, 0.5, 0.5
LIGHT_GRAY = 0.75, 0.75, 0.75
WHITE = 1, 1, 1
LEFT = 'Left'
RIGHT = 'Right'
OTHER = 'Other'

IMAGE_FILE_STEM = 'MNI_152'
# IMAGE_FILE_STEM = 'colin27_t1_tal_lin'


#
# SemiologyVisualization
#

class SemiologyVisualization(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Semiology Visualization"
    self.parent.categories = ["Epilepsy Semiology"]
    self.parent.dependencies = []
    self.parent.contributors = [
      "Fernando Pérez-García (3D Slicer Module and data processing)",
      "Ali Alim-Marvasti (data collection and processing)",
      "Gloria Romagnoli (data collection)",
      "John Duncan (supervision)",
    ]
    self.parent.helpText = """[This is the help text.]
    """
    self.parent.helpText += self.getDefaultModuleDocumentationLink(
      docPage='https://github.com/thenineteen/Semiology-Visualisation-Tool')
    self.parent.acknowledgementText = """
    University College London.
    """

#
# SemiologyVisualizationWidget
#
class SemiologyVisualizationWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    self.logic = SemiologyVisualizationLogic()
    self.logic.installRepository()
    self.parcellation = GIFParcellation(
      segmentationPath=self.logic.getGifSegmentationPath(),
      colorTablePath=self.logic.getGifTablePath(),
    )
    self.makeGUI()
    self.scoresVolumeNode = None
    self.parcellationLabelMapNode = None
    self.tableNode = None
    self.color_blind_mode = False
    slicer.semiologyVisualization = self

  def makeGUI(self):
    self.makeLoadDataButton()
    self.makeSettingsButton()
    self.makeUpdateButton()
    self.splitter = qt.QSplitter()
    self.splitter.setOrientation(qt.Qt.Vertical)
    self.layout.addWidget(self.splitter)
    self.makeSemiologiesButton()
    self.makeTableButton()

    # Add vertical spacer
    self.layout.addStretch(1)

  def makeSettingsButton(self):
    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.enabled = False
    self.settingsCollapsibleButton.text = 'Settings'

    self.settingsLayout = qt.QVBoxLayout(self.settingsCollapsibleButton)

    self.settingsTabWidget = qt.QTabWidget()
    self.settingsLayout.addWidget(self.settingsTabWidget)

    self.settingsTabWidget.addTab(self.getQuerySettingsTab(), 'Query')
    self.settingsTabWidget.addTab(self.getVisualizationSettingsTab(), 'Visualization')
    self.settingsTabWidget.addTab(self.getModuleSettingsTab(), 'Module')

    self.layout.addWidget(self.settingsCollapsibleButton)

  def getQuerySettingsTab(self):
    querySettingsWidget = qt.QWidget()
    querySettingsLayout = qt.QFormLayout(querySettingsWidget)
    querySettingsLayout.addRow('Dominant hemisphere: ', self.getDominantHemisphereLayout())
    return querySettingsWidget

  def getVisualizationSettingsTab(self):
    visualizationSettingsWidget = qt.QWidget()
    visualizationSettingsLayout = qt.QFormLayout(visualizationSettingsWidget)
    visualizationSettingsLayout.addWidget(self.getShowGIFButton())
    visualizationSettingsLayout.addRow('Show hemispheres: ', self.getHemispheresVisibleLayout())
    return visualizationSettingsWidget

  def getModuleSettingsTab(self):
    self.autoUpdateCheckBox = qt.QCheckBox()
    self.autoUpdateCheckBox.setChecked(False)
    self.autoUpdateCheckBox.toggled.connect(self.onAutoUpdateCheckBox)

    moduleSettingsWidget = qt.QWidget()
    moduleSettingsLayout = qt.QFormLayout(moduleSettingsWidget)
    moduleSettingsLayout.addRow('Auto-update: ', self.autoUpdateCheckBox)
    return moduleSettingsWidget

  def getDominantHemisphereLayout(self):
    self.leftDominantRadioButton = qt.QRadioButton('Left')
    self.rightDominantRadioButton = qt.QRadioButton('Right')
    self.unknownDominantRadioButton = qt.QRadioButton('Unknown')
    self.leftDominantRadioButton.setChecked(True)
    dominantHemisphereLayout = qt.QHBoxLayout()
    dominantHemisphereLayout.addWidget(self.leftDominantRadioButton)
    dominantHemisphereLayout.addWidget(self.rightDominantRadioButton)
    dominantHemisphereLayout.addWidget(self.unknownDominantRadioButton)
    self.leftDominantRadioButton.toggled.connect(self.onAutoUpdateButton)
    self.rightDominantRadioButton.toggled.connect(self.onAutoUpdateButton)
    self.unknownDominantRadioButton.toggled.connect(self.onAutoUpdateButton)
    return dominantHemisphereLayout

  def makeSemiologiesButton(self):
    self.semiologiesCollapsibleButton = ctk.ctkCollapsibleButton()
    self.semiologiesCollapsibleButton.enabled = False
    self.semiologiesCollapsibleButton.text = 'Semiologies'
    self.splitter.addWidget(self.semiologiesCollapsibleButton)

    semiologiesFormLayout = qt.QFormLayout(self.semiologiesCollapsibleButton)
    semiologiesFormLayout.addWidget(self.getSemiologiesWidget())

  def makeTableButton(self):
    self.tableCollapsibleButton = ctk.ctkCollapsibleButton()
    self.tableCollapsibleButton.visible = False
    self.tableCollapsibleButton.text = 'Scores'
    self.splitter.addWidget(self.tableCollapsibleButton)

    tableLayout = qt.QFormLayout(self.tableCollapsibleButton)
    self.tableView = slicer.qMRMLTableView()
    tableLayout.addWidget(self.tableView)

  def makeLoadDataButton(self):
    self.loadDataButton = qt.QPushButton('Load data')
    self.loadDataButton.clicked.connect(self.onLoadDataButton)
    self.layout.addWidget(self.loadDataButton)

  def getShowGIFButton(self):
    self.showGifButton = qt.QPushButton('Show GIF colors')
    self.showGifButton.clicked.connect(self.onshowGifButton)
    return self.showGifButton

  def getHemispheresVisibleLayout(self):
    self.showLeftHemisphereCheckBox = qt.QCheckBox('Left')
    self.showRightHemisphereCheckBox = qt.QCheckBox('Right')
    self.showLeftHemisphereCheckBox.setChecked(True)
    self.showRightHemisphereCheckBox.setChecked(True)
    showHemispheresLayout = qt.QHBoxLayout()
    showHemispheresLayout.addWidget(self.showLeftHemisphereCheckBox)
    showHemispheresLayout.addWidget(self.showRightHemisphereCheckBox)
    self.showLeftHemisphereCheckBox.toggled.connect(self.onAutoUpdateButton)
    self.showRightHemisphereCheckBox.toggled.connect(self.onAutoUpdateButton)
    return showHemispheresLayout

  def makeUpdateButton(self):
    self.updateButton = qt.QPushButton('Update')
    self.updateButton.enabled = not self.autoUpdateCheckBox.isChecked()
    self.updateButton.clicked.connect(self.updateColors)
    self.layout.addWidget(self.updateButton)

  def getSemiologiesWidget(self):
    try:
      from mega_analysis import (
        get_all_semiology_terms,
        get_possible_lateralities,
      )
    except ImportError as e:
      message = f'{e}\n\nPlease restart 3D Slicer and try again'
      slicer.util.errorDisplay(message)

    lateralitiesDict = {
      term: get_possible_lateralities(term)
      for term in get_all_semiology_terms()
    }
    self.semiologiesWidgetsDict = self.logic.getSemiologiesWidgetsDict(
      lateralitiesDict,
      self.onAutoUpdateButton,
      self.onSemiologyCheckBox,
    )
    semiologiesWidget = qt.QWidget()
    semiologiesLayout = qt.QGridLayout(semiologiesWidget)
    align_args = 1, 1, qt.Qt.AlignCenter
    iterable = enumerate(self.semiologiesWidgetsDict.items())
    for row, (semiology, widgetsDict) in iterable:
      semiologiesLayout.addWidget(widgetsDict['checkBox'], row, 0)
      for i, laterality in enumerate(('left', 'right', 'other')):
        widget = widgetsDict[f'{laterality}RadioButton']
        if widget is not None:
          semiologiesLayout.addWidget(widget, row, i + 1, *align_args)

    # https://www.learnpyqt.com/courses/adanced-ui-features/qscrollarea/
    scrollArea = qt.QScrollArea()
    scrollArea.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOn)
    scrollArea.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(semiologiesWidget)

    return scrollArea

  def getColorNode(self):
    colorNode = slicer.util.getFirstNodeByClassByName(
      'vtkMRMLColorTableNode',
      'Cividis' if self.color_blind_mode else 'Viridis',
    )
    return colorNode

  def getScoresFromGUI(self):
    from mega_analysis.semiology import Semiology, combine_semiologies
    termsAndSides = self.getSemiologyTermsAndSidesFromGUI()
    if termsAndSides is None:
      #slicer.util.messageBox('Please select a semiology')
      return
    semiologies = []
    for semiologyTerm, symptomsSide in termsAndSides:
      semiology = Semiology(
        semiologyTerm,
        symptomsSide,
        self.getDominantHemisphereFromGUI(),
      )
      semiologies.append(semiology)
    try:
      normalise = len(semiologies) > 1
      scoresDict = combine_semiologies(semiologies, normalise=normalise)
    except Exception as e:
      message = f'Error retrieving semiology information. Details:\n\n{e}'
      slicer.util.errorDisplay(message)
      scoresDict = None
      raise
    return scoresDict

  def getSemiologyTermsAndSidesFromGUI(self):
    from mega_analysis.semiology import Laterality
    termsAndSides = []
    for (semiologyTerm, widgetsDict) in self.semiologiesWidgetsDict.items():
      if not widgetsDict['checkBox'].isChecked():
        continue
      lateralitiesDict = {
        'left': Laterality.LEFT,
        'right': Laterality.RIGHT,
        'other': Laterality.NEUTRAL,
      }
      for i, laterality in enumerate(lateralitiesDict):
        widget = widgetsDict[f'{laterality}RadioButton']
        if widget is not None and widget.isChecked():
          result = semiologyTerm, lateralitiesDict[laterality]
          termsAndSides.append(result)
    termsAndSides = None if not termsAndSides else termsAndSides
    return termsAndSides

  def getDominantHemisphereFromGUI(self):
    from mega_analysis.semiology import Laterality
    if self.leftDominantRadioButton.isChecked():
      return Laterality.LEFT
    if self.rightDominantRadioButton.isChecked():
      return Laterality.RIGHT
    if self.unknownDominantRadioButton.isChecked():
      return Laterality.NEUTRAL

  # Slots
  def onSemiologyCheckBox(self):
    for widgetsDict in self.semiologiesWidgetsDict.values():
      enable = widgetsDict['checkBox'].isChecked()
      for i, laterality in enumerate(('left', 'right', 'other')):
        widget = widgetsDict[f'{laterality}RadioButton']
        if widget is not None:
          widget.setVisible(enable)
    self.onAutoUpdateButton()

  def onAutoUpdateButton(self):
    if self.autoUpdateCheckBox.isChecked():
      self.updateColors()

  def onshowGifButton(self):
    self.parcellation.setOriginalColors()

  def onSelect(self):
    # parcellationPath = Path(self.parcellationPathEdit.currentPath)
    # referencePath = Path(self.referencePathEdit.currentPath)
    # parcellationIsFile = parcellationPath.is_file()
    # referenceIsFile = referencePath.is_file()
    # if not parcellationIsFile:
    #   print(parcellationIsFile, 'does not exist')
    # if not referenceIsFile:
    #   print(referenceIsFile, 'does not exist')
    # self.applyButton.enabled = parcellationIsFile and referenceIsFile

    scoresPath = Path(self.scoresPathEdit.currentPath)
    scoresIsFile = scoresPath.is_file()
    if not scoresIsFile:
      print(scoresIsFile, 'does not exist')
    self.applyButton.enabled = scoresIsFile

  def onLoadDataButton(self):
    self.referenceVolumeNode = self.logic.loadVolume(
      self.logic.getDefaultReferencePath())
    self.parcellationLabelMapNode = self.logic.loadParcellation(
      self.logic.getDefaultParcellationPath())
    slicer.util.setSliceViewerLayers(
      label=None,
    )
    self.parcellation.load()
    self.semiologiesCollapsibleButton.enabled = True
    self.settingsCollapsibleButton.enabled = True

  def onAutoUpdateCheckBox(self):
    self.updateButton.setDisabled(self.autoUpdateCheckBox.isChecked())

  def updateColors(self):
    colorNode = self.getColorNode()
    if colorNode is None:
      slicer.util.errorDisplay('No color node is selected')
      return

    scoresDict = self.getScoresFromGUI()
    if scoresDict is None:
      return
    self.scoresVolumeNode = self.logic.getScoresVolumeNode(
      scoresDict,
      colorNode,
      self.parcellationLabelMapNode,
      self.scoresVolumeNode,
    )
    showLeft = self.showLeftHemisphereCheckBox.isChecked()
    showRight = self.showRightHemisphereCheckBox.isChecked()
    self.parcellation.setScoresColors(
      scoresDict,
      colorNode,
      BLACK if self.color_blind_mode else LIGHT_GRAY,
      showLeft=showLeft,
      showRight=showRight,
    )

    slicer.util.setSliceViewerLayers(
      foreground=self.scoresVolumeNode,
      foregroundOpacity=0,
      labelOpacity=0,
    )
    self.scoresVolumeNode.GetDisplayNode().SetInterpolate(False)
    self.logic.showForegroundScalarBar()
    self.logic.jumpToMax(self.scoresVolumeNode)
    scoresDict = self.parcellation.getScoresDictWithNames(scoresDict)
    self.tableNode = self.logic.exportToTable(self.tableNode, scoresDict)

    self.tableCollapsibleButton.visible = True
    self.logic.showTableInModuleLayout(self.tableView, self.tableNode)

    # self.logic.showTableInViewLayout(self.tableNode)

#
# SemiologyVisualizationLogic
#
class SemiologyVisualizationLogic(ScriptedLoadableModuleLogic):

  def getSemiologiesWidgetsDict(
      self,
      lateralitiesDict,
      radioButtonSlot,
      checkBoxSlot,
      ):
    from mega_analysis import Laterality
    semiologiesDict = {}
    for semiology_term, lateralities in lateralitiesDict.items():
      checkBox = qt.QCheckBox(semiology_term)
      checkBox.toggled.connect(checkBoxSlot)
      buttonGroup = qt.QButtonGroup()

      leftRadioButton = qt.QRadioButton('Left')
      leftRadioButton.clicked.connect(radioButtonSlot)
      leftRadioButton.setVisible(False)
      buttonGroup.addButton(leftRadioButton)

      rightRadioButton = qt.QRadioButton('Right')
      rightRadioButton.clicked.connect(radioButtonSlot)
      rightRadioButton.setVisible(False)
      buttonGroup.addButton(rightRadioButton)

      otherRadioButton = qt.QRadioButton('Other')
      otherRadioButton.clicked.connect(radioButtonSlot)
      otherRadioButton.setVisible(False)
      buttonGroup.addButton(otherRadioButton)

      semiologiesDict[semiology_term] = dict(
        checkBox=checkBox,
        leftRadioButton=leftRadioButton if Laterality.LEFT in lateralities else None,
        rightRadioButton=rightRadioButton if Laterality.RIGHT in lateralities else None,
        otherRadioButton=otherRadioButton if Laterality.NEUTRAL in lateralities else None,
        buttonGroup=buttonGroup,
      )
    return semiologiesDict

  def loadVolume(self, imagePath):
    stem = Path(imagePath).name.split('.')[0]
    try:
      volumeNode = slicer.util.getNode(stem)
    except slicer.util.MRMLNodeNotFoundException:
      volumeNode = slicer.util.loadVolume(str(imagePath))
    return volumeNode

  def loadParcellation(self, imagePath, gifVersion=None):
    stem = Path(imagePath).name.split('.')[0]
    try:
      volumeNode = slicer.util.getNode(stem)
    except Exception as e:  # slicer.util.MRMLNodeNotFoundException:
      print(e)
      volumeNode = slicer.util.loadLabelVolume(str(imagePath))
      colorNode = self.getGifColorNode(version=gifVersion)
      displayNode = volumeNode.GetDisplayNode()
      displayNode.SetAndObserveColorNodeID(colorNode.GetID())
    return volumeNode

  def getGifTablePath(self, version=None):
    version = 3 if version is None else version
    colorDir = self.getResourcesDir() / 'Color'
    filename = f'BrainAnatomyLabelsV{version}_0.txt'
    colorPath = colorDir / filename
    return colorPath

  def getGifSegmentationPath(self):
    return self.getImagesDir() / f'{IMAGE_FILE_STEM}_gif_cerebrum.seg.nrrd'

  def getGifColorNode(self, version=None):
    colorPath = self.getGifTablePath(version=version)
    colorNodeName = colorPath.stem
    className = 'vtkMRMLColorTableNode'
    colorNode = slicer.util.getFirstNodeByClassByName(className, colorNodeName)
    if colorNode is None:
      colorNode = slicer.util.loadColorTable(str(colorPath))
    return colorNode

  def getGifSegmentationNode(self):
    return slicer.util.loadSegmentation(str(self.getGifSegmentationPath()))

  def getResourcesDir(self):
    moduleDir = Path(slicer.util.modulePath(self.moduleName)).parent
    resourcesDir = moduleDir / 'Resources'
    return resourcesDir

  def getImagesDir(self):
    return self.getResourcesDir() / 'Image'

  def getDefaultReferencePath(self):
    return self.getImagesDir() / f'{IMAGE_FILE_STEM}_mri.nii.gz'

  def getDefaultParcellationPath(self):
    return self.getImagesDir() / f'{IMAGE_FILE_STEM}_gif.nii.gz'

  def getScoresVolumeNode(
      self,
      scoresDict,
      colorNode,
      parcellationLabelMapNode,
      outputNode,
      ):
    """Create a scalar volume node so that the colorbar is correct."""
    parcellationImage = su.PullVolumeFromSlicer(parcellationLabelMapNode)
    parcellationArray = sitk.GetArrayViewFromImage(parcellationImage)
    scoresArray = np.zeros_like(parcellationArray, np.float)

    if scoresDict is not None:
      for (label, score) in scoresDict.items():
        label = int(label)
        score = float(score)
        labelMask = parcellationArray == label
        scoresArray[labelMask] = score

    scoresImage = self.getImageFromArray(scoresArray, parcellationImage)
    scoresName = 'Scores'
    scoresVolumeNode = su.PushVolumeToSlicer(
      scoresImage,
      name=scoresName,
      targetNode=outputNode,
    )
    displayNode = scoresVolumeNode.GetDisplayNode()
    displayNode.SetAutoThreshold(False)
    displayNode.SetAndObserveColorNodeID(colorNode.GetID())
    displayNode.SetLowerThreshold(1)
    displayNode.ApplyThresholdOn()
    displayNode.SetAutoWindowLevel(False)
    windowMin = scoresArray[scoresArray > 0].min() if scoresArray.any() else 0
    windowMax = scoresArray.max()
    displayNode.SetWindowLevelMinMax(windowMin, windowMax)
    return scoresVolumeNode

  def getImageFromArray(self, array, referenceImage):
    image = sitk.GetImageFromArray(array)
    image.SetDirection(referenceImage.GetDirection())
    image.SetOrigin(referenceImage.GetOrigin())
    image.SetSpacing(referenceImage.GetSpacing())
    return image

  def readScores(self, scoresPath):
    with open(scoresPath) as csvfile:
      reader = csv.reader(csvfile)
      next(reader)  # assume there is a header row
      scoresDict = {int(label): float(score) for (label, score) in reader}
    return scoresDict

  def getTestScores(self):
    scoresPath = self.getResourcesDir() / 'Test' / 'head.csv'
    return self.readScores(scoresPath)

  def removeColorMaps(self):
    for colorNode in slicer.util.getNodesByClass('vtkMRMLColorTableNode'):
      if colorNode.GetName() not in COLORMAPS:
        slicer.mrmlScene.RemoveNode(colorNode)

  def installRepository(self):
    repoDir = Path(__file__).parent.parent
    import sys
    sys.path.insert(0, str(repoDir))
    try:
      import mega_analysis
    except ImportError:
      requirementsPath = repoDir / 'requirements.txt'
      slicer.util.pip_install(
        f'-r {requirementsPath}'
      )
    import matplotlib
    matplotlib.use('agg')

  def showForegroundScalarBar(self):
    qt.QSettings().setValue('DataProbe/sliceViewAnnotations.scalarBarEnabled', 1)
    qt.QSettings().setValue('DataProbe/sliceViewAnnotations.scalarBarSelectedLayer', 'foreground')
    import DataProbeLib
    DataProbeLib.SliceAnnotations().updateSliceViewFromGUI()

  def exportToTable(self, tableNode, scoresDict):
    if tableNode is None:
      tableNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode')
    tableWasModified = tableNode.StartModify()
    tableNode.RemoveAllColumns()
    # Sort from large to small and remove zeros
    scoresDict = {
      k: v
      for k, v
      in sorted(scoresDict.items(), key=lambda item: item[1], reverse=True)
      if v > 0
    }
    structuresColumn = tableNode.AddColumn(vtk.vtkStringArray())
    structuresColumn.SetName('Structure')
    scoresColumn = tableNode.AddColumn(vtk.vtkDoubleArray())
    scoresColumn.SetName('Score')

    # Fill columns
    table = tableNode.GetTable()
    for label, score in scoresDict.items():
        rowIndex = tableNode.AddEmptyRow()
        table.GetColumn(0).SetValue(rowIndex, str(label))
        table.GetColumn(1).SetValue(rowIndex, score)
    tableNode.Modified()
    tableNode.EndModify(tableWasModified)
    return tableNode

  def showTableInModuleLayout(self, tableView, tableNode):
    tableView.setMRMLTableNode(tableNode)
    tableView.show()

  def showTableInViewLayout(self, tableNode):
    currentLayout = slicer.app.layoutManager().layout
    tablesLogic = slicer.modules.tables.logic()
    appLogic = slicer.app.applicationLogic()

    layoutWithTable = tablesLogic.GetLayoutWithTable(currentLayout)
    slicer.app.layoutManager().setLayout(layoutWithTable)
    appLogic.GetSelectionNode().SetActiveTableID(tableNode.GetID())
    appLogic.PropagateTableSelection()

  def jumpToMax(self, volumeNode):
    array = slicer.util.array(volumeNode.GetID())
    maxIndices = np.array(np.where(array == array.max())).T
    meanMaxIdx = maxIndices.mean(axis=0)[::-1].astype(np.uint16).tolist()  # numpy to sitk
    image = su.PullVolumeFromSlicer(volumeNode)
    point = image.TransformContinuousIndexToPhysicalPoint(meanMaxIdx)
    point = np.array(point)
    point[:2] *= -1  # LPS to RAS
    self.jumpSlices(point)

  def jumpSlices(self, center):
    colors = 'Yellow', 'Green', 'Red'
    for (color, offset) in zip(colors, center):
      sliceLogic = slicer.app.layoutManager().sliceWidget(color).sliceLogic()
      sliceLogic.SetSliceOffset(offset)


class SemiologyVisualizationTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_SemiologyVisualization1()

  def test_SemiologyVisualization1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767',
      checksums='SHA256:12d17fba4f2e1f1a843f0757366f28c3f3e1a8bb38836f0de2a32bb1cd476560')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = SemiologyVisualizationLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')


class Parcellation(ABC):
  def __init__(self, segmentationPath):
    self.segmentationPath = Path(segmentationPath)
    self.segmentationNode = None
    self._labelMap = None

  # @property
  # def label_map(self):
  #   if self._labelMap is None:
  #     self._labelMap = sitk.ReadImage(str(self.parcellation_path))
  #     if 'float' in self._labelMap.GetPixelIDTypeAsString():
  #       self._labelMap = sitk.Cast(self._labelMap, sitk.sitkUInt16)
  #   return self._labelMap

  # Note that @property must come before @abstractmethod
  @property
  @abstractmethod
  def colorTable(self):
    pass

  @property
  def segmentation(self):
    return self.segmentationNode.GetSegmentation()

  def getSegmentIDs(self):
    stringArray = vtk.vtkStringArray()
    self.segmentation.GetSegmentIDs(stringArray)
    segmentIDs = [
        stringArray.GetValue(n)
        for n in range(stringArray.GetNumberOfValues())
    ]
    return segmentIDs

  def getSegments(self):
    return [self.segmentation.GetSegment(x) for x in self.getSegmentIDs()]

  def load(self):
    stem = self.segmentationPath.name.split('.')[0]
    try:
      node = slicer.util.getNode(stem)
      logging.info(f'Segmentation found in scene: {stem}')
    except slicer.util.MRMLNodeNotFoundException:
      logging.info(f'Segmentation not found in scene: {stem}')
      node = slicer.util.loadSegmentation(str(self.segmentationPath))
    self.segmentationNode = node
    self.segmentationNode.GetDisplayNode().SetOpacity2DFill(1)

  def isValidNumber(self, number):
    return self.colorTable.isValidNumber(number)

  def getColorFromName(self, name):
    return self.colorTable.getColorFromName(name)

  def getColorFromSegment(self, segment):
    return self.getColorFromName(segment.GetName())

  def getLabelFromName(self, name):
    return self.colorTable.getLabelFromName(name)

  def getLabelFromSegment(self, segment):
    return self.getLabelFromName(segment.GetName())

  def setOriginalColors(self):
    segments = self.getSegments()
    numSegments = len(segments)
    progressDialog = slicer.util.createProgressDialog(
      value=0,
      maximum=numSegments,
      windowTitle='Setting colors...',
    )
    for i, segment in enumerate(segments):
      progressDialog.setValue(i)
      progressDialog.setLabelText(segment.GetName())
      slicer.app.processEvents()
      color = self.getColorFromSegment(segment)
      segment.SetColor(color)
      self.setSegmentOpacity(segment, 1, dimension=2)
      self.setSegmentOpacity(segment, 1, dimension=3)
    progressDialog.setValue(numSegments)
    slicer.app.processEvents()
    progressDialog.close()

  def setScoresColors(
      self,
      scoresDict,
      colorNode,
      defaultColor,
      showLeft=True,
      showRight=True,
      ):
    segments = self.getSegments()
    numSegments = len(segments)
    progressDialog = slicer.util.createProgressDialog(
      value=0,
      maximum=numSegments,
      windowTitle='Setting colors...',
    )
    for i, segment in enumerate(segments):
      progressDialog.setValue(i)
      progressDialog.setLabelText(segment.GetName())
      slicer.app.processEvents()
      label = self.getLabelFromSegment(segment)
      if scoresDict is not None:
        scores = np.array(list(scoresDict.values()))
        positiveScores = scores[scores > 0]  # do I want this?
        minScore = min(scores)
        maxScore = max(scores)
      color = defaultColor
      opacity2D = 0
      opacity3D = 1
      if scoresDict is not None and label in scoresDict:
        score = scoresDict[label]
        if score > 0:
          opacity2D = 1
          opacity3D = 1
          normalizedScore = score - minScore
          normalizedScore /= (maxScore - minScore)
          color = self.getColorFromScore(normalizedScore, colorNode)
      if not showLeft and 'Left' in segment.GetName():
        opacity3D = 0
      if not showRight and 'Right' in segment.GetName():
        opacity3D = 0
      segment.SetColor(color)
      self.setSegmentOpacity(segment, opacity2D, dimension=2)
      self.setSegmentOpacity(segment, opacity3D, dimension=3)
    progressDialog.setValue(numSegments)
    slicer.app.processEvents()
    progressDialog.close()

  def getColorFromScore(self, normalizedScore, colorNode):
    """This method is very important"""
    numColors = colorNode.GetNumberOfColors()
    scoreIndex = int((numColors - 1) * normalizedScore)
    colorAlpha = 4 * [0]
    colorNode.GetColor(scoreIndex, colorAlpha)
    color = np.array(colorAlpha[:3])
    return color

  def setRandomColors(self):
    """For debugging purposes"""
    segments = self.getSegments()
    numSegments = len(segments)
    progressDialog = slicer.util.createProgressDialog(
        value=0,
        maximum=numSegments,
        windowTitle='Setting colors...',
    )
    for i, segment in enumerate(segments):
      progressDialog.setValue(i)
      slicer.app.processEvents()
      color = self.getRandomColor()
      segment.SetColor(color)
    progressDialog.setValue(numSegments)
    slicer.app.processEvents()
    progressDialog.close()

  def getRandomColor(self, normalized=True):
    return np.random.rand(3)

  def setSegmentOpacity(self, segment, opacity, dimension):
    displayNode = self.segmentationNode.GetDisplayNode()
    if dimension == 2:
      displayNode.SetSegmentOpacity2DFill(segment.GetName(), opacity)
      displayNode.SetSegmentOpacity2DOutline(segment.GetName(), opacity)
    elif dimension == 3:
      displayNode.SetSegmentOpacity3D(segment.GetName(), opacity)

  def getNameFromLabel(self, label):
    return self.colorTable.getStructureNameFromLabelNumber(label)

  def getScoresDictWithNames(self, scoresDict):
    return {self.getNameFromLabel(k): v for k, v in scoresDict.items()}


class GIFParcellation(Parcellation):
  def __init__(self, segmentationPath, colorTablePath):
    Parcellation.__init__(self, segmentationPath)
    self.colorTablePath = colorTablePath
    self._colorTable = None

  @property
  def colorTable(self):
    return self._colorTable

  def load(self):
    super().load()
    self._colorTable = GIFColorTable(self.colorTablePath)


class ColorTable(ABC):
  def __init__(self, path):
    self.structuresDict = self.readColorTable(path)

  def getStructureNameFromLabelNumber(self, labelNumber):
    return self.structuresDict[labelNumber]['name']

  def isValidNumber(self, number):
    return number in self.structuresDict

  @staticmethod
  def readColorTable(path):
    structuresDict = {}
    with open(path) as f:
      for row in f:
        label, name, *color, _ = row.split()
        label = int(label)
        color = np.array(color, dtype=np.float) / 255
        structuresDict[label] = dict(name=name, color=color)
    return structuresDict

  def getColorFromName(self, name):
    for structureDict in self.structuresDict.values():
      if structureDict['name'] == name:
        color = structureDict['color']
        break
    else:
      raise KeyError(f'Structure {name} not found in color table')
    return color

  def getLabelFromName(self, name):
    for label, structureDict in self.structuresDict.items():
      if structureDict['name'] == name:
        result = label
        break
    else:
      raise KeyError(f'Structure {name} not found in color table')
    return result


class GIFColorTable(ColorTable):
  pass


COLORMAPS = [
  'Cividis',
  'Plasma',
  'Viridis',
  'Magma',
  'Inferno',
  'Grey',
  'Red',
  'Green',
  'Blue',
  'Yellow',
  'Cyan',
  'Magenta',
]
