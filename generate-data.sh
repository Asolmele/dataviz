#/bin/bash

raw_data=data-raw/wait
results=data

mkdir $results
mkdir $raw_data

for d in data-raw/data/*/ ; do
    [ -L "${d%/}" ] && continue
    tmp=$raw_data/$(basename $d).txt
    name=$results/$(basename $d).csv
    python ./data-raw/decode/merge.py -d $d -o $tmp
    python ./data-raw/decode/tokenizer.py $tmp $name
done

python builder/main.py

# python decode/merge.py
