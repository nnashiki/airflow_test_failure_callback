build:
	docker build --rm \
	 --build-arg AIRFLOW_DEPS="datadog,dask" \
	 -t ariflow_failure_callback .

python_ver:
	docker run --rm -it ariflow_failure_callback python -V

run:
	docker run --rm -d -p 8080:8080 -v ${PWD}/src/dags:/usr/local/airflow/dags ariflow_failure_callback

down:
	docker-compose -p ${PROJECT} down

up:
	docker-compose -p ${PROJECT} up -d


