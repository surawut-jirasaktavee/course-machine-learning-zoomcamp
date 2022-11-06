# ELASTIC CONTAINER SERVICE

## CREATE ECS

1. GO TO `ELASTIC CONTAINER SERVICE` console.
2. Click create cluster.
3. Select cluster template for `Networking only` with `AWS FARGATE`.

  ![cluster_template](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_cluster_template.png)
  
4. Set the cluster configuration.

  ![cluster_config](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_cluster_config.png)

5. Then create cluster.
6. From the left side select `Task definition` bar.
7. Select `Create new Task Definition`

  ![create_new_task](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/create_fargate_new_task.png)
  
8. Select `new lunch type capatibilities` (**FARGATE**). 

  ![task_difinition](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_definition.png)
  
9. Configure `Task and Container definition`.
10. Set name of the task and OS.

  ![task_config](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_config.png)
  
11. Set `Task size`

  ![task_size](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_size.png)
  
12. Add container with the latest tag of your image that pushed from the `AWS ECR` and set up the port for the service.

  ![task_add_container](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_cluster_add_container.png)
  
Now your will have a task definition.
  
  ![task_definition](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_cluster.png)
  
13. Navigate back to `Cluster` from the left side bar and select the `cluster` that you created.
14. Create `Task Run`

  ![create_task_run](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/create_task_run.png)
  
15. Setting up `Task run` as the following.

  ![create_task_system](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/create_task_system.png)
  
16. Configure the `Securtity group` and add custom tcp with port range `3000`.

  ![set_security_group](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/set_cluster_sec_group.png)
  
17. Then create task and task use a few minutes to creating then will running.

  ![task_running](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_running.png)
  
18. Select the task that you created for running the service and navigate to below info of the task. you will see the public ip address then map with the port `3000` and open with the browser.

  ![task_info](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_info.png)
  
19. You should entering to `Swagger UI` and you can test with some customer data and get the result.

  ![credit_risk_classifier_service](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/credit_risk_classifier_service.png)
 
