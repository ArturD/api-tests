#/usr/bin/env bash

WORKSPACE=${WROKSPACE:-.}
PYENV_HOME=$WORKSPACE/.pyenv
VE_HOME=$WORKSPACE/.ve
VIRTUALENV_URL=https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
VIRTUALENV_DIR=virtualenv-1.10.1
VIRTUALENV=$VE_HOME/$VIRTUALENV_DIR/virtualenv.py

if [ "$1" = "clean" ]; then
  echo "cleanup"
  rm -rvf $PYENV_HOME
  rm -rvf $VE_HOME
else
  if [ ! -d $VE_HOME ]; then
    mkdir $VE_HOME
    wget $VIRTUALENV_URL -O ${VE_HOME}/ve.tgz
    tar xvzf ${VE_HOME}/ve.tgz -C $VE_HOME
    chmod +x $VIRTUALENV
  fi

  if [ ! -d $PYENV_HOME ]; then
    # Create virtualenv and install necessary packages
    python $VIRTUALENV --no-site-packages --distribute $PYENV_HOME
  fi

  . $PYENV_HOME/bin/activate
  pip install requests
fi
if [ "$1" = "run" ]; then
  python run.py
fi
