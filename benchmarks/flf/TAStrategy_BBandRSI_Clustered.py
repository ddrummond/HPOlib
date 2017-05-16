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
    bbPriceType = int(params.get("bbPriceType", "1"))
    bbTimePeriod = int(params.get("bbTimePeriod", "7"))
    bbStdevs = float(params.get("bbStdevs", "1.907"))
    rsiDCPeriodFraction = int(params.get("rsiDCPeriodFraction", "9"))
    trendEMAPeriod = int(params.get("trendEMAPeriod", "55"))
    rsiOverSoldThresh = float(params.get("rsiOverSoldThresh", "31.78"))
    rsiOverBoughtThresh = float(params.get("rsiOverBoughtThresh", "68.95"))
    trendAngleThresh = float(params.get("trendAngleThresh", "9.885"))
    trendLinregPeriods = int(params.get("trendLinregPeriods", "37"))

    #Cluster args
    clusterTIPeriod = int(params.get("clusterTIPeriod", "20"))
    clusterMaxDistanceThreshold = float(params.get("clusterMaxDistanceThreshold", "0.68"))
    clusterMatchingLookbackWindow = int(params.get("clusterMatchingLookbackWindow", "40"))
    maxClusterDistance = float(params.get("maxClusterDistance", "1000.0"))

    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects

    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --writeOutputToFiles=False --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --evalMethod=TA_OPT_BY_CLUSTER --maxOptEvaluations=125 --clusterTIPeriod={:d} --clusterMaxDistanceThreshold={:.2f} --clusterMatchingLookbackWindow={:d} --maxClusterDistance={:.2f} --taStrategy=100 --bbPriceType={:d} --bbTimePeriod={:d} --bbStdevs={:.2f} --rsiDCPeriodFraction={:d} --trendEMAPeriod={:d} --rsiOverSoldThresh={:.1f} --rsiOverBoughtThresh={:.1f} --trendAngleThresh={:.1f} --trendLinregPeriods={:d}'\
        .format(experimentHome,
                clusterTIPeriod,
                clusterMaxDistanceThreshold,
                clusterMatchingLookbackWindow,
                maxClusterDistance,
                bbPriceType, bbTimePeriod, bbStdevs, rsiDCPeriodFraction, trendEMAPeriod, rsiOverSoldThresh, rsiOverBoughtThresh, trendAngleThresh, trendLinregPeriods)
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