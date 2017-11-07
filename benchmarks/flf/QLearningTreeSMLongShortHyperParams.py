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
    enterLongThresh = float(params.get("enterLongThresh", "nan"))
    exitLongThresh = float(params.get("exitLongThresh", "nan"))
    enterShortThresh = float(params.get("enterLongThresh", "nan"))
    exitShortThresh = float(params.get("exitLongThresh", "nan"))
    minReverseLongThresh = float(params.get("minReverseLongThresh", "nan"))
    minReverseShortThresh = float(params.get("minReverseShortThresh", "nan"))

    #Experience filters
    # --collectRegressorStats={} --maxDistanceThresholdStdevs={:.4f} --maxExperienceZScoreThresh={:.4f}
    collectRegressorStats = True #NOTE: turn this off if you don't want to filter an experience stats
    maxDistanceThresholdStdevs = float(params.get("maxDistanceThresholdStdevs", "2.0"))
    maxExperienceZScoreThresh = float(params.get("maxExperienceZScoreThresh", "0.20")) #Note, this is really max forrest-exceeds-compliance-threshold

    reversalSig = int(params.get("reversalSig", "3"))

    #Q Reward Params
    sigma = float(params.get("sigma", "2.5625"))
    sigmaSAR = float(params.get("sigmaSAR", "52.3854"))
    gamma = float(params.get("gamma", "0.0136"))
    beta = float(params.get("beta", "1.0"))
    commissionRate = float(params.get("commissionRate", "0.00005"))
    reversalWeight0 = float(params.get("reversalWeight0", "4.54"))
    reversalWeight1 = float(params.get("reversalWeight1", "1.01"))

    #Hyper params
    maxTreeDepth = int(params.get("maxTreeDepth", "349"))
    min_samples_leaf = int(params.get("min_samples_leaf", "3"))
    min_samples_split = int(params.get("min_samples_split", "16"))
    n_estimators = int(params.get("n_estimators", "241"))

    max_features = None
    if "max_features" in params:
        max_features = int(params["max_features"])
    else:
        max_features = "auto"

    #RSI BBand args
    bbTimePeriod = int(params.get("bbTimePeriod", "10"))
    bbStdevs = float(params.get("bbStdevs", "1.67"))
    rsiDCPeriodFraction = int(params.get("rsiDCPeriodFraction", "19"))
    trendEMAPeriod = int(params.get("trendEMAPeriod", "24"))
    trendLinregPeriods = int(params.get("trendLinregPeriods", "29"))
    trendRateOfChangeLookBack = int(params.get("trendRateOfChangeLookBack", "11"))

    #Doma args
    ma1Period = int(params.get("ma1Period", "4"))
    ma2Period = int(params.get("ma2Period", "5"))
    ma1Type = int(params.get("ma1Type", "4"))  #TEMA
    ma2Type = int(params.get("ma2Type", "0")) #SMA
    stdLookback = int(params.get("stdLookback", "60"))

    #macd
    macdSlowPeriodFraction = float(params.get("macdSlowPeriodFraction", "0.05"))
    macdFastPeriodFraction = float(params.get("macdFastPeriodFraction", "0.38"))
    signalperiod = int(params.get("signalperiod", "9"))

    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects
    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --random_state=1234 --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --writeOutputToFiles=False --model=11 --trainingEpochs=1 --useSaveQSpace=False --enterLongThresh={:.4f} --exitLongThresh={:.4f} --enterShortThresh={:.4f} --exitShortThresh={:.4f} --minReverseLongThresh={:.4f} --minReverseShortThresh={:.4f} --reversalSig={:d} --maxTreeDepth={:d} --n_estimators={:d} --min_samples_leaf={:d} --min_samples_split={:d} --max_features={} --instanceOrder=0 --oob_score=False --n_jobs=-1 --warm_start=False --isSAR=False --bbTimePeriod={:d} --bbStdevs={:.2f} --rsiDCPeriodFraction={:d} --trendEMAPeriod={:d} --trendLinregPeriods={:d} --trendRateOfChangeLookBack={:d} --stdLookback={:d} --macdSlowPeriodFraction={:.2f} --macdFastPeriodFraction={:.2f} --sigma={:.4f} --sigmaSAR={:.4f} --gamma={:.4f} --beta={:.4f} --commissionRate={:.5f} --reversalWeight0={:.2f} --reversalWeight1={:.2f} --collectRegressorStats={} --maxDistanceThresholdStdevs={:.4f} --maxExperienceZScoreThresh={:.4f}'.format(experimentHome, enterLongThresh, exitLongThresh, enterShortThresh, exitShortThresh, minReverseLongThresh, minReverseShortThresh, reversalSig, maxTreeDepth, n_estimators, min_samples_leaf, min_samples_split, max_features, bbTimePeriod, bbStdevs, rsiDCPeriodFraction, trendEMAPeriod, trendLinregPeriods, trendRateOfChangeLookBack, stdLookback, macdSlowPeriodFraction, macdFastPeriodFraction, sigma, sigmaSAR, gamma, beta, commissionRate, reversalWeight0, reversalWeight1, collectRegressorStats, maxDistanceThresholdStdevs, maxExperienceZScoreThresh)
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