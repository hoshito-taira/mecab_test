count=1
while read line
do
  curl "$line" | python wiki_extractor.py -o 47area/area_$count
  count=`expr $count + 1`
done < xml_47area
