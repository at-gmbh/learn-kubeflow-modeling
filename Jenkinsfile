
pipeline {
    // run the pipeline on any available agent/slave
    agent any

    options {
        // timeout the job after 1 hour
        timeout(time: 1, unit: 'HOURS')
        // keep logs from last 10 jobs (default: no limit)
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {

        PROJECT_NAME = "kubeflow-120"  
        APP = "learn-kubeflow-modeling"
        ENV="dev"

        AWS_ACCOUNT = "863518836478"
        AWS_CREDENTIALS = "jenkins-aws-credentials"
        AWS_DEFAULT_REGION = "eu-central-1"


        DOCKER_REG_URL = "${env.AWS_ACCOUNT}.dkr.ecr.${env.AWS_DEFAULT_REGION}.amazonaws.com"
        DOCKER_REG_URL_HTTPS = "https://${DOCKER_REG_URL}"
        DOCKER_REGISTRY_CREDENTIALS = "ecr:${env.AWS_DEFAULT_REGION}:${AWS_CREDENTIALS}"

        DOCKER_REPO = "${env.ENV}/${env.PROJECT_NAME}/${env.APP}"

    }

    stages {
        stage("init") {
            steps {
                sh('''
                    echo "BUILD_NUMBER: ${BUILD_NUMBER}"
                    echo "APP_NAME: ${APP_NAME}"
                ''')

                sh('echo "Loading groovy scripts"')
                script {
                    utils = load "utils.groovy"
                }
            }
        }

         stage("build and push image") {
            //when { changeset "dockerfiles/rstudio/**"}
            steps {
                script {
                    utils.build("${env.DOCKER_REPO}:latest", ".")
                }
                script {
                    utils.deployImage("${env.DOCKER_REPO}:latest", "latest", "https://${env.DOCKER_REG_URL}/${env.DOCKER_REPO}", env.DOCKER_REGISTRY_CREDENTIALS)
                }
            }
        }

    }

}
