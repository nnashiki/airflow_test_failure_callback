# airflow_test_failure_callback
on_failure_callback をテストしてみる


検証の結果:
タスクのログにはタスクのon_failure_callbackのログが残るが、DAGのon_failure_callbackのログは残らない。
PythonOperatorのコールバックにエラーのデフォルトargsとして指定するのが良さそう。

```
*** Reading local file: /usr/local/airflow/logs/sample_dag/fail_task/2020-08-11T00:00:00+00:00/1.log
[2020-08-12 12:25:20,951] {{taskinstance.py:669}} INFO - Dependencies all met for <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [queued]>
[2020-08-12 12:25:20,960] {{taskinstance.py:669}} INFO - Dependencies all met for <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [queued]>
[2020-08-12 12:25:20,960] {{taskinstance.py:879}} INFO - 
--------------------------------------------------------------------------------
[2020-08-12 12:25:20,960] {{taskinstance.py:880}} INFO - Starting attempt 1 of 1
[2020-08-12 12:25:20,960] {{taskinstance.py:881}} INFO - 
--------------------------------------------------------------------------------
[2020-08-12 12:25:20,971] {{taskinstance.py:900}} INFO - Executing <Task(PythonOperator): fail_task> on 2020-08-11T00:00:00+00:00
[2020-08-12 12:25:20,973] {{standard_task_runner.py:53}} INFO - Started process 73 to run task
[2020-08-12 12:25:21,024] {{logging_mixin.py:112}} INFO - Running %s on host %s <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [running]> 6636e679f187
[2020-08-12 12:25:21,034] {{taskinstance.py:1145}} ERROR - エラーだ!!
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/airflow/models/taskinstance.py", line 983, in _run_raw_task
    result = task_copy.execute(context=context)
  File "/usr/local/lib/python3.7/site-packages/airflow/operators/python_operator.py", line 113, in execute
    return_value = self.execute_callable()
  File "/usr/local/lib/python3.7/site-packages/airflow/operators/python_operator.py", line 118, in execute_callable
    return self.python_callable(*self.op_args, **self.op_kwargs)
  File "/usr/local/airflow/dags/flow.py", line 11, in all_time_fail
    raise Exception('エラーだ!!')
Exception: エラーだ!!
[2020-08-12 12:25:21,041] {{taskinstance.py:1202}} INFO - Marking task as FAILED.dag_id=sample_dag, task_id=fail_task, execution_date=20200811T000000, start_date=20200812T122520, end_date=20200812T122521
[2020-08-12 12:25:21,041] {{logging_mixin.py:112}} INFO - タスクが失敗した時
[2020-08-12 12:25:30,918] {{logging_mixin.py:112}} INFO - [2020-08-12 12:25:30,917] {{local_task_job.py:103}} INFO - Task exited with return code 1
```

```
** Reading local file: /usr/local/airflow/logs/sample_dag/fail_task/2020-08-11T00:00:00+00:00/1.log
[2020-08-12 12:28:29,634] {{taskinstance.py:669}} INFO - Dependencies all met for <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [queued]>
[2020-08-12 12:28:29,644] {{taskinstance.py:669}} INFO - Dependencies all met for <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [queued]>
[2020-08-12 12:28:29,644] {{taskinstance.py:879}} INFO - 
--------------------------------------------------------------------------------
[2020-08-12 12:28:29,644] {{taskinstance.py:880}} INFO - Starting attempt 1 of 1
[2020-08-12 12:28:29,644] {{taskinstance.py:881}} INFO - 
--------------------------------------------------------------------------------
[2020-08-12 12:28:29,657] {{taskinstance.py:900}} INFO - Executing <Task(PythonOperator): fail_task> on 2020-08-11T00:00:00+00:00
[2020-08-12 12:28:29,661] {{standard_task_runner.py:53}} INFO - Started process 59 to run task
[2020-08-12 12:28:29,714] {{logging_mixin.py:112}} INFO - Running %s on host %s <TaskInstance: sample_dag.fail_task 2020-08-11T00:00:00+00:00 [running]> 95040f560c9d
[2020-08-12 12:28:29,725] {{taskinstance.py:1145}} ERROR - エラーだ!!
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/airflow/models/taskinstance.py", line 983, in _run_raw_task
    result = task_copy.execute(context=context)
  File "/usr/local/lib/python3.7/site-packages/airflow/operators/python_operator.py", line 113, in execute
    return_value = self.execute_callable()
  File "/usr/local/lib/python3.7/site-packages/airflow/operators/python_operator.py", line 118, in execute_callable
    return self.python_callable(*self.op_args, **self.op_kwargs)
  File "/usr/local/airflow/dags/flow.py", line 11, in all_time_fail
    raise Exception('エラーだ!!')
Exception: エラーだ!!
[2020-08-12 12:28:29,733] {{taskinstance.py:1202}} INFO - Marking task as FAILED.dag_id=sample_dag, task_id=fail_task, execution_date=20200811T000000, start_date=20200812T122829, end_date=20200812T122829
[2020-08-12 12:28:39,599] {{logging_mixin.py:112}} INFO - [2020-08-12 12:28:39,598] {{local_task_job.py:103}} INFO - Task exited with return code 1
```

コンテキスト  
`context['dag']`
`context['task']`
`context['execution_date']` etc...


参考記事:
https://medium.com/@momota/airflow-dag%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E5%90%84%E3%82%BF%E3%82%B9%E3%82%AF%E3%81%AE%E6%88%90%E5%8A%9For%E5%A4%B1%E6%95%97%E3%82%92slack%E3%81%AB%E9%80%9A%E7%9F%A5%E3%81%99%E3%82%8B-5eecda9ec378  
https://blog.imind.jp/entry/2019/02/08/170332  
https://note.com/dd_techblog/n/n7c3fc2559ff2  
https://qiita.com/munaita_/items/1a5b131839e01ea7280dhttps://qiita.com/munaita_/items/1a5b131839e01ea7280d  
https://note.com/dd_techblog/n/n7c3fc2559ff2  
