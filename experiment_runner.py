from azureml.core import Experiment, RunConfiguration, ScriptRunConfig, Workspace, Environment
from azureml.train.dnn import TensorFlow
from azureml.core.conda_dependencies import CondaDependencies

ws = Workspace.from_config()

environment = Environment.from_existing_conda_environment(name="sentiment-env", conda_environment_name="sentiment") 
# environment = Environment.get(workspace=ws, name="AzureML-TensorFlow-2.1-GPU")
# environment = environment.clone("sentiment-env")
# conda_dep = CondaDependencies()
# conda_dep.add_conda_package("tensorflow-datasets")
# environment.python.conda_dependencies=conda_dep

estimator = TensorFlow(
    source_directory="sentiment_analysis", 
    entry_script="experiment.py", 
    compute_target="local", 
    #pip_packages=['tensorflow-datasets', 'numpy', 'azureml-dataprep[pandas,fuse]'], 
    framework_version="2.1", 
    #use_gpu=True, 
    script_params={'--n-words': 88000, '--epochs': 2},
    environment_definition=environment
    )

experiment = Experiment(workspace=ws, name="sentiment-analysis")
run = experiment.submit(config=estimator)

run.wait_for_completion(show_output=True)