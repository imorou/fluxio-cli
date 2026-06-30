#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from datetime import datetime
from openai import OpenAI

# 1. Vérification de la clé API OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print(" Erreur critique : La variable 'OPENROUTER_API_KEY' est introuvable.")
    print(" Exécutez : source ~/fluxio-cli/.env")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def sauvegarder_dans_historique(fichier_analyse, reponse_ia):
    """[Fluxio-History] Enregistre le diagnostic dans un fichier de rapport."""
    fichier_rapport = "fluxio_report.txt"
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texte_rapport = f"\n==================================================\n DATE : {horodatage}\n🔍 ANALYSE / ACTION : {fichier_analyse}\n--------------------------------------------------\n{reponse_ia}\n==================================================\n"
    try:
        with open(fichier_rapport, "a", encoding="utf-8") as f:
            f.write(texte_rapport)
        print(f" [Fluxio-History] Rapport sauvegardé dans : {fichier_rapport}")
    except Exception as e:
        print(f"IImpossible de sauvegarder l'historique : {e}")

def extraire_et_creer_fichier(reponse_texte):
    """[Fluxio-Template] Détecte un bloc de code et propose de créer le fichier."""
    blocs = re.findall(r"```.*?\n(.*?)```", reponse_texte, re.DOTALL)
    if blocs:
        code_a_sauvegarder = blocs[0].strip()
        print("\n [Fluxio-Template] Un bloc de configuration a été détecté !")
        nom_fichier = input(" Entrez le nom du fichier à créer (ex: Dockerfile, docker-compose.yml) [Entrée pour annuler] : ").strip()
        if nom_fichier:
            try:
                with open(nom_fichier, "w", encoding="utf-8") as f:
                    f.write(code_a_sauvegarder)
                print(f" Fichier '{nom_fichier}' créé avec succès !")
            except Exception as e:
                print(f" Erreur de création de fichier : {e}")

def executer_fluxio_cli():
    if len(sys.argv) < 2:
        print(" Erreur : Argument manquant.")
        sys.exit(1)
        
    argument = sys.argv[1]
    prompt_utilisateur = ""
    est_une_action_auto = False
    cible_rapport = argument

    # MODULE FLUXIO-DOC : Générateur de Cheat Sheet DevOps interactif
    if argument == "doc" and len(sys.argv) > 2:
        sujet = " ".join(sys.argv[2:])
        print(f" [Fluxio-Doc] Génération d'une fiche technique sur : '{sujet}'...")
        prompt_utilisateur = f"Provide a practical cheat sheet for '{sujet}'. List the most important commands first inside code blocks, followed by a very brief explanation of best practices."
        cible_rapport = f"Doc {sujet}"

    # MODULE FLUXIO-FIX : Analyse et réparation de conteneur
    elif argument == "fix" and len(sys.argv) > 2:
        est_une_action_auto = True
        conteneur = sys.argv[2]
        print(f" [Fluxio-Fix] Extraction des logs de '{conteneur}'...")
        try:
            logs_conteneur = subprocess.check_output(f"docker logs --tail 30 {conteneur}", shell=True, stderr=subprocess.STDOUT, text=True)
            if not logs_conteneur.strip():
                logs_conteneur = "Le conteneur n'a renvoyé aucun log (vide)."
        except Exception as e:
            logs_conteneur = f"Impossible de récupérer les logs : {e}"
        prompt_utilisateur = f"Analyze the following crash logs from the docker container '{conteneur}'. Explain the exact root cause of the crash loop and provide the precise command or configuration fix:\n\n{logs_conteneur}"
        cible_rapport = f"Fix container {conteneur}"

    # MODULE FLUXIO-CHECK : État du système ou de Docker
    elif argument == "check" and len(sys.argv) > 2:
        est_une_action_auto = True
        cible = sys.argv[2].lower()
        cible_rapport = f"Check {cible}"
        
        if cible == "docker":
            print(" [Fluxio-Check] Collecte de l'état des conteneurs Docker...")
            try:
                contexte_check = subprocess.check_output("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'", shell=True, text=True)
            except Exception:
                contexte_check = "Erreur : Le service Docker ne répond pas."
            prompt_utilisateur = f"Analyze this 'docker ps -a' output. Spot any stopped, crashing, or abnormal containers, explain why, and give the fix command:\n\n{contexte_check}"
            
        elif cible == "system":
            print(" [Fluxio-Check] Collecte des métriques système...")
            try:
                ram = subprocess.check_output("free -m", shell=True, text=True)
                disk = subprocess.check_output("df -h /", shell=True, text=True)
                contexte_check = f"--- RAM MEMORY ---\n{ram}\n--- DISK USAGE ---\n{disk}"
            except Exception:
                contexte_check = "Erreur lors de la récupération des métriques."
            prompt_utilisateur = f"Analyze these system metrics. Spot any high usage (Disk > 85%, RAM critical), and give clear optimization commands if needed:\n\n{contexte_check}"

    # MODULE FLUXIO-LOG (Fichier statique)
    elif os.path.isfile(argument):
        print(f"🔍 [Fluxio-Log] Analyse du fichier de log détecté : {argument}...")
        try:
            with open(argument, 'r', encoding="utf-8") as fichier:
                contenu_log = fichier.read()
            prompt_utilisateur = f"Analyze this error log, explain the cause and give the exact fix command:\n\n{contenu_log}"
        except Exception as e:
            print(f" Impossible de lire le fichier : {e}")
            sys.exit(1)
            
    # MODULE CORE (Question classique)
    else:
        prompt_utilisateur = " ".join(sys.argv[1:])

    prompt_systeme = (
        "You are Fluxio-CLI, an AI terminal assistant highly specialized in DevOps architecture, "
        "Linux system administration (Ubuntu), container management (Docker), and automation (Terraform).\n\n"
        "Strict response rules:\n"
        "1. Be extremely concise and direct.\n"
        "2. ALWAYS return the exact command, script, or configuration file content first, inside a code block.\n"
        "3. Then, add a very brief technical explanation (maximum 2 sentences) below the code block.\n"
        "4. Respond ONLY in English."
    )

    print(" [Fluxio-CLI] Traitement de la demande...")

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": prompt_systeme},
                {"role": "user", "content": prompt_utilisateur}
            ]
        )
        
        reponse_texte = response.choices[0].message.content
        
        print("\n [RÉPONSE DE FLUXIO] :")
        print("-" * 50)
        print(reponse_texte)
        print("-" * 50 + "\n")

        # Sauvegarde automatique pour logs, checks, et docs
        if os.path.isfile(argument) or est_une_action_auto or (argument == "doc"):
            sauvegarder_dans_historique(cible_rapport, reponse_texte)
        else:
            mots_cles = ["generate", "create", "template", "dockerfile", "yaml", "yml", "compose"]
            if any(mot in prompt_utilisateur.lower() for mot in mots_cles):
                extraire_et_creer_fichier(reponse_texte)

    except Exception as error:
        print(f" Erreur API : {error}")
        sys.exit(1)

if __name__ == "__main__":
    executer_fluxio_cli()
