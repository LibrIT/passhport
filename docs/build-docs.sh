#!/bin/bash
make gettext
sphinx-intl update -p _build/locale -l fr
NEED_TO_UPDATE_TRANSLATION=0
for POFILE in $(find po/fr/LC_MESSAGES/ -iname "*.po")
do
	if [ ! -z "$(msggrep -v -T -e "." ${POFILE})" ]
	then
		if [ ${NEED_TO_UPDATE_TRANSLATION} == 0 ]
		then
			NEED_TO_UPDATE_TRANSLATION=1
			echo -e '\n#########################################'
			echo "Those files need to be updated :"
		fi
		echo $POFILE
	fi
done
if $(grep -Ri fuzzy  po/ | cut -d: -f1 > /dev/null )
then
	if [ ${NEED_TO_UPDATE_TRANSLATION} == 0 ]
	then
		NEED_TO_UPDATE_TRANSLATION=1
		echo -e '\n#########################################'
		echo "Those files need to be updated :"
	fi
	grep -Ri fuzzy  po/ | cut -d: -f1
fi
