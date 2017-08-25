*Objectifs*
1/ Définir le format de métadonnées CNV4Sel avec les utilisateurs

2/ Créer un script Python pour parser un fichier VCF et l'inclure dans l'onglet 'VARIANT CALL' du dbVar

3/ Développer un job Talend:
- parser en entrée le fichier Excel de métadonnées CNV4Sel fourni par l'utilisateur
- checker les formats des onglets, les champs obligatoires et l'ontologie des champs statiques
- séparer les champs utiles (futures métadonnées iRODS) de ceux réservés à une soumission au NCBI
- créer en sortie le fichier metadata.csv qui servira de base aux métadonnées iRODS

4/ Créer un script Python pour pour parser le fichier de sortie du job Talend et associer les métadonnées au fichier VCF correspondant dans la base de données iRODS

5/ Tester le worflow des points 2, 3 et 4 avec l'intégration de données fournis par l'utilisateur

6/ Créer des fonctions JavaScript propres aux CNVs pour les JBrowse 

*Résultats*
- Le fichier Excel de métadonnées d'analyse (appelé GnpCNV) se fonde sur le format dbVar (base de variants du NCBI; [https://www.ncbi.nlm.nih.gov/core/assets/dbvar/files/dbVarSubmissionTemplate_v3.3.xlsx]). Tous les champs de ce format ont été inclus; des champs provenant de GnpCNV ont été ajoutés ainsi que d'autres, créés spécialement pour CNV4Sel.
- Un fichier CSV de métadonnées machine readable a été créé pour les besoins d'attribution de métadonnées sous iRODS. Ce format ne sera pas téléchargeable par l'utilisateur. Les métadonnées de ce fichier proviennent de certains champs de GnpCNV qui ont été renommés pour être alignés avec des standards internationaux: Dublin Core ([http://dublincore.org/]), Darwin Core ([http://rs.tdwg.org/dwc/terms/]), MIAPPE ([https://docs.google.com/spreadsheets/d/1SiUVvauhdNSpAfHgds-vQpjAXYs34lFD8wSOZdkyCgY/edit]), MIxS ([http://gensc.org/mixs/]), MIMARKS ([http://wiki.gensc.org/index.php?title=MIMARKS]) et EDAM-SWO ([http://www.ebi.ac.uk/ols/ontologies/swo])
- Après soumission par un partenaire biologiste de CNV4Sel d'un couple données d'analyse CNV -  métadonnées GnpCNV dans un formulaire sur GnpIS (technologie dataverse ; [https://data-test.jouy.inra.fr/dataverse/urgi-dataverse]), ces fichiers seront téléversés dans le gestionnaire de fichiers iRODS. Normalement, pour chaque soumission, un dossier contiendra ces fichiers dans l'arborescence iRODS de CNV4Sel. Ces fichiers données-GnpCNV pourront être prochainement téléchargés par l'utilisateur.
- Le curateur devra utiliser le job d'orchestration Talend pour (a) vérifier la conformité du remplissage du GnpCNV et (b) produire le fichier de standards iRODS. Il peut éventuellement activer un second job (convert2dbVar) (p.ex., avec une variable de contexte setté à 'yes') permettant de créer un fichier au format dbVar. ((!) copier le fichier de vocabulaire statique avant execution du Talend et éventuellement le dbVar).
- Si besoin, le curateur peut faire tourner un script python pour parser un VCF dans l'onglet VARIANT CALL du dbVar (obligatoire pour soumettre au NCBI)
- Finalement, lors de l'insertion d'un fichier de standards 'metada.csv' dans un dossier de soumission CNV4Sel sous iRODS, un Python parsera ce fichier pour attribuer ses métadonnées au fichiers contenus dans ce dossier (données d'analyse CNV, GnpCNV et éventuellement un dbVar)

