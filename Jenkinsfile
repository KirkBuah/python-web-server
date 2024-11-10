pipeline {
    agent {
        label 'ec2-node'
    }
    environment {
        GKE_KEY = credentials('gke-key-file')
        GITHUB_PAT = credentials('fab67924-9c54-4e6d-94d3-eb9f9322556c')
        GITHUB_USERNAME = credentials('github-username')
        GITHUB_EMAIL = credentials('github-email')
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
                // Install git
                sh '''
                    sudo apt install git -y
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
            // Authenticate and push the Docker image
            sh '''
                sudo chmod 666 /var/run/docker.sock
                cat $GKE_KEY | docker login -u _json_key --password-stdin https://europe-north1-docker.pkg.dev
                docker build -t europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:$BUILD_NUMBER .
                docker push europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:$BUILD_NUMBER  
            '''

            // Update k8s/deploy.yaml with the new image tag
            sh '''
                sed -i "s|image: europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:.*|image: europe-north1-docker.pkg.dev/gke-python-webapp/python-webapp/gke-python-webapp:$BUILD_NUMBER|" k8s/deploy.yaml
            '''

            // Commit and push changes to k8s/deploy.yaml
            sh '''
                git checkout main
                git config --global user.name "$GITHUB_USERNAME"
                git config --global user.email "$GITHUB_EMAIL"
                git add k8s/deploy.yaml
                git commit -m "Update image tag to $BUILD_NUMBER"
                git remote set-url origin https://$GITHUB_PAT@github.com/KirkBuah/python-web-server.git
                git push origin main
            '''
        }
    }
}