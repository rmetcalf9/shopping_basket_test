# shopping_basket_technical_test

This repository contains code for the shopping basket technical test.

## Technology Choice
Due to the 2 hour time guideline and fact this is a prototype service I have chosen to implement my Python base app. (I have previously blogged about this at https://code.metcarob.com/node/236 ) This lets me skip over setting up the testing framework and container build pipeline and quickly start writing the service specific code. This lets me quickly prototype new API's, build them and deploy them to container enviroments in very little time.

## Code produced during the test

The base app starts me off with the main structure. The following files were created solely for this test:

 - [./APIContainerPythonVersion/src/CurrencyConverter.py](./APIContainerPythonVersion/src/CurrencyConverter.py)
 - [./APIContainerPythonVersion/test/test_CurrencyConverter.py](./APIContainerPythonVersion/test/test_CurrencyConverter.py)
 - [./APIContainerPythonVersion/src/shoppingBasket.py](./APIContainerPythonVersion/src/shoppingBasket.py)
 - [./APIContainerPythonVersion/src/shoppingBasketAPI.py](./APIContainerPythonVersion/src/shoppingBasketAPI.py)
 - [./APIContainerPythonVersion/test/test_shoppingBasketAPI.py](./APIContainerPythonVersion/test/test_shoppingBasketAPI.py)
Other files came from my previously built template and may have had slight minor alterations.

## swagger.json

TODO

## Docker images

The main API image is in docker hub: https://hub.docker.com/r/metcarob/shopping_basket_test/

I also produced a tester image to preform container tests: https://hub.docker.com/r/metcarob/genericpythonapitester/


## Running tests

I have a developer machine setup (see Developer Enviroment section) but it is also possible to test and run the application in a portable way using docker.
This can be achieved by running the following command from the \APIContainerPythonVersion directory in your clone of this repo:
```
docker run --rm --mount type=bind,source=$(pwd),target=/ext_volume metcarob/genericpythonapitester:latest nosetests --exclude-dir=/ext_volume/testContainer --rednose /ext_volume/
```
If you edit code while this is running tests should automatically re-run. You need to ctrl+c to finish.



## Developer Enviroment

 - Linux based machine
 - python3 and pip
 - Install requirments from [.\APIContainerPythonVersion\src\requirements.txt] and [.\APIContainerPythonVersion\testContainer\requirements.txt]
 - EXTURL enviroment variable exits example: "http://mymachinehostname"
  
 
If you want to build the container and use the Docker test container:
 - Docker (Tested with version 17.12.0-ce)
 - git (with commit rights to repo)
 
## Running the unit tests directly

Tests can be run with the command nosetests --rednose ./test however I like to continusly run these during development and I use continous_test.sh to achieve this.

## Container tests

As this is a simple prototype with a single service unit tests covered all my use cases. It is possible to test the container by conecting it to a special test container. Instructions are in /APIContainerPythonVersion/RELEASE.md
 
