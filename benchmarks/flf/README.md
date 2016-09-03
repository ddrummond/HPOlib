Set up your environment before running experiments:
===================================================
Instructions taken from: https://github.com/automl/HPOlib/blob/master/INSTALL.md

virtualenv virtualHPOlib
source virtualHPOlib/bin/activate

Convert config search spaces:
----------------------------------
1. write config in hyperopt
2. convert to smac (TPE->SMAC)
3. convert to spearmint (SMAC -> Spearmint)

mkdir smac
python ~/dev/HPOlib/HPOlib/format_converter/TpeSMAC.py tpe/mySpace.py >> smac/params.pcs
python path/to/wrapping.py smac
mkdir spearmint
python path/to/hpolib/format_converter/SMACSpearmint.py >> spearmint/config.pb
python path/to/wrapping.py spearmint

Run Benchmark
----------------------------------
Now you can run your benchmark with tpe. The command (which has to be executed from HPOlib/benchmarks/myBenchmark) is

HPOlib-run -o ../../optimizers/smac/smac

HPOlib-run -o ../../optimizers/spearmint/spearmint_april2013

HPOlib-run -o ../../optimizers/tpe/hyperopt_august2013_mod

Plot Results
-----------------------------------
General Example:
HPOlib-plot SMAC smac_2_06_01-dev_23_*/smac_*.pkl TPE hyperopt_august2013_mod_23_*/hyp*.pkl SPEARMINT spearmint_april2013_mod_23_*/spear*.pkl -s `pwd`/Plots/

FLF Example:
HPOlib-plot SMAC smac_2_06_01-dev_1_*/smac_*.pkl -s `pwd`/Plots/
HPOlib-plot flf smac_2_06_01-dev_1_*/smac_*.pkl -s `pwd`/Plots/
-------------
{'status': 3, 'std': 0.0, 'instance_durations': array([ 69.918]), 'instance_results': array([-9.841764]), 'test_error': nan, 'params': OrderedDict([('-enterLongThresh', '0.020344370133324588'), ('-exitLongThresh', '0.020476588256197456')]), 'result': -9.8417639999999995, 'duration': 69.918000000000006, 'instance_status': array([3])}


