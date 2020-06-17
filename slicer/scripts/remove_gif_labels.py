import sys
import click
import numpy as np
import nibabel as nib
from tqdm import tqdm


KEEP = [
    32,
    33,
    39,
    40,
    48,
    49,
    60,
    61,
    76,
    77,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    129,
    130,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    148,
    149,
    150,
    151,
    152,
    153,
    154,
    155,
    156,
    157,
    158,
    161,
    162,
    163,
    164,
    165,
    166,
    167,
    168,
    169,
    170,
    171,
    172,
    173,
    174,
    175,
    176,
    177,
    178,
    179,
    180,
    181,
    182,
    183,
    184,
    185,
    186,
    187,
    188,
    191,
    192,
    193,
    194,
    195,
    196,
    197,
    198,
    199,
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    207,
    208,
]

@click.command()
@click.argument('input-path', type=click.Path(exists=True))
@click.argument('output-path', type=click.Path())
def main(input_path, output_path):
    img = nib.load(input_path)
    data = np.asanyarray(img.dataobj)
    labels = np.unique(data)
    for label in tqdm(labels):
        if label not in KEEP:
            data[data == label] = 0
    result = nib.Nifti1Image(data, img.affine, header=img.header)
    result.to_filename(output_path)
    return 0


# To be run within Slicer
def createSegmentation(labelMapPath, colorsPath, outputPath, smoothing=0.2):
    labelMapPath = str(labelMapPath)
    colorsPath = str(colorsPath)
    outputPath = str(outputPath)
    if not outputPath.endswith('.seg.nrrd'):
        raise ValueError('Output path must end with ".seg.nrrd"')
    labelNode = loadLabelVolume(labelMapPath)
    colorNode = loadColorTable(colorsPath)
    displayNode = labelNode.GetDisplayNode()
    displayNode.SetAndObserveColorNodeID(colorNode.GetID())
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')
    logic = slicer.modules.segmentations.logic()
    logic.ImportLabelmapToSegmentationNode(labelNode, segmentationNode)
    rule = slicer.vtkBinaryLabelmapToClosedSurfaceConversionRule
    smoothingParameter = rule.GetSmoothingFactorParameterName()
    segmentation = segmentationNode.GetSegmentation()
    segmentation.SetConversionParameter(smoothingParameter, str(smoothing))
    segmentationNode.CreateClosedSurfaceRepresentation()
    saveNode(segmentationNode, outputPath)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    sys.exit(main())  # pragma: no cover
