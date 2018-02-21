#!/bin/bash
python ./parseTweets.py
python ./preprocess.py
python ./classification.py
python ./dbscan.py
python ./gmm.py
python ./parseCountData.py
python ./clusterDescrip_and_ranking.py
