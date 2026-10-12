# Scénario : la première machine de la boutique

La boutique fil rouge de la formation a son architecture chiffrée. Il lui faut
maintenant sa première machine, celle qui portera l'API. L'équipe s'est fixé
trois règles avant d'en créer une seule :

1. **Rien à la main.** Tout ce que la machine porte au démarrage vient d'un
   fichier user-data versionné. Une machine qu'on ne sait pas recréer à
   l'identique est une machine qu'on finira par perdre.
2. **Aucune adresse publique.** La machine naît sur un réseau privé. Elle peut
   sortir chercher ses paquets, personne ne peut entrer.
3. **Rien ne survit à l'essai.** La machine de test est détruite à la fin,
   avec son réseau.

Vous partez d'un poste où Incus fonctionne, d'un réseau privé `lab-amorcer`
préparé par le lab, d'une paire de clés SSH et d'un gabarit de user-data
incomplet. Il n'existe encore aucune machine.
