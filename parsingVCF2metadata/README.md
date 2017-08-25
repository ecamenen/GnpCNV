Ce script se fonde sur la librairie PyVCF, librairie de parsing de VCFv4.0 et 4.1 (version : 0.6.8, release-date : 2016-03-18; [https://pyvcf.readthedocs.io/en/latest/API.html]). Le programme est lancé par un objet Launcher  ([^Launcher.py]) et peut être testé par une classe de tests unittaires ([^Test_VCFParser.py]).

Le script [^VcfParser.py] contient 4 classes: DbVarWriter, VCF, Record et Call. La première récupère l'onglet "VARIANT_CALL" d'un dbVar et va permettre de setter les cellules de cet onglet avec la fonction setCell. Un unique DbVarWriter est un composant de la classe VCF. Cette classe VCF hérite de "parser.Reader" de PyVCF et correspond à un fichier VCF en mode lecture. Il est composé d'une ou plusieurs instances de la classe Record (hérité de "model._Record") correspondant à une ligne d'enregistrement du fichier. Cette ligne d'enregistrement est elle même composé d'une ou plusieurs instance de la classe Call (model._Call), un variant pour chaque colonne d'échantillon dans une ligne. Record et Call sont défini en tant qu'Iterator Python respectivement de VCF et de Record. La classe Laucher va ainsi instancié un VCF puis appelé sa fonction parseVCF qui va boucler sur les record et sur les call pour appeler la fonction de parsing du Call (parsingCall). Celle-ci comporte une liste de colonnes qui peuvent être remplies dans l'onglet VARIANT CALL et une liste de fonctions de parsing. Pour chaque colonne de cette liste, la cellule du dbVar sera setter avec la sortie de la fonction de parsing correspondante. Ces informations de parsing peuvent être récupérées à différentes échelles par les objets correspondant: à l'échelle du VCF ( '##' , l'en tête du fichier comportant les métadonnées; ex: fonction getAssembly), à celle de la ligne d'enregistrement (ex: fonction parseChr) ou à celle du variant (ex: getVarType).

Les colonnes suivantes du  [^dbVar.xlsx] sont remplies:
- « variant_call_id » (identifiant unique du variant)
- « variant_call_type » (type de variants structuraux)
- « experiment_id » (identifiant unique obligatoire de l’expérimentation de « biologie humide » lié à une analyse de variant, clé étrangère pour l’onglet EXPERIMENT)
- « sample_id » (identifiant unique obligatoire de l’échantillon, clé étrangère pour l’onglet SAMPLE)
- « assembly » (nom de la séquence de référence)
- « chr »  (nom du chromosome où a été détecté le variant)
- « start » (position du premier nucléotide du variant)
- lorsque le parsing est permis, le champ « outer_stop » (position maximale supposée du dernier nucléotide d’un variant) est calculé depuis celui correspondant à « variant_length » (longueur de la séquence d’un variant), formaté  selon les informations fournies par certains champs du VCF (e.g. champ « IMPRECISE » de la colonne « INFO »).
- « copy_number » (nombre de copies de gènes affectés par le variant)
- « zygosity »


---

h3. *ExcelWriter(fileName)* 
hérite de la classe « Workbook » de la libraire « openpyxl» (classe correspondant à un fichier Excel). 

*_Attributs :_*
- « wb » correspondant à la sortie de la fonction load_workbook(filename) de la librarie correspondante ;
- « sheet » correspondant à la sortie de la fonction get_sheet_by_name(‘VARIANT CALLS’) de l’objet « wb » ;
- « filename », le nom du fichier Excel (variable d’entrée de l’initialisation).

_*Méthodes  :*_
- write() : fonctions save() et close()
- setCell() : permettant de valuer le contenu de « sheet » avec en entrée la colonne et la ligne de l’Excel ainsi que la valeur à attribuer


h3. *VCFParser(vcfFile, excelFilename, idExperiment )*

*_Attributs :_*
- idExperiment : l’ID de l’expériment dont est issu l’analyse ayant produit le VCF (champ du fichier de métadonnées Excel)
- version : version du fichier VCF, récupérée par la fonction getVCFversion()
- dbVar : instanciation d’un objet ExcelWriter
- headerAlt : dictionnaire des match des noms des types de CNV issus du VCF et de l’ontologie associée de dbVar (récupéré par la fonction parsingHeaderAlt())

_*Méthodes  :*_
- next() : redéfinition de la fonction d’itération propre à Python (i.e., itération d’une boucle for), permet d’instancier un objet Record2 comme itérateur de l’objet VCFParser
- getVCFversion() : récupère la version du fichier VCF et affiche un warning si la version est trop ancienne ou inconnue ;
- parsingHeaderAlt() : dans la partie du header correspondant aux variants alternatifs (i.e., « Alt. ») du VCF, insère dans un dictionnaire les valeurs VCF (clé) matchant avec l’ontologie dbVar (valeur) ;
- getAssembly() : parse le VCF pour récupérer dans le header la valeur de la référence si elle est présente, ou, le cas échéant, celle de l’assemblé.
- parseVCF() : lance sur le VCF une boucle d’itération les « Record2 », elle même lançant une boucle sur les « Calls2 » pour parser les données de chaque variant dans l’Excel.


h3. *Record2(record, vcfFile, idExperiment)* 
*_Attributs :_*
- « vcfFile », « cptCall » (un compteur du nombre de variants parsés), « idExperiment », « call » un variant (objet « call »), initialisé avec celui en première position de la liste contenue dans l’objet Record2.

_*Méthodes  :*_
- next() : redéfinition de la fonction d’itération de l’objet ; en sortie : un objet correspondant à un variant (Call2)
- parseChr : parse et formate le numéro du chromosome

h3. *Call2 (call , record , vcfFile, idExperiment, cptCall)*
 *_Attributs :_*
« vcfFile », « cptCall », « idExperiment » et un attribut de classe « cptVar » incrémenté à chaque instanciation.

_*Méthodes  :*_
- getVarType: formate en vocabulaire contrôlé dbVar le résultat d’un parsing du type de polymorphisme (e.g., SNP, INDEL, etc. ; fonction var_type(), héritée de l’objet « Call »). En cas de match avec un CNV, recherche la clé correspondante dans le dictionnaire headerAlt de la classe VCFParser et retourne la valeur format dbVar associée. S’il n’y a pas de métadonnées et que le dictionnaire est vide, appel à la fonction parsingAlt.
- parsingAlt : formate en vocabulaire contrôlé dbVar le résultat d’un parsing de types complémentaires de polymorphisme (e.g., « LINE1 insertion, tandem duplication) non renvoyés par la fonction var_type. Pour ce faire, la fonction héritée var_subtype est utilisée.
- getZygosity: retourne le type de zygosité parmi les valeurs possibles de l’ontologie dbVar (i.e., Heterozygous, Homozygous, Hemizygous) 
- getCopyNumber : retourne le nombre de copie d’une allèle (parsing du champ CN du VCF trouvé grâce à la fonction searchCNVPos)
- searchCNVPos : recherche dans le champ « FORMAT » du VCF la position de l’information contenant le nombre de copie d’une allèle (si elle existe)
- getInsertionLength : utilise la fonction calculateAlleleLength pour calculer la longueur de la séquence d’un variant. Si cette valeur est estimée, appel à la fonction roundCallLength 
- roundCallLength : formate un arrondi selon la taille du nombre envoyé en entrée
- getOuterstop : calcule la position dans le génome de la fin de la séquence du variant
- parsingCall : appel à la fonction setCell de remplissage d’une cellule du fichier Excel de la classe VCFParser. Boucle sur plusieurs cellules à remplir avec comme paramètre d’entrée : la colonne, le compteur de variant pour incrémenter le numéro de la ligne et une liste des fonctions de parsing des classes définis dans ce script.
