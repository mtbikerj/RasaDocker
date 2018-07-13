#!/bin/bash
# This bash script rebuilds the NLU container and accepts a parameter for level
# The level determines how low to rebuild.
#  Providing a level of "bare" rebuilds everything from rasa/rasa_nlu:latest-bare up through NLU
#  Providing a level of "spacy" uses the existing bare image, but rebuilds the chatbot/spacy:latest image and then the NLU
#  Providing a value of "nlu" only rebuilds the NLU.  this is the fastest rebuild option
LVL=$1
if [ $# -eq 0 ] ; then
 echo "You must provide a parameter of either 'bare', 'spacy', or 'nlu'."
elif [ "$LVL" == "bare" ] ; then
 bash bash/bare.sh
 bash bash/chatbot.sh
 bash bash/nlu.sh
elif [ "$LVL" == "spacy" ] ; then
 bash bash/chatbot.sh
 bash bash/nlu.sh
elif [ "$LVL" == "nlu" ] ; then
 bash bash/nlu.sh
else
 echo "You must provide a parameter of either 'bare', 'spacy', or 'nlu'."
fi