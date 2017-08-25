*OBJECTIFS*

Des métadonnées, un trackList et deux jeux de données ont été intégrés à la dernière version (3.0) du JBrowse de peuplier:
* une piste de SNP récupéré sur le site de Phytozome ([https://plantgenie.org/Data/PopGenIE/Populus_trichocarpa/v3.0/v10.1/VCF/P.trichocarpa.gatk.hap.bed.filter.snp.rm_indel.bed.biallelic.DP5.GQ10.rm_missing.recode.vcf])
* une piste de CNV extrait du tableau 5 et 6 du matériel supplémentaire de Pinosio et al (2006; [https://academic.oup.com/mbe/article/33/10/2706/2925611/Characterization-of-the-Poplar-Pan-Genome-by])

L'insertion de la piste de CNV permettait de créer des fonctions JavaScript d'affichage des features qui pourront être réutilisés lors de l'insertion de CNV dans d'autres JBrowse.


*RESULTATS*

-Piste de gène: Un lien vers une fiche d'annotation fonctionnelle du site Phytozome (ex: [https://phytozome.jgi.doe.gov/pz/portal.html#!gene?search=1&detail=1&method=3252&searchText=transcriptid:27041692]) a été ajouté au menu clique-droit des features de gènes. La fonction link2phytozome permettait ainsi de getter l'ID du gène sur une sub-feature et de créer un lien dynamique.
-Piste de CNV: Le texte secondaire (description) de chaque feature de CNV affichait les gènes impactés (récupéré par la fonction getGene gettant le champ GENEID propre au VCF de Pinosio). Si plusieurs gènes étaient impactés, une couleur permettait de différencié les CNV multi-loci des single-locus (fonction colMultiGene). Chaque glyphe de CNV était affiché d'une couleur différente en fonction de son type de CNV. Cette action permise par la fonction colCNV(featureObject, variableName, glyphObject, trackObject) permettait en même temps de modifier les éléments dans la pop-up d'un glyphe.

h2. *Fonction principale: code couleur en fonction du type de CNV ( colCNV() )*
En paramètre, elle attend notamment les objets feature et track. Ceux-ci doivent être définis en variables locales pour les besoins de certaines fonction (au risque de soulever des erreurs le cas échéant). L'ordre de ses paramètres doit être respecté pour définir une fonction jBrowse complexe. On travaillera notamment sur l'attribut de configuration du track (config). J'ai donc défini deux fonctions principales: l'une, setConf(conf), permettant de setter cette configuration et l'autre, colSVTYPE(featureObject), renvoyant en sortie de fonction colCNV la couleur d'affichage du glypĥe du CNV selon leur type.

h3. _*Sous fonction: Typage des CNVs et renvoi d'un code couleur*_
-colSVTYPE va ainsi getter le champ VCF 'SVTYPE' (i.e.,  type de SV) de l'objet feature. En fonction de différentes regex, il peut ainsi définir une couleur différente selon qu'il s'agit d'une inversion, d'une déletion, d'une insertion ou d'une duplication. Si ce champ n'est pas présent ou si aucun valeur ne match avec les regex, une seconde fonction sera appelée: colSVLEN
-colSVLEN va getter le champ VCF 'SVLEN' correspondant à différence la longueur de la référence et celle du SV. Si sa valeur < 0, alors il va renvoyer le code couleur de la déletion, sinon celui de l'insertion. Si ce champ n'est pas présent, il va appeler la fonction calculLength
-calculLength va getter la séquence de référence et celle du variant présents. Selon une même logique que colSVLEN, selon le signe de la différence entre la référence et le variant, il va renvoyer une code couleur correspondant à une insertion ou à une déletion. Le cas échéant, un code couleur par défaut sera attribué à l'élement.

h3. _*Sous fonction: Modification de la configuration*_
setConf se fonde sur l'utilisation fmtDetail pour modifier les éléments dans la pop-up. 
-Le titre de la fenêtre est remplacé si possible par une concaténation du 'SVTYPE' et du nom (ID) de la feature (action permise par l'ajout de l'objet "onClick": "action": "defaultDialog").
-Le type de la feature est valué en tant que 'CNV' 
-Le champ Description principale ('Description' et non 'description'; généralement comportant une information du type SNV C -> A) est remplacé par la légende du code couleur

-Le champ 'description' (ex: SNV C -> A) est remplacé par un champ comportant une liste d'espèce.  Pour ce faire, il va utiliser la fonction linkGnpis2taxon(track)
* linkGnpis2taxon récupère depuis la métadonnées du track correspondant au champ des espèces. La fonction s'applique seulement aux métadonnées espèces ne comporte pas déjà un lien html. Si c'est le cas, il formaté la liste pour extraire le genre et l'espèce pour chaque espèce. Ces paramètres vont être envoyé à la fonction speciesIsInGnpIS(genus, species) qui va récupérer l'ID de la card espèce GnpIS si elle existe. En sortie, la fonction renvoi une liste de liens formatés html vers ces cards.
* speciesIsInGnpIS va effectuer une requête HTML en utilisant l'API Germplasm. Deux requêtes sont nécessaires: une première pour récupérer le champ germplasmDbId qui servira à récupérer le taxonId

-La matrice des génotypes est modifiée pour ajouter un certain nombre de colonnes à l'aide de la fonction formatingAccession(featureObject)
* formatingAccession va getter cette matrice de génotype. Celle-ci correspond à une liste d'échantillons pour une variation donnée (le nom de l'échantillon est dans la première colonne) et de leur attributs (initialement uniquement le génotype GT, dans la 2eme). La fonction va créer différentes listes (une pour chaque ajout de colonne). En bouclant sur chaque accession de cette liste, elle va ajouter des attributs à chaque objet : l'espèce dont elle est issue, un lien vers l'accession card (si il existe) et des informations issus du matériel supplémentaire de Pinosio et al. ([https://academic.oup.com/mbe/article/33/10/2706/2925611/Characterization-of-the-Poplar-Pan-Genome-by]) incluant des liens vers des bases d'échantillons (SRA [https://www.ncbi.nlm.nih.gov/sra] & Biosample [https://www.ncbi.nlm.nih.gov/biosample/]), le lieu et le pays d'échantillonnage (récupéré sur ces BDDs).
