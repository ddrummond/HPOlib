import math
import time
import subprocess
import HPOlib.benchmark_util as benchmark_util
import os

def myAlgo(params, **kwargs):
    # Params is a dict that contains the params
    # As the values are forwarded as strings you might want to convert and check them
    '''
    if not params.has_key('x'):
        raise ValueError("x is not a valid key in params")

    x = float(params["x"])

    if x < 0 or x > 3.5:
        raise ValueError("x not between 0 and 3.5: %s" % x)
     '''
    enterLongThresh = float(params.get("enterLongThresh", "0.0012742"))
    exitLongThresh = float(params.get("exitLongThresh", "0.0028681"))
    reversalSig = int(params.get("reversalSig", "3"))
    #Hyper params
    maxTreeDepth = int(params.get("maxTreeDepth", "68"))
    min_samples_leaf = int(params.get("min_samples_leaf", "5"))
    min_samples_split = int(params.get("min_samples_split", "43"))
    n_estimators = int(params.get("n_estimators", "50"))
    learningRate = float(params.get("learningRate", "1.0"))
    max_features = None
    if "max_features" in params:
        max_features = int(params["max_features"])
    else:
        max_features = "auto"
    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects
    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --random_state=1234 --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --writeOutputToFiles=False --model=4 --trainingEpochs=15 --useSaveQSpace=True --enterLongThresh={:.4f} --exitLongThresh={:.4f} --reversalSig={:d} --maxTreeDepth={:d} --n_estimators={:d} --min_samples_leaf={:d} --min_samples_split={:d} --max_features={} --n_jobs=1 --instanceOrder=0 --oob_score=False --warm_start=False --learningRate={:.8f} --instanceOrder=0'.format(experimentHome, enterLongThresh, exitLongThresh, reversalSig, maxTreeDepth, n_estimators, min_samples_leaf, min_samples_split, max_features, learningRate)
    print("DD executing command: " + cmd)
    p = subprocess.Popen([cmd], shell=True, cwd=r'{:s}/tutorials/src/'.format(experimentHome), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output, err = p.communicate()
    exitCode = p.wait()
    if exitCode != 0:
        print("Script exited with non zero value [{:d}]".format(exitCode))

    if err != None:
        print("DD stderr: " + err)

    lastLine = ""
    for line in output.splitlines():
        print("Parsing line: " + line)
        lastLine = line

    print("DD this is the lastLine: " + lastLine)
    result = float(lastLine.rstrip())
    return result

if __name__ == "__main__":
    starttime = time.time()
    # Use a library function which parses the command line call
    #parses: target_algorithm_executable --fold 0 --folds 1 --params [ [ -param1 value1 ] ]
    args, params = benchmark_util.parse_cli()
    result = myAlgo(params, **args)
    duration = time.time() - starttime
    print("Result for ParamILS: %s, %f, 1, %f, %d, %s" % ("SAT", abs(duration), result, -1, str(__file__)))