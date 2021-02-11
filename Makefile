.PHONY: sim

CWD=${CURDIR}

ifeq ($(OS), Windows_NT)
VENV=.venv_windows
PYTHON=Set-ExecutionPolicy Bypass -Scope Process; py
VENVBIN=./${VENV}/Scripts
REMOVE=Remove-Item –recurse 
else ifneq ("$(wildcard /.dockerenv)","")
VENV=.venv_docker
PYTHON=python3
VENVBIN=./${VENV}/bin
REMOVE=rm -fr
else
VENV=.venv_osx
PYTHON=python3
VENVBIN=./${VENV}/bin
REMOVE=rm -fr
endif

SETUP=setup_${VENV}



sim: ${SETUP}
	${VENVBIN}/${PYTHON} robot.py sim

run:
	${PYTHON} robot.py run

${VENV}:
	${PYTHON} -m venv ${VENV}

lint:
	# From CI pipeline. We are more strict in our local check
	# --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293 
	${VENVBIN}/flake8 . --count --ignore W293,E501 --show-source --statistics --exclude venv,*/tests/pyfrc*

test: ${SETUP} lint
	${VENVBIN}/${PYTHON} robot.py test

coverage: ${SETUP} test
	${VENVBIN}/${PYTHON} robot.py coverage test

setup_${VENV}: ${VENV}
	${VENVBIN}/pip install --upgrade pip setuptools || (echo "upgrading pip/setuptools failed $$?"; exit 1)
	${VENVBIN}/pip install --pre -r ${CWD}/requirements.txt || (echo "Installing requirements.txt failed $$?"; exit 1)
	$(file > ${SETUP})

clean:
	${REMOVE} setup ${SETUP}

realclean: clean
	${REMOVE} ${VENV} 

docker: docker_build
	docker run --rm -ti -v $$(PWD):/src raptacon2021_build bash 

docker_build:
	docker build . --tag raptacon2021_build

deploy:
	${PYTHON} robot.py deploy --no-resolve --robot 10.32.0.2
