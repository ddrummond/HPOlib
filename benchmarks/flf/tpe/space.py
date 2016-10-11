from hyperopt import hp

space = {'enterLongThresh': hp.uniform('enterLongThresh', 0.0, 0.03),
         'exitLongThresh': hp.uniform('exitLongThresh', 0.0, 0.03),
         'reversalSig': hp.uniform('reversalSig', 1, 5)}