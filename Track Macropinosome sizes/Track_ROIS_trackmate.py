from __future__ import division
import ij.gui.NewImage as NewImage
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.Logger as Logger
import fiji.plugin.trackmate.Spot as Spot
import fiji.plugin.trackmate.SelectionModel as SelectionModel
import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.visualization.trackscheme.TrackScheme as TrackScheme
import fiji.plugin.trackmate.visualization.PerTrackFeatureColorGenerator as PerTrackFeatureColorGenerator
import fiji.plugin.trackmate.features.ModelFeatureUpdater as ModelFeatureUpdater
import fiji.plugin.trackmate.features.track.TrackIndexAnalyzer as TrackIndexAnalyzer
import ij.plugin.Animator as Animator
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils
import fiji.plugin.trackmate.tracking.sparselap.SparseLAPTrackerFactory as SparseLAPTrackerFactory
import fiji.plugin.trackmate.tracking.oldlap.LAPTrackerFactory as LAPTrackerFactory
import fiji.plugin.trackmate.detection.ManualDetectorFactory as ManualDetectorFactory
import math
from ij import IJ
from ij import *
from ij import ImagePlus
from ij import ImageStack
from ij.measure import *
from ij.plugin import *
from ij.process import *
from ij.plugin import ChannelSplitter
from ij.measure import Measurements
from ij.plugin import ImageCalculator
from ij.plugin.frame import RoiManager
from ij.plugin import Duplicator
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.gui import Roi
from ij.gui import PointRoi
from ij.gui import OvalRoi
import math 
from java.awt import * 
from java.awt import Font
import itertools 
from ij.plugin.filter import MaximumFinder
from ij.measure import ResultsTable
import time
from ij.gui import WaitForUserDialog
import os, errno
import glob
from ij.gui import Overlay
import sys
import time
import fiji.plugin.trackmate.features.TrackFeatureCalculator as TrackFeatureCalculator
import fiji.plugin.trackmate.action.ExportStatsToIJAction as ExportStatsToIJAction
import fiji.plugin.trackmate.action.ExportAllSpotsStatsAction as ExportAllSpotsStatsAction


savepath =  "D:/Macropinosome_sizes/"
experiment = 1
genotype = "WT"


#Cleaning up the ROI manager and opening a  new one in case none is open
try:
    rm = RoiManager.getInstance()
    if rm.getCount() > 0:
        rm.runCommand("Delete");
except:
    rm = RoiManager()

#Get current image and the image title (for saving the tracking data)
imp1 = IJ.getImage()

IJ.run(imp1, "Select None", "");
filename = imp1.getTitle()

imp = Duplicator().run(imp1, 1, 1, 1, 1, 1, 61);
imp.show()
imp = IJ.getImage()
#crop image to remove deconvolution borders
IJ.run(imp, "Canvas Size...", "width=960 height=960 position=Center");
IJ.run(imp, "Enhance Contrast", "saturated=0.55")
# remove scaling from image - tracking of binary images only works reliable with pixel units
# Measuring ROI values (especially Feret's diameter) does not work reliable on calibrated data, potentially only when using TrackMate
IJ.run(imp, "Set Scale...", "distance=0 known=0 pixel=1 unit=pixel");

roi_cell = None
while roi_cell == None:
    WaitForUserDialog("Please outline a cell").show()
    roi_cell = imp.getRoi()
cell_stats = roi_cell.getStatistics()
cell_size = cell_stats.area
IJ.run(imp, "Select None", "");


IJ.run(imp, "Subtract Background...", "rolling=20 stack");
IJ.setAutoThreshold(imp, "Otsu dark no-reset");
IJ.run(imp, "Convert to Mask", "method=Otsu background=Dark calculate black");
#IJ.run(imp, "Select All", "");
IJ.run(imp, "Close-", "stack");
IJ.run(imp, "Fill Holes", "stack");
#IJ.run(imp, "Watershed", "stack");
imp.setRoi(roi_cell)
IJ.setBackgroundColor(0, 0, 0);
IJ.run(imp, "Clear Outside", "stack");
IJ.run(imp, "Select None", "");

# We just need a model for this script. Nothing else, since 
# we will do everything manually.
model = Model()
model.setLogger(Logger.IJ_LOGGER)

# Well actually, we still need a bit:
# We want to color-code the tracks by their feature, for instance 
# with the track index. But for this, we need to compute the 
# features themselves. 
#
# Manuall, this is done by declaring what features interest you
# in a settings object, and creating a ModelFeatureUpdater that 
# will listen to changes in the model, and compute the feautures
# on the fly.
settings = Settings()
settings.setFrom(imp)


settings.addTrackAnalyzer( TrackIndexAnalyzer() )
# If you want more, add more analyzers.

# The object in charge of keeping the numerical features
# up to date:
ModelFeatureUpdater( model, settings )
# Nothing more to do. When the model changes, this guy will be notified and
# recalculate all the features you declared in the settings object.

# Every manual edit to the model must be made 
# between a model.beginUpdate() and a model.endUpdate()
# call, otherwise you will mess with the event signalling
# and feature calculation.

# This actually triggers the features to be recalculated.


#Generating a binary image from the loaded image: We extract Channel1, generate ROIs and add them as new spots to the model


IJ.run(imp, "Analyze Particles...", "size=25-Infinity circularity=0.30-1.00 pixel exclude record add stack");

roinumber = RoiManager.getInstance().getCount()

model.beginUpdate()


roinumber = RoiManager.getInstance().getCount()
s1 = None



#ort0 = ResultsTable()
for roi in range(roinumber):
    RoiManager().getInstance().select(imp, roi)
    imp.setC(1)
    roi1 = imp.getRoi()
    imp.setRoi(roi1)
    name= roi
    name_1 = roi1.getName()
    stats = imp.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID | Measurements.CENTER_OF_MASS)
    x_center = stats.xCentroid
    y_center = stats.yCentroid
    area1 = stats.area



    frame =  imp.getT()
    z_pos = imp.getZ()
    feret_diam= 0
    time.sleep=0.01    
    feret_diam = roi1.getFeretValues()

    #radius= roi1.getFeretsDiameter()/2
    radius=0
    radius = ((round(feret_diam[0],3)+round(feret_diam[2],3))/4)
    """
    ort0.incrementCounter()

    ort0.addValue("ROI", str(roi))
    ort0.addValue("name", str(name_1))
    ort0.addValue("Area", str(area1))
    ort0.addValue("Time", str(int(frame)))
    ort0.addValue("Radius", str(radius))
    ort0.addValue("Feret Max", str(feret_diam[0]))
    ort0.addValue("Feret Min", str(feret_diam[2]))
    ort0.addValue("Feret0", str(feret_diam[0]))
    ort0.addValue("Feret1", str(feret_diam[1]))
    ort0.addValue("Feret2", str(feret_diam[2]))
    ort0.addValue("Feret3", str(feret_diam[3]))
    ort0.addValue("X", str(x_center))
    ort0.addValue("Y", str(y_center))
    """   
    """
    if s1 is None:
        # When you create a spot, you always have to specify its x, y, z 
        # coordinates (even if z=0 in 2D images), AND its radius, AND its
        # quality. We enforce these 5 values so as to avoid any bad surprise
        # in other TrackMate component.
        # Typically, we use negative quality values to tag spot created 
        # manually. 
        s1 = Spot(x_center, y_center, z_pos, radius, -1)
        s1.putFeature("Frame", frame)
        s1.putFeature("Area", 999)
        model.addSpotTo(s1, frame-1)

        continue
    """
    s2 = Spot(x_center, y_center, z_pos, radius, -1)
    s2.putFeature("Frame", frame)
    s2.putFeature("Area", area1)
    s2.putFeature("Name", name)
    
    model.addSpotTo(s2, frame-1)
    # You need to specify an edge cost for the link you create between two spots.
    # Again, we use negative costs to tag edges created manually.

    s1 = s2
        #model.addEdge(s1, s2, -1)
#    print x_center

#    print y_center
# So that's how you manually build a model from scratch. 
# The next lines just do more of this, to build something enjoyable.
# Commit all of this.
model.endUpdate()

#ort0.show("Spots")



settings.trackerFactory = SparseLAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 15.0
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']=15.0
settings.trackerSettings['MAX_FRAME_GAP']= 2

# Add the analyzers for some spot features.
# You need to configure TrackMate with analyzers that will generate 
# the data you need. 
# Here we just add two analyzers for spot, one that computes generic
# pixel intensity statistics (mean, max, etc...) and one that computes
# an estimate of each spot's SNR. 
# The trick here is that the second one requires the first one to be in
# place. Be aware of this kind of gotchas, and read the docs. 

trackmate = TrackMate(model, settings)
trackmate.execTracking() 
"""
ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
"""
selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)
displayer.render()
displayer.refresh()

#print model.getSpots().getNSpots(True)
#print model.getTrackModel().nTracks(True)
# Echo results with the logger we set at start:
#model.getLogger().log(str(model))
#TrackFeatureCalculator(model,settings).process()
#ExportStatsToIJAction().execute(trackmate)


fm = model.getFeatureModel()

ort = ResultsTable()   
    
for id in model.getTrackModel().trackIDs(True):
   
    # Fetch the track feature from the feature model.
    #v = fm.getTrackFeature(id, 'TRACK_MEAN_SPEED')
    #model.getLogger().log('')
    #model.getLogger().log('Track ' + str(id) + ': mean velocity = ' + str(v) + ' ' + model.getSpaceUnits() + '/' + model.getTimeUnits())
    track = model.getTrackModel().trackSpots(id)
    for spot in track:
        sid = spot.ID()
        # Fetch spot features directly from spot. 
        x=spot.getFeature('POSITION_X')
        rad = spot.getFeature("RADIUS")
        y=spot.getFeature('POSITION_Y')
        t=spot.getFeature('FRAME')
        q=spot.getFeature('QUALITY')
        area=spot.getFeature('Area')
        name2 = spot.getFeature("Name")
        snr=spot.getFeature('SNR') 
        mean=spot.getFeature('MEAN_INTENSITY')
        #model.getLogger().log('\tspot ID = ' + str(sid) + ': x='+str(x)+', y='+str(y)+', t='+str(t)+', q='+str(q) + ', snr='+str(snr) + ', mean = ' + str(mean))
        #imp1.setT(int(t+1))
        #IJ.doWand(imp1, int(x), int(y), 0.0, "Legacy");
        #stats = imp1.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
       

        ort.incrementCounter()

        ort.addValue("Track", str(id))
        ort.addValue("ID", str(sid))
        ort.addValue("Area", str(area))
        ort.addValue("Time", str(int(t)))
        ort.addValue("Radius", str(rad))
        ort.addValue("X", str(x))
        ort.addValue("Y", str(y))
        ort.addValue("Cell size", str(cell_size))
        name = RoiManager().getInstance().getName(int(name2))
        ort.addValue("Roi label", name)
        ort.addValue("Experiment", experiment)
        ort.addValue("Genotype", genotype)
ort.show("Results1")
dataname =  "Exp_"+str(experiment)+"_"+filename +".csv"
savename = savepath + dataname
ort.save(savename)
imp.changes=False

try:
    IJ.selectWindow("Results1")
    IJ.run("Close")
except:
    pass
try:
    IJ.selectWindow("Log")
    IJ.run("Close")
except:
    pass

