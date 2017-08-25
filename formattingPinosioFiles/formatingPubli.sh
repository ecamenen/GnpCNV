cut -f 1-6,13- $file > $file2 #extraire certaines colonnes
sed -re 's/(;){2}/;<NA>;/g' $file | sed -re 's/\t;/\t<NA>/g' | sed -re  's/;$/<NA>/g' | sed -re 's/,//g' | sed -re 's/;/,/g' > $file2 # enlever certains caracteres
#awk -F'\t' '{if (!($4=="na" || $4=="0/0")) print $0}' $file2 > $file

#awk '/^>/ {printf("\n");next; } { printf("%s",$0);}  END {printf("\n");}' < REF.fa | tail -n +2  > REF2.fa

head -n 7 Pinosio2016b.csv > Pinosio2016.vcf
tail -n +8 Pinosio2016b.csv | sort -k 1,1n -k 2,2n  >> Pinosio2016.vcf
head -n 7 test3.txt && tail -n +9 test3.txt

cat Pinosio2016.vcf | head -n 10  && cat Pinosio2016.vcf | tail -n 10
gunzip -c Pinosio2016.vcf.gz | head -n 10  && gunzip -c Pinosio2016.vcf.gz | tail -n 10

for csv in *.csv; do cat headerfile $csv > tmpfile2; mv tmpfile2 $csv; done
rm headerfile

grep -m1 "pattern" fichier #affiche la premiere occurence

sed -e '0,/Chr02/ s//###\nChr02/1' test4.txt #insere avant la premier occurence et depuis le debut de la ligne

sed -e '0~3 a\###' test4.txt #insere avant la premiere ligne toutes les 3 lignes


awk -F'\t' '!/^##/ { if(NR%3==0){ print $0 "\n###";} { print $0;}} /^##/ { print $0 ;} { print $0;}}  END {printf("\n");}' test4.txt


awk -F'\t' '!/^##/ { if(NR%3==0){ print $0 "\n###";} { print $0;}} /^##/ { print $0 ;}  END {printf("\n");}' test4.txt

cut -c -3 class | uniq -c | sort -k 1,1n
