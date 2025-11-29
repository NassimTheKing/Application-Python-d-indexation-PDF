import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ⚙️ Démarrer le navigateur
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000")

# 🧾 Sélectionner le fichier PDF à téléverser
upload_input = driver.find_element(By.NAME, "file")
upload_input.send_keys(r"C:\chemin\vers\ton\document.pdf")  # 🔹 Remplace par un vrai chemin

# 🔍 Entrer un mot-clé à rechercher
keyword_input = driver.find_element(By.NAME, "keyword")
keyword_input.send_keys("test")

# ▶️ Soumettre le formulaire
keyword_input.send_keys(Keys.RETURN)

# ⏳ Attendre un peu le chargement
time.sleep(2)

# ✅ Vérifier le résultat affiché
body_text = driver.find_element(By.TAG_NAME, "body").text

if "test" in body_text.lower():
    print("✅ Test réussi : le mot-clé est trouvé dans le résultat.")
else:
    print("❌ Test échoué : le mot-clé n'apparaît pas dans les résultats.")

# 🚪 Fermer le navigateur
driver.quit()
