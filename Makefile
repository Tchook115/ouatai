

### GCP configuration - - - - - - - - - - - - - - - - - - -
# /!\ you should fill these according to your account
### GCP Project - - - - - - - - - - - - - - - - - - - - - -

# not required here
### GCP Storage - - - - - - - - - - - - - - - - - - - - - -
BUCKET_NAME=wagon-data-677-bernard
##### Data  - - - - - - - - - - - - - - - - - - - - - - - -
BUCKET_TRAIN_DATA_RAW = quickdraw_dataset
##### Training  - - - - - - - - - - - - - - - - - - - - - -
# will store the packages uploaded to GCP for the training
BUCKET_TRAINING_FOLDER = 'trainings'
##### Model - - - - - - - - - - - - - - - - - - - - - - - -
# not required here
### GCP AI Platform - - - - - - - - - - - - - - - - - - - -
##### Machine configuration - - - - - - - - - - - - - - - -
REGION=europe-west1

PYTHON_VERSION=3.7
FRAMEWORK=TensorFlow
RUNTIME_VERSION=2.5

##### Package params  - - - - - - - - - - - - - - - - - - -
PACKAGE_NAME=ouatai
TRAINING_FILENAME=trainer
ILLUSTRATOR_FILENAME= illustrator

##### Job - - - - - - - - - - - - - - - - - - - - - - - - -

JOB_NAME=ouatai_pipeline_$(shell date +'%Y%m%d_%H%M%S')

run_locally:
	@python -m ${PACKAGE_NAME}.${TRAINING_FILENAME}

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${TRAINING_FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs \
		--scale-tier=BASIC_GPU
		#--master-machine-type=a2-highgpu-1g \
		#--acceleratorConfig=NVIDIA_TESLA_A100

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ __pycache__
	@rm -fr build dist *.dist-info *.egg-info
	@rm -fr */*.pyc


run_api:
	uvicorn API.api:app --reload  # load web server with code autoreload

run_local_illustration:
	@python -m ${PACKAGE_NAME}.${ILLUSTRATOR_FILENAME}

run_rasa:
	cd ./rasa_ouatai && rasa run -m models --enable-api

run_rasa_action:
	cd ./rasa_ouatai && rasa run actions
