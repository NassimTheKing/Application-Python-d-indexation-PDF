# 1. Image de Base: Utilise la version officielle et légère de Python
FROM python:3.12-slim

# 2. Répertoire de Travail: Définit le dossier /app comme répertoire de base
WORKDIR /app

# 3. Installation des Dépendances
# Copie le fichier requirements.txt
COPY requirements.txt .

# Installe Flask, Gunicorn et pypdf (nécessaire pour votre application)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie du Code: Copie tous les fichiers de votre répertoire local
# Ceci inclut app.py, le dossier templates/ et tout le reste.
COPY . .

# 5. Port: Indique le port que le conteneur va écouter
EXPOSE 80

# 6. Commande de Démarrage: Lance le serveur de production Gunicorn
# 'app:app' signifie : trouve l'instance Flask nommée 'app' dans le fichier 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]