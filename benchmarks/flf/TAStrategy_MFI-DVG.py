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
    mfiPeriod = int(params.get("mfiPeriod", "14"))
    ma1Period = int(params.get("ma1Period", "4"))
    ma2Period = int(params.get("ma2Period", "5"))
    ma1Type = int(params.get("ma1Type", "4"))
    ma2Type = int(params.get("ma2Type", "0"))
    domaBuyThresh = float(params.get("domaBuyThresh", "0.02"))
    domaSellThresh = float(params.get("domaSellThresh", "-0.02"))
    priceReversalSig = int(params.get("priceReversalSig", "2"))
    indicatorReversalSig = int(params.get("indicatorReversalSig", "2"))
    reversalPointLookbackCount = int(params.get("reversalPointLookbackCount", "3"))

    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects
    #                                         StrategyRunner.py --random_state=1234 --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --writeOutputToFiles=True --evalMethod=TA_ManyEval --taStrategy=140 --mfiPeriod=14 --ma1Period=4 --ma2Period=5 --ma1Type=4 --ma2Type=0 --domaBuyThresh=0.02 --domaSellThresh=-0.02 --priceReversalSig=2 --indicatorReversalSig=2 --reversalPointLookbackCount=3
    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --writeOutputToFiles=False --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --evalMethod=TA_ManyTraining --taStrategy=140 --mfiPeriod={:d} --ma1Period={:d} --ma2Period={:d} --ma1Type={:d} --ma2Type={:d} --domaBuyThresh={:0.2f} --domaSellThresh={:0.2f} --priceReversalSig={:d} --indicatorReversalSig={:d} --reversalPointLookbackCount={:d}'\
        .format(experimentHome,
                mfiPeriod,
                ma1Period,
                ma2Period,
                ma1Type,
                ma2Type,
                domaBuyThresh,
                domaSellThresh,
                priceReversalSig,
                indicatorReversalSig,
                reversalPointLookbackCount)
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