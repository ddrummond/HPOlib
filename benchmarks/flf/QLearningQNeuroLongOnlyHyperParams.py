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
    #--nb_epoch=10 --layerCount=8 --firstLayerOutputCount=22 --learningRate=0.0001 --beta1=0.9 --beta2=0.999 --epsilon=1e-08
    nb_epoch = int(params.get("nb_epoch", "5"))
    layerCount = int(params.get("layerCount", "16"))
    firstLayerOutputCount = int(params.get("firstLayerOutputCount", "42"))
    learningRate = float(params.get("learningRate", "0.0672"))
    beta1 = float(params.get("beta1", "0.7884"))
    beta2 = float(params.get("beta2", "0.19973"))
    epsilon = float(params.get("epsilon", "0.0191431"))
    rho = float(params.get("rho", "0.95"))
    decay = float(params.get("decay", "1e-7"))
    momentum = float(params.get("momentum", "0.9"))
    nesterov = bool(params.get("nesterov", "True"))
    inputDropOutRate = float(params.get("inputDropOutRate", "0.0"))
    hiddenDropOutRate = float(params.get("hiddenDropOutRate", "0.0"))

    # **kwargs contains further information, like
    # for crossvalidation
    #    kwargs['folds'] is 1 when no cv
    #    kwargs['fold'] is the current fold. The index is zero-based
    experimentHome = os.environ['EXPERIMENT_HOME'] #/home/ddrummond/PycharmProjects
    #--model=0 --trainingBatchSize=1 --layerSizeStep=1 --nb_epoch=10 --firstLayerOutputCount=22 --learningRate=0.0001 --beta1=0.9 --beta2=0.999 --epsilon=1e-08
    cmd = r'python3 -u {:s}/tutorials/src/flf/StrategyRunner.py --random_state=1234 --writeOutputToFiles=False --inputGlobPath=tests/testData/features_reinfocement_training_*.csv --useSaveQSpace=True --trainingEpochs=15 --trainingBatchSize=15 --enterLongThresh={:.4f} --exitLongThresh={:.4f} --reversalSig={:d} --model=0 --layerSizeStep=1 --nb_epoch={:d} --layerCount={:d} --firstLayerOutputCount={:d} --learningRate={:.9f} --beta1={:.9f} --beta2={:.9f} --epsilon={:.9f} --rho={:.9f} --decay={:.9f} --momentum={:.9f} --nesterov={} --inputDropOutRate={:.9f} --hiddenDropOutRate={:.9f}'.format(experimentHome, enterLongThresh, exitLongThresh, reversalSig, nb_epoch, layerCount, firstLayerOutputCount, learningRate, beta1, beta2, epsilon, rho, decay, momentum, nesterov, inputDropOutRate, hiddenDropOutRate)
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