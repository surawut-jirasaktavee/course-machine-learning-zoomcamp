# ELASTIC CONTAINER REGISTRY

In order to push the image container for our model service to `AWS ELASTIC CONTAINER REGISTRY` follow this guide instruction.

## Create ECR Repository

> **NOTE:** In order to push the image container to `AWS ECR` you should have `AWS CLI` first to installation see the [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

> **NOTE:** In order to push the image container with specific `AWS PROFILE` see the [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

Navigate to the search bar and find the `Elastic Container Registry`. 

- Go to the ECR console and click create.
- Set the name of your private repo.
- Leave all options as default and create.

![create_ecr_repo](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/crate_ecr_repo.png)

![ecr_repo](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/ecr_repo.png)

This will assume we already have a container image. we will push the image to aws repo with following command. you can follow the command that will show you after finish to create the reposity as well.

1. we need to retrieve an authentication token and authenticate your Docker client to your registry.

    Use the AWS CLI:

    ```bash
    aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <your registry uri>
    ```

    > Note: if you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

2. Then build the Docker image in case your still don't build any images. Skip this step if you already have one.

    ```bash
    docker build -t <your repository> .
    ```

3. After the build is completed, tag your image and push the image to the registry.

    ```bash
    docker tag <image_name:tag> <your registry uri>
    ```

4. Run the following command to push the image to the registry.

    ```bash
    docker push <your registry uri>
    ```
    
![push_image](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/docker_images_tag.png)

