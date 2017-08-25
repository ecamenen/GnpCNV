*OBJECTIFS*:
- parser en entrée le fichier Excel de métadonnées CNV4Sel fourni par l'utilisateur
- checker les formats des onglets, les champs obligatoires et l'ontologie des champs statiques
- séparer les champs utiles (futures métadonnées iRODS) de ceux réservés à une soumission au NCBI
- créer en sortie le fichier metadata.csv qui servira de base aux métadonnées iRODS

*Orchestration*
Ses variables de contexte [^context.properties] sont les suivantes :
* workdir, le chemin du dossier contenant les fichiers de soumission (ex: /home/ecamenen/Documents/git/GnpCNV/talend)
* excelFileIn, le nom du fichier Excel de métadonnées d'analyse de CNV soumis par l'utilisateur (GnpCNV); ex: /Pinosioetal2016.xlsx
* encoding, l'encodage ex: UTF-8
* dbVarSubmit, mettre 'yes' pour activer le sous-job de conversion au format dbVar
* storageDir, le chemin du dossier où sont stockés les patron des fichiers staticData.tmp et éventuellement dbVar.xlsx (ex: /home/ecamenen/Documents/git/GnpCNV/)

Ce job d'orchestration (au nom original 'orchestration') permet d'exécuter un premier job permettant de vérifier le remplissage du GnpCNV et de créer un fichier CSV de métadonnées de standards "machine readable". Si dbVarSubmit vaut 'yes', un second job est activé et permettant de créer un fichier au format dbVar (base de variant du NCBI) pour une soumission par l'utilisateur.

*CheckOrchestration*

h2. Objectifs
Ce Talend vise à vérifier le format GnpCNV (métadonnées d'analyse de CNV) rempli par un utilisateur dans le cadre du projet CNV4Sel. 

Il permet également de produire un fichier CSV de métadonnées standardisés et issus de certains champs extraits du GnpCNV et renommé pour correspondre avec certains champs des standards internationaux:
* Dublin Core pour les données bibliographiques ([http://dublincore.org/]), 
* Darwin Core pour la taxonomie ([http://rs.tdwg.org/dwc/terms/]), 
* MIAPPE pour les données d'échantillons ([https://docs.google.com/spreadsheets/d/1SiUVvauhdNSpAfHgds-vQpjAXYs34lFD8wSOZdkyCgY/edit#gid=989837895]), 
* MIxS pour les données de séquençage ([http://wiki.gensc.org/index.php?title=MIMARKS])
* Software Ontology pour les paramètres de logiciels bioinformatiques ([http://theswo.sourceforge.net/]).

Ce fichier de métadonnées standardisés permettra d'attribuer ces métadonnées sous iRODS aux fichiers issus d'une soumission CNV4Sel

h2. Resultats

Chacun des sous-jobs concernant un onglet du fichier de métadonnées CNV4Sel (GnpCNV) est orchestré par le job CheckOrchestration. Lui-même est orchestré par un super-job au nom original : "orchestration" ([https://urgi.versailles.inra.fr/jira/browse/GNP-4856]). 

Ce job CheckOrchestration comporte un premier sub-job où deux paires clé-valeurs sont créées de manière statique (DC.type:Polymorphism & SWO.Topic....:CNV) et enregistrées dans un fichier CSV de standards internationaux constitué de deux colonnes : une pour les clés et une pour les valeurs. CheckOrchestration comporte ainsi une série d'exécution des sous-job relatifs à la vérification de chaque onglet. Au final, ce job d'orchestration vérifiera l'existence de fichiers bad: si c'est le cas il supprime le fichier CSV de standards et quitte le programme sur le canal d'erreur; le cas échéant, le dossier de fichiers bad automatiquement créé  - même vide - est supprimé et le programme se termine. 

{color:red}(!) A noter que chaque job de vérification d'onglet nécessite la présence d'un fichier comportant des listes de valeurs statiques pour plusieurs champs de métadonnées. Si ce fichier n'est pas présent sous le nom 'staticData.tmp dans un dossier défini dont le chemin est dans la variable de contexte 'storageDir', il est nécessaire d'activer le job extractStatic présent dans CheckOrchestration. Ce job permet d'extraire l'onglet caché (" CVs"; attention à l'espace !) du fichier GnpCNV soumis par l'utilisateur.{color}



Chacun des job de vérification d'onglets (p.ex: CheckAnalysis) comporte plusieurs sous-jobs:
# Le premier consiste à lire l'onglet correspondant du fichier GnpCNV, à l'enregistrer dans un fichier CSV temporaire, à lire ligne par ligne ce fichier pour filtrer les lignes vides pour les enregistrer dans un nouveau fichier temporaire.
# Le second consiste à compter le nombre de ligne du dernier fichier temporaire créé. S'il est vide et que son remplissage est obligatoire, un message d'erreur alerte le curateur (fichier bad créé) et le job se termine pour cet onglet.
# Le cas échéant, un troisième sous-job compare le fichier temporaire des métadonnées contenus dans GnpCNV avec un schéma de référence notamment pour vérifier le remplissage des colonnes obligatoires. En cas d'erreur, le flux est stocké dans un buffer d'erreur. Le cas échéant, le flux subit un traitement tJavaRow pour convertir les valeurs nulles en valeurs vides ('') pour éviter des erreurs. Ce flux d'entrée est transformé dans un tMap. En entrée du module, un second flux de look-up va permettre d'extraire une liste de valeurs statiques d'un fichier CSV. A l'aide d'une jointure, le module permet de vérifier que les valeurs de certains champs correspondent avec cette liste de vocabulaire contrôlé. A noter que Talend nous permettait seulement de traiter un seul champ de vocabulaire contrôlé à la fois (le cas échéant, des erreurs apparaissaient). Pareillement, certains champs acceptant des valeurs vides (s'ils sont facultatif), ces valeurs vides ont été ajoutées au flux de look-up de certains job. En sortie du module de mapping tMap on a deux flux possibles: un enregistrement d'erreur en cas de non-correspondance avec le look-up et une poursuite du traitement. Lorsque tous les traitement de look-up ont été effectués, le flux est pivoté pour être enregistrés sous la forme de deux colonnes clé-valeurs dans le fichier CSV de standards.
# Le dernier sous-job permet de récupérer les flux d'erreurs précédemment stockés dans des buffer et les enregistrer dans un fichier .bad




Deux catégories d'onglet ont fait l'objet de traitement particulier:


-Les jobs checkStudy & checkSamplesets parsent des onglets qui contrairement aux autres ont leurs métadonnées orientés verticalement sous la forme de deux colonnes clé-valeur. Pour effectuer tous les traitement nécessaires, un certain nombre de modules sont ajoutés au premier sous-job :
# Tout d'abord, le nom de l'onglet est envoyé en flux à l'aide de paramètres du fichier de contexte qui est ré-actualisé et envoyé dans un module d’exécution d'un job de pivot de flux (pivotExcel).
# Au sein de ce sous-job, pour pouvoir effectuer une rotation du flux depuis l'axe vertical (deux colonnes : clé-valeur) à l'axe horizontal (autant de colonnes qu'il y a de clés), j'ai utilisé le module tPivotToColumnsDelimited. Celui-ci pivote le flux en fonction d'un groupement effectué sur un champs particulier. Pour ce faire j'ai dû créé un champ ID ajouté aux champs clé-valeur avec la même valeur pour tous ("1"). Le pivot s'effectuait ainsi sur un seul groupe d'ID ("1") et le fichier enregistré par le module tPivotToColumnsDelimited ne contenait donc qu'une seule ligne correspondant initialement à la colonne "valeur" et autant de colonnes qu'il y a de clés.
# Ce fichier temporaire issu du sous-job de pivot est récupéré par le job qui l'a appelé (checkStudy par exemple). La colonne ID va être supprimée et le flux de données sera enregistré dans un nouveau fichier temporaire. Pareillement que les autres onglets, les lignes vides seront ensuite filtrées.


-Pour l'onglet contact, chacune de ces lignes correspond à un contact particulier défini dans sa première colonne ("contactType"). Les valeurs des cinq premières lignes sont obligatoirement remplis avec : Submitter, First author, Senior Author, Other et Analyst). Or, cet onglet doit obligatoirement avoir sa première ligne rempli (soit la valeur "Submitter" de la première colonne "contactType"). Pour ce faire, il va ajouter deux sous-jobs :
#  Pour vérifier que l'onglet "Contact" obligatoire soit rempli, après le premier sous-job ayant filtrés les lignes vides, un deuxième sous-job va supprimer la première colonne correspondant au type de Contact et de nouveau supprimer les lignes vides de ce nouveau format. 
{color:#cccccc}# Ce traitement permet de renvoyer à l'aide du troisième sous-job un message d'erreur si aucune ligne n'est remplie, comme pour les autres onglets et le job sera terminé {color}
# Après avoir vérifié que cet onglet contenait au moins une ligne, le job checkContacts comporte un quatrième sous-job permettant de vérifier le remplissage obligatoire de la première ligne correspondant au Soumetteur de données. Si ce n'est pas le cas, une erreur sera stockée dans un buffer. Si cette ligne est bien remplie, le tMap permet de vérifier à l'aide du filtre d'expression que la ligne correspondante contienne des informations sur le nom OU sur le prénom du contact ET sur l'email du contact OU sur son identifiant NCBI. 
{color:#cccccc} # Si l'onglet contient d'autres lignes, le cinquième sous-job de vérification de l'onglet Contact sera similaire à celui des autres onglets (dans leur cas, correspondant à leur troisième sous-job) à la différence que le tMap utilisera un filtre d'expression comme pour la première ligne 'Submitter'.
# Comme pour les autres contacts, les erreurs capturées dans des buffer seront enregistrés dans un fichier .bad {color}


*convert2dbVar*

h2. Objectifs

Ce job Talend ("convert2dbVar") permet au curateur de créer un nouveau fichier au format dbVar (base de variant du NCBI) téléchargeable ici: [https://www.ncbi.nlm.nih.gov/core/assets/dbvar/files/dbVarSubmissionTemplate_v3.3.xlsx]. Il se fonde sur la conversion d'un format de métadonnées d'analyse de CNV (GnpCNV). Cet outil permettra donc à un utilisateur de soumettre à dbVar après avoir déposer un fichier GnpCNV dans la base de GnpIS. Il peut être activé optionnellement par le super-job "orchestration" [https://urgi.versailles.inra.fr/jira/browse/GNP-4856].

h2. Resultats

-A l'aide d'un tJavaFlex, grâce à la fonction WorkbookFactory.create il va créé un objet depuis le patron de fichier dbVar qu'il faut fournir en paramètre du job d'orchestration (excelFileIn). [{color:red} (!) Par défaut, le fichier est considéré comme présent dans le dossier Talend (défini par context.workdir) sous le nom 'dbVar.xlsx'. Si ce n'est pas le cas il faut l'y copier.{color} ] Ce module permet de boucler sur les onglets et de les instancier dans une variable "sheetName" grâce à la fonction getSheetName de l'objet.

-Le module tJava permet d'afficher le nom de l'onglet en cours de traitement.

-Depuis l'orchestration, ce job est activé après celui vérifiant le remplissage du format GnpCNV [https://urgi.versailles.inra.fr/jira/browse/GNP-4854]. De ce fait, pour le format dbVar dont il découle, un certains nombre de vérifications ont déjà été effectués. et différents traitements seront effectués en fonction de l'onglet itéré :
* L'onglet est obligatoirement ouvert à l'aide du module tExcelInput. Dans le cas des onglets Study et Samplesets dont la données est orientés verticalement (deux colonnes clé-valeur), le flux est pivoté à l'aide de l'exécution d'un sous-job ad hoc (pivotExcel).
* De manière optionnel, un sous-job permet de supprimer les lignes vides (tFilterRow) de certains onglets (Samples, Samplesets & VariantCalls).
* Pour certains onglets, seuls le remplissage des onglets (tRowCount) et des champs qui n'étaient pas obligatoires (tSchemaComplianceCheck) pour GnpCNV (et qui le sont pour dbVar) doit être vérifié. Si le format ne correspond pas avec les règles de remplissage de dbVar, des fichiers d'erreurs ".bad" sont enregistrés pour chaque onglets correspondant.
* Par ailleurs, le format GnpCNV contient l'ensemble des colonnes dbVar plus - pour certains onglets - quelques colonnes surnuméraires. Celles-ci doivent donc être filtrées au sein d'un sous-job adéquat (tFilterColumn).  
* Pour les onglets Study et Samplesets, le flux initiallement pivoté pour effectuer les traitement sera de nouveau pivoté pour retrouver son format initial (tUnpivotRow) correspondant à deux colonnes (clé-valeur).
* Finalement, après traitement, les flux de tous les onglets sont enregistrés dans l'onglet correspondant du dbVar nouvellement créé (tExcelOutput).

-Au final, il va vérifier l'existence de fichiers bad: si c'est le cas il supprime le fichier CSV de standards et quitte le programme sur le canal d'erreur; le cas échéant, le dossier de fichiers bad automatiquement créé - même vide - est supprimé et le programme se termine. 
{color:#707070}
(i) A noter:
* Pour l'onglet contact, un tMap permet à l'aide du filtre d'expression d'écarter les lignes contenant la valeur 'Analyst' pour le champ 'contactType'. En effet, cette valeur n'est pas native de dbVar (et les lignes vides).
* L'onglet Analysis du format GnpCNV n'est pas présent au sein du format dbVar. Certains champs au format dbVar de l'onglet l'onglet Experiment ont été migrés dans cet onglet. Les champs dbVar de ces deux onglets (Experiment & Analysis) sont recombinés au sein d'un tMap pour reconstituer les champs propre à l'onglet Experiment au format dbVar.{color}

