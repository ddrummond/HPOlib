from hyperopt import hp

space = {'enterLongThresh': hp.uniform('enterLongThresh', 0.0, 0.05),
         'exitLongThresh': hp.uniform('exitLongThresh', 0.0, 0.05)}