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
    #--model=6 --instanceOrder=0 --C=1.0 --epsilon=0.1 --gamma=0.0454 --shrinking=True --tol=1e-3 --cache_size=2000.0 --max_iter=-1
    C = float(params.get("C", "1.0"))
    epsilon = float(params.get("epsilon", "0.10"))
    gamma = float(params.get("gamma", "0.0454"))
    degree = int(params.get("degree", "3"))
    coef0 = float(params.get("coef0", "0.0"))
    shrinking = bool(params.get("shrinking", "True"))
    tol = float(params.get("tol", "1.07e-3"))
    kernel = params.get("kernel", "poly")
    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects
    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --random_state=1234 --writeOutputToFiles=False --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --useSaveQSpace=True --trainingEpochs=15 --enterLongThresh={:.4f} --exitLongThresh={:.4f} --reversalSig={:d} --model=6 --instanceOrder=0 --kernel={} --degree={:d} --coef0={:.2f} --C={:.2f} --epsilon={:.6f} --gamma={:.6f} --shrinking={} --tol={:.6f} --cache_size=5000.0 --max_iter=4000'.format(experimentHome, enterLongThresh, exitLongThresh, reversalSig, kernel, degree, coef0, C, epsilon, gamma, shrinking, tol)
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