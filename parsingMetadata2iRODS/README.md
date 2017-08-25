*OBJECTIFS*
- Créer un script iRODS pour parser le fichier de métadonnées standardisés "machine readable" (sortie d'un job Talend ad hoc; [https://urgi.versailles.inra.fr/jira/browse/GNP-4856]) et associer ces informations aux fichiers de soumission correspondant (données d'analyse CNV ET fichier de métadonnées GnpCNV associé). Ce script devra utiliser une librairie adaptée pour: (a) gérer les flux de métadonnées au format iRODS et (b) catcher les erreurs appropriées

*RESULTATS*
- La fonction pos-process d'insertion de données CNV4Sel dans iRODS fait appel à un script Bash d'orchestration (Cf. [https://urgi.versailles.inra.fr/jira/browse/GNP-4777]). Lui-même fait appel à un script Python qui permet d'attribuer automatiquement les données d'un fichier de standards interopérables au fichier de soumission (données CNV et métadonnées GnpCNV). A noter que les librairies non-natives utilisés pour des langages autre que Bash doivent être copiés dans le dossier adéquat (ex: /var/lib/irods/iRODS/scripts/python).


*acPostProcForPut*
Le script ci-dessus a été ajouté au fichier de configuration /etc/irods/core.re contenant l'ensemble des déclencheurs automatiques iRODS. La fonction modifiée est un post-process se déclenchant lors de l'insertion de donnée (acPostProcForPut). Je lui ai ajouté un filtre pour qu'elle se déclenche uniquement lors d'insertion dans l'arborescence de CNV4Sel dans iRODS ( ON($objPath like "/tempZone/home/rods/CNV4Sel*") ). Celui-ci permet également de récupérer dans une variable le chemin du fichier ayant déclenché le post-process ($objPath). Cette variable va être envoyé en tant que paramètre d'un microprocess (msiExecCmd) permettant d'appeler un script Bash (parsing_metadata2iRODS.sh). Celui-ci doit être stocké dans le dossier de scripts d'IRODS (/var/lib/irods/iRODS/server/bin/cmd/). Sa sortie est récupérée dans une variable *CMD_OUT qui va être envoyé à un microprosess (msiGetStdoutInExecCmdOut) pour être traduite sur le canal de sortie (variable *OUT) puis enregistré dans un fichier de log (writeLine; /var/lib/irods/iRODS/server/log)

*Bash*
Script Bash déclenché par la règle de traitement post-process iRODs (acPostProcForPut). Son rôle principal est de lancer le script Python, le microprocess d'appel de script d'iRODS (msiExecCmd) ne marchant qu'avec du bash. Ce script récupère l'argument de cette fonction iRODS correspondant au chemin du fichier ayant déclenché le post-process et l'envoi au script Python.

*Python*

#Paramètres
Un certain nombre de paramètres peuvent être envoyé au script: 
* l'utilisateur, 
* son mot de passe,
* le nom de la zone iRODS de stockage ("tempZone" par défaut), 
* le numéro de port, l'adresse de l'hôte ainsi que le nom du fichier de métadonnées à parser ("/metadata.csv" par défaut). 
* Ces arguments sont facultatif, seul le chemin du fichier déclencheur est requis (ex: "/tempZone/home/rods/CNV4Sel/SoumissionX/GnpCNV.xls"). Ce paramètre est automatiquement envoyé au script via un script Bash qui le reçoit lui-même de la fonction iRODS de déclenchement lors d'insertion.

#Méthodes (par ordre chronologique de déclenchement)
* La fonction getCollPath(filePath) reçoit ce chemin du fichier déclencheur et renvoie en sortie le chemin du dossier de soumission (collPath)
* La fonction iRODSSession(host, port, user, password) ouvre un objet iRODS de session d'utilisateur (d'administateur par défaut; variable "sess"). Elle capture et affiche avec des messages personnalisés les erreurs iRODS éventuelles liées à un utilisateur ou un mot de passe erroné (CAT_INVALID_USER, CAT_INVALID_AUTHENTICATION) ou une erreur de connexion lié à l'adresse ou au numéro de port (NetworkException).
* La fonction sess.collections.get(collPath) va récupérer un objet iRODS correspondant à un dossier ("Collection"; variable 'coll'). Dans notre cas il s'agit du dossier de soumission de données. En cas d'échec un message d'erreur personnalisé est affiché (CollectionDoesNotExist).
* La fonction sess.data_objects.get(collPath, metadataName) recupère un objet iRODS correspondant à un fichier ("ObjectData"; variable metadata). Ce fichier correspond au fichier de métadonnées à parser. En cas d'échec un message d'erreur personnalisé est affiché (DataObjectDoesNotExist).
* La fonction testEmptyFolder(coll) va vérifier que la longueur de la liste est supérieure à 1 (s'il y a d'autres fichiers que le metadata.csv), le cas échéant elle renvoie un message d'erreur.
* La fonction metadata.remove_all() va effacer toutes les précédentes métadonnées iRODS de tous les fichiers contenus dans la collection si elles existent.
* La fonction parsingMetadata(metadata, coll) va parcourir chaque ligne du fichier de métadonnées. La première colonne de ce fichier CSV contient une clé et la seconde une valeur qui vont être récupérées. Chaque pair clé/valeur va être attribuée à chaque objet de la collection (excepté au fichier de métadonnées lui-même) grâce à la fonction metadata.add(key,value). Celle-ci tolère une même clé pour plusieurs valeurs tant que ces dernières sont différentes; en cas de doublons d'une paire clé-valeur, un message d'erreur personnalisé est affiché. Contrairement aux autres erreurs, ces erreurs sont seulement capturées et ne provoquent pas l'arrêt du programme.
* Le fichier de métadonnées peut éventuellement être  effacé en activant la fonction metadata.unlink(force=True)
