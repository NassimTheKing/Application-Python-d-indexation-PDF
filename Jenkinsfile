pipeline {
    agent any
    
    environment {
        GITHUB_URL = 'https://github.com/NassimTheKing/Application-Python-d-indexation-PDF.git'
        EC2_HOST = '51.20.65.117'
        EC2_USER = 'ubuntu'
        REMOTE_DIR = '/home/ubuntu/app_flask/'
        VENV_DIR = '/home/ubuntu/app_flask/venv'
    }
    
    stages {
        stage('Checkout du Code') {
            steps {
                echo '🔄 Clonage du code depuis GitHub...'
                git branch: 'main', credentialsId: 'GITHUB-TOKEN', url: env.GITHUB_URL
                echo '✅ Code cloné avec succès'
            }
        }
        
        stage('Déploiement sur EC2') {
            steps {
                sshagent(['KEY-EC2-DEPLOY']) {
                    /* TRANSFERT DES FICHIERS */
                    echo "📤 Transfert des fichiers vers l'EC2..."
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "mkdir -p ${REMOTE_DIR}"
                        scp -r -o StrictHostKeyChecking=no * ${EC2_USER}@${EC2_HOST}:${REMOTE_DIR}
                    """
                    echo '✅ Fichiers transférés'
                    
                    /* INSTALLATION VENV + DÉPENDANCES */
                    echo "🐍 Installation du venv et des dépendances..."
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'bash -l' << 'ENDSSH'
                            set -e
                            cd ${REMOTE_DIR}
                            
                            echo "📦 Installation des paquets système..."
                            sudo apt update -y
                            sudo apt install -y python3-venv python3-pip
                            
                            # Supprimer et recréer le venv
                            if [ -d "${VENV_DIR}" ]; then
                                echo "🗑️  Suppression de l'ancien venv..."
                                rm -rf ${VENV_DIR}
                            fi
                            
                            echo "🔨 Création du venv..."
                            /usr/bin/python3 -m venv ${VENV_DIR}
                            
                            echo "📥 Mise à jour de pip..."
                            ${VENV_DIR}/bin/pip install --upgrade pip
                            
                            echo "📥 Installation des dépendances..."
                            ${VENV_DIR}/bin/pip install -r ${REMOTE_DIR}requirements.txt
                            
                            echo "✅ Environnement Python configuré"
ENDSSH
                    """
                    
                    /* SYSTEMD : NETTOYAGE + INSTALLATION */
                    echo "🔧 Installation et redémarrage du service systemd..."
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << 'ENDSSH'
                            set -e
                            
                            echo "🧹 Arrêt et suppression de l'ancien service..."
                            sudo systemctl stop mon-app-flask.service || true
                            sudo rm -f /etc/systemd/system/mon-app-flask.service
                            
                            echo "📋 Copie du nouveau fichier service..."
                            sudo cp ${REMOTE_DIR}mon-app-flask.service /etc/systemd/system/
                            
                            echo "🔄 Rechargement de systemd..."
                            sudo systemctl daemon-reload
                            
                            echo "🚀 Démarrage du service..."
                            sudo systemctl start mon-app-flask.service
                            
                            echo "✅ Activation du service au démarrage..."
                            sudo systemctl enable mon-app-flask.service
                            
                            # Attendre que le service démarre
                            sleep 3
                            
                            echo "📊 Statut du service:"
                            sudo systemctl status mon-app-flask.service --no-pager -l || true
                            
                            if sudo systemctl is-active --quiet mon-app-flask.service; then
                                echo "✅ Service actif et en cours d'exécution"
                            else
                                echo "❌ ATTENTION: Le service n'est pas actif!"
                                echo "📜 Logs du service:"
                                sudo journalctl -u mon-app-flask.service -n 30 --no-pager
                                exit 1
                            fi
ENDSSH
                    """
                    echo '✅ Déploiement terminé avec succès'
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ ========================================='
            echo '✅ DÉPLOIEMENT RÉUSSI !'
            echo '✅ ========================================='
            echo "✅ Application accessible sur: http://${EC2_HOST}:5000"
        }
        failure {
            echo '❌ ========================================='
            echo '❌ ÉCHEC DU DÉPLOIEMENT'
            echo '❌ ========================================='
            echo '❌ Consultez les logs ci-dessus'
        }
    }
}