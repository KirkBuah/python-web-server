pipeline {
    agent {
        label 'ec2-node'
    }

    stages {
        stage('Install dependencies') {
            steps {
                // Install dependencies in a virtual environment
                sh '''
                    #!/bin/bash
                    sudo apt install python3-venv -y
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                // Run unit tests
                sh '''
                    #!/bin/bash
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
    }
}
