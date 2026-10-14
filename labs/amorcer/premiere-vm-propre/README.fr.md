# Première VM propre : amorcée par cloud-init, sans adresse publique

Une machine cloud bien née ne se configure pas à la main après son démarrage :
elle reçoit au boot un fichier **user-data** que **cloud-init** applique une
seule fois, et elle naît sur un **réseau privé**, sans adresse joignable depuis
Internet. Ce lab vous fait poser ce geste en local, sans compte cloud : une
machine virtuelle **Incus** joue le rôle de l'instance, un réseau Incus privé
celui du réseau du fournisseur.

Leçon du site qui porte ce lab :
<https://blog.stephane-robert.info/docs/cloud/cloud-init/>.

## Ce que vous saurez faire

- Écrire un user-data valide : utilisateur sans mot de passe joignable par clé
  SSH, paquets installés au premier démarrage, fichier posé avec ses droits.
- Démarrer une machine virtuelle à partir de ce seul fichier, sur un réseau
  privé en NAT sortant.
- Vérifier que cloud-init a terminé sans erreur, et que la machine n'a aucune
  adresse publique.
- Détruire la machine et ce qui l'entoure, pour ne rien laisser derrière soi.

## Prérequis

- **Incus installé et utilisable sans sudo** (votre compte dans le groupe
  `incus-admin`) :
  <https://blog.stephane-robert.info/docs/virtualiser/type1/incus/installation/>.
  Le poste doit savoir virtualiser (KVM) : `incus info | grep -i virtual`
  doit citer `qemu`.
- **dsoxlab installé** :
  <https://blog.stephane-robert.info/docs/dsoxlab/installation/>.
- Un accès Internet sortant : l'image (300 Mo environ au premier tirage) et
  les paquets se téléchargent.

## Durée

30 minutes environ, dont une minute de démarrage de la machine une fois
l'image en cache.

## Ce que `dsoxlab run` prépare

- le réseau privé `lab-amorcer` : `10.10.71.0/24`, NAT sortant, sans IPv6 ;
- une paire de clés SSH propre au lab, `cle_lab` et `cle_lab.pub`, dans
  `challenge/work` ;
- un gabarit `challenge/work/user-data.yaml`, troué de `???`.

```bash
dsoxlab run amorcer-premiere-vm-propre
cd labs/amorcer/premiere-vm-propre/challenge/work
```

## Étape 1 : écrire le user-data

Le fichier commence **exactement** par `#cloud-config` : sans cette ligne,
cloud-init ignore tout le reste, sans erreur visible. Complétez le gabarit pour
obtenir :

```yaml
#cloud-config
users:
  - name: boutique
    shell: /bin/bash
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... boutique-lab   # le contenu de cle_lab.pub
package_update: true
packages:
  - jq
  - tree
write_files:
  - path: /etc/boutique/role
    content: |
      app
    owner: root:root
    permissions: "0644"
```

Trois choix méritent un mot. `lock_passwd: true` verrouille le mot de passe :
le compte ne s'ouvre que par la clé. L'utilisateur **n'est pas** dans le groupe
`sudo` : c'est un compte applicatif, pas un compte d'administration. Les droits
`"0644"` sont **entre guillemets**, sinon YAML les lit comme un nombre décimal.

## Étape 2 : démarrer la machine à partir du fichier

```bash
incus launch images:ubuntu/noble/cloud boutique-vm1 --vm \
  --network lab-amorcer \
  --config=cloud-init.user-data="$(cat user-data.yaml)"
```

`--vm` demande une **machine virtuelle**, avec son propre noyau, comme une
instance cloud. `--network lab-amorcer` la branche sur le seul réseau privé.
Le user-data passe par la clé `cloud-init.user-data`, comme il passe par le
service de métadonnées chez un fournisseur.

## Étape 3 : vérifier depuis la machine

```bash
incus exec boutique-vm1 -- cloud-init status --wait
incus exec boutique-vm1 -- id boutique
incus exec boutique-vm1 -- dpkg-query -W jq tree
incus exec boutique-vm1 -- cat /etc/boutique/role
incus list boutique-vm1 -c n4t
```

`status: done` signifie que cloud-init a fini. L'adresse affichée est en
`10.10.71.x` : privée, joignable depuis votre poste, invisible d'Internet. La
machine sort tout de même installer ses paquets, par le **NAT** du réseau,
exactement comme une instance sans IP publique sort par la passerelle NAT de
son réseau cloud.

```bash
dsoxlab check amorcer-premiere-vm-propre
```

## Étape 4 : détruire

Une machine oubliée continue de coûter chez un fournisseur. Ici, la règle est
la même :

```bash
dsoxlab clean amorcer-premiere-vm-propre
incus list boutique-vm1        # la liste doit être vide
```

`clean` détruit la machine, puis le réseau `lab-amorcer`.

## Ce que ce lab ne prouve pas

Une machine Incus n'est pas une instance de fournisseur : le service de
métadonnées, les images et l'adressage réels diffèrent. Le geste, lui, est le
même : un fichier, un démarrage, aucune intervention manuelle, aucune adresse
publique.
