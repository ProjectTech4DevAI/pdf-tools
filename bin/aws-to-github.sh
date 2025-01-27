#!/bin/bash

ROOT=`git rev-parse --show-toplevel`

_workflows=(
    zerox/openai_gpt-4o
    # marker/default
)

while getopts 's:d:b:i:h' option; do
    case $option in
        s) _pdfs="$OPTARG" ;;
        d) _markdowns=$OPTARG ;;
	b) _bucket=$OPTARG ;;
	i) _instance=$OPTARG ;;
        h)
            cat <<EOF
Usage: $0
 -s Local source directory containing PDFs (optional)
 -d Github repository for Markdown destination
 -b AWS bucket containing PDFs (must have s3:// prefix)
EOF
            exit 0
            ;;
        *)
            echo -e Unrecognized option \"$option\"
            exit 1
            ;;
    esac
done

if [ ! $_pdfs ]; then
    _pdfs=`mktemp --directory`
fi

aws s3 sync $_bucket $_pdfs/ --no-progress --delete
for i in ${_workflows[@]}; do
    dst=$_markdowns/$i
    model=$(dirname $i)

    find $dst -name '*.md' \
	| while read; do
	md=$(realpath --relative-to=$dst "$REPLY")
	src="$_pdfs/$md"
	src=$(sed -e's/\.md/.pdf/' <<< "$src")
	if [ ! -f "$src" ]; then
	    (cd $dst && git rm "$md")
	fi
    done
    $ROOT/bin/run.sh -s $_pdfs -d $_markdowns -m $model

    (cd $_markdowns \
	 && git add $i \
	 && git commit -m "Document add/removal using $model"
    )
done

if [ $_instance ]; then
    aws ec2 stop-instances --instance-id $_instance
fi
