# Script to analyze the large scale training progress.
# Produces plots (and later maybe tables) as output.


from modules.training_log import TrainingLog
from config import ROOT_LIST, PLOT_PATH
import os

ROOT_LIST =["/Users/amadeus/Documents/garmin/tracks", '/Users/amadeus/Documents/Movescount/2015/']

training_log = TrainingLog(2015, ROOT_LIST)
# efforts = training_log.effort_list

training_log.plot_calendar(os.path.join(PLOT_PATH, 'training_log_{}.pdf'.format(training_log.year)))
