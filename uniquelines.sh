#!/bin/bash

if [ -f "$*" ]
then
	cp "$*" ".$*_original"
	awk '!x[$0]++' ".$*_original" > "$*"
fi
