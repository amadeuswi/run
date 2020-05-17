# Script to analyze the large scale training progress.
# Produces plots (and later maybe tables) as output.


from modules.training_log import TrainingLog
from config import ROOT_LIST, PLOT_PATH
import os

training_log = TrainingLog(2020, ROOT_LIST)
training_log.plot_calendar(os.path.join(PLOT_PATH, 'training_log_{}.pdf'.format(training_log.year)))
