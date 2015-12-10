#!/bin/bash

for i in {12..1544}
do 
curl http://xkcd.com/$i/ | grep "Image URL (for hotlinking/embedding):" |awk '{print $(NF)}'|xargs wget -O $i.png
done
