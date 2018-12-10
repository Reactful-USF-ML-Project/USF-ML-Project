# Setup of Tensorflow & Google Cloud Platform

This guide will help you to install tensorflow and GCP so that you can get started with Machine Learning within the Google Cloud Platform.

 

## Getting Comfortable with the Terminal
All of this machine learning stuff will be run from your terminal so now is a good time to learn how to use it. I know it may seem like a lot at once but the terminal truly is the most powerful tool within your computer. You may want to look into some things like running commands and arguments, inspecting output, keyboard shortcuts, bash.

## Tensorflow
I followed [this guide](https://www.tensorflow.org/install/pip) to setup Tensorflow but there are a couple of things you should note:

  1. The guide will show you how to install Python to your system, but make sure that you use python version 2.7 as that is what GCP uses.
  2. If you run into installing tensorflow on your system you can [use a prebuilt version here](https://github.com/lakshayg/tensorflow-build)
  3. Every time that you use tensorflow you should use the virtual [env you made with virtualenv here](https://www.tensorflow.org/install/pip#2-create-a-virtual-environment-recommended)
   a. To activate it you run `source ./venv/bin/activate `
   b. I’d suggest making an alias in .bash_profile to make this easier to activate by running: `echo "alias tensor='source ~/venv/bin/activate'" >> ~/.bash_profile`


## Google Cloud Platform SDK
I followed [this guide to set up the Cloud environment](https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction) which is all in the context of a sample problem that is using machine learning for predicting income category based on United States Census Income Dataset. Here are a couple of things to note:

 1. Make sure in the top right corner that you are signed into the account that you will be using Google Cloud Platform on (i.e. not your personal account probably). All of the links are referenced according to that account and that’s the only way that you will be able to pass the first few steps.
 2. You will need to install the Cloud SDK which [has a guide here](https://cloud.google.com/sdk/docs/). I’d highly recommend using the install script: `./google-cloud-sdk/install.sh `
 3. Your terminal has things called Environment Variables which look like this `UPPERCASE_VARIABLE_NAME=path/or/value `, this allows you to have variables in your environment (i.e the terminal session that you are running all of this in) that will last only as long as your terminal session or forever if you run them with `export` in the front. You will be using a lot of this so please look into this guide.
