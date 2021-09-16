# Phafin2
Software for Phafin2 manuscript (Schink et al. )

Track intensities: Fiji script and postprocessing python script.
Usage: manually track point ROIs using Fiji using the "Add to ROI manager" function. With these ROIs, the script will measure two channels in a composite image within a defines circular ROI
Postprocessing script (locate in the root directory of the tracked data): Aligns data temporally, generates plots using seaborn


Track Macropinosome sizes:
Python script using FIJI and Trackmate:
 - Asks user to select a cell in a movie
 - Will segment vesicles in that cell and track them using Trackmate
Analysis script:
 - Will filter tracks, extract sizes of the first track time point, filter them and thn plot

