pipeline {
    agent {
        label 'ec2-node'
    }
    environment {
        GKE_KEY = credentials('gke-key-file')
    }

    stages {
        stage('Install dependencies') {
            steps {
                // Install dependencies in a virtual environment
                sh '''
                    sudo apt install python3-venv -y
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                // Run unit tests
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s . -p "test_*.py"
                '''
            }
        }

        stage('Cleanup') {
            steps {
                // Clean up the virtual environment
                sh 'rm -rf venv'
            }
        }
    }

    post {
        always {
            // Archive test results and cleanup workspace if desired
            echo 'Pipeline completed'
        }
        failure {
            echo 'Pipeline failed'
        }
        success {
            sh '''
                sudo chmod 666 /var/run/docker.sock
                cat $GKE_KEY | docker login -u _json_key --password-stdin https://europe-north1-docker.pkg.dev
                docker build -t europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:$BUILD_NUMBER .
                docker push europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:$BUILD_NUMBER  
            '''
        }
    }
}