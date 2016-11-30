from src.parameter_classes import Paths, Tags, AlgorithmPars, SystemPars, Pars
from src import filenames
from src.liblinear_utils import write_execution_file, run_and_wait_trainpredict_for_all_shuffles
import os
import subprocess

# Build project files
subprocess.check_call('cmake -Bbuild -H.', shell=True)
os.chdir('build')
try:
    subprocess.check_output('make')
    os.chdir('../')
except:
    os.chdir('../')
    raise


train_file = '/home/allie/Documents/current/anomalyframework_python/data/input/features/' + \
             'Avenue/03_feaPCA.train'

name = os.path.splitext(os.path.basename(train_file))[0]

pars = Pars()

pars.paths = filenames.generate_all_paths(name, pars.algorithm,
                                          anomalyframework_root=pars.system.anomalyframework_root)

d = pars.paths.folders.path_to_tmp
if not os.path.isfile(d):
    os.makedirs(d)

write_execution_file(runinfo_fname=pars.paths.files.runinfo_fnames[0], train_file=train_file,
                     predict_directory=pars.paths.folders.path_to_tmp, solver_num=0,
                     c=1/pars.algorithm.lambd, window_size=pars.algorithm.window_size,
                     window_stride=pars.algorithm.window_stride, num_threads=8)

run_and_wait_trainpredict_for_all_shuffles(pars.paths.files.done_files,
                                           pars.paths.files.runinfo_fnames,
                                           pars.paths.files.verbose_fnames,
                                           os.path.join(pars.system.anomalyframework_root,
                                                        pars.system.path_to_trainpredict_relative))

# Sanity check to ensure score_anomalies did its job
summary_file = os.path.join(pars.paths.folders.path_to_tmp, 'summary.txt')
print('Summary file written to: ' + summary_file)
assert os.path.isfile(summary_file)
