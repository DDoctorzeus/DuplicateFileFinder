#!/bin/bash
IFS=$'\n';

HELPTEXT="Usage: ./duplicatefinder.sh path filesearchpattern\n
    e.g: ./duplicatefinder.sh /home/user/ '*.jpg'\n
    \n
    Triggers:\n
    -m : Move duplicates to specified directory
";

MOVEMODE=0;
MOVEDIR='';

COUNT=0;
COUNT2=0;
FOUNDFILES=();
FOUNDFILESCOUNT=0;

CRCVALS=();
CRCVALA='';
CRCVALB='';
MD5VALA='';
MD5VALB='';
CREATIONDATESTR='';

#Check Minimum Input
if [ $# -lt 2 ]; then 
    echo -e $HELPTEXT;
    exit 1;
elif [ $# -gt 2 ] && [ $# -ne 4 ]; then
    echo "You must specifiy a path with the move flag";
    exit 1;
fi

#Get additional statements
if [ "$3" == "-m" ]; then
    MOVEMODE=1;
    MOVEDIR="$4";
fi

#Check directorys exists
if [ ! -d "$1" ]; then
    echo "Search directory does not exist, or you do not have access to it.";
    exit 1;
elif [ ! "$MOVEDIR" == '' ] && [ ! -d "$MOVEDIR" ]; then
    echo "Specified move directory does not exist, or you do not have access to it.";
    exit 1;
fi

echo "Searching For Files.."
if [ [ "$2" == "'*'" ]; then
    FOUNDFILES=( $(find $1 -type f) );
else
    FOUNDFILES=( $(find $1 -type f -iname $2) );
fi
FOUNDFILESCOUNT=${#FOUNDFILES[@]};

echo "Found $FOUNDFILESCOUNT Files..";

echo "Checking CRC Values..";
COUNT=0;
COUNT2=0;
while [ $COUNT -lt $FOUNDFILESCOUNT ]; do

    #If we do not already have this crc val, then get it
    if [ "${CRCVALS[COUNT]}" == '' ]; then
        CRCVALS[$COUNT]=$(cksum ${FOUNDFILES[COUNT]} | cut -d ' ' -f 1);
    fi

    #Get ValA
    CRCVALA=${CRCVALS[$COUNT]};

    #Loop through looking for duplicates
    COUNT2=$((COUNT+1));
    while [ $COUNT2 -lt $FOUNDFILESCOUNT ]; do

        #If we do not already have this crc val, then get it
        if [ "${CRCVALS[COUNT2]}" == '' ]; then
            CRCVALS[$COUNT2]=$(cksum ${FOUNDFILES[COUNT2]} | cut -d ' ' -f 1);
        fi

        #Get ValB
        CRCVALB=${CRCVALS[$COUNT2]};
        
        #If we found a match
        if [ "$CRCVALA" == "$CRCVALB" ]; then

            #Also check md5 hash (just in case)
            MD5VALA=$(md5sum ${FOUNDFILES[$COUNT]} | cut -d ' ' -f 1);
            MD5VALB=$(md5sum ${FOUNDFILES[$COUNT2]} | cut -d ' ' -f 1);

            #If we have confirmed a duplicated with md5
            if [ "$MD5VALA" == "$MD5VALB" ]; then

                
                if [ $MOVEMODE -eq 1 ]; then

                    #If specified move
                    echo "Moving duplicate ${FOUNDFILES[$COUNT2]} $MOVEDIR";
                    mv ${FOUNDFILES[$COUNT2]} $4;
                else
                    #Otherwise just show match
                    echo "${FOUNDFILES[$COUNT]} = ${FOUNDFILES[$COUNT2]}";
                fi
            fi
        fi

        COUNT2=$((COUNT2+1));
    done

    COUNT=$((COUNT+1));
done
