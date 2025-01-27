#!/bin/bash

ROOT=`git rev-parse --show-toplevel`

export OPENAI_API_KEY=`cat $ROOT/open-ai.key`
source $ROOT/venv/bin/activate

_scripts=$ROOT/src/build
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

#
#
#
aws s3 sync $_bucket $_pdfs/ --no-progress --delete || exit 1

#
#
#
(cd $_markdowns \
     && git switch main \
     && git checkout -b $_automator/`date +%Y%m%d-%H%M%S`
) || exit 1

#
#
#
for i in ${_workflows[@]}; do
    dst=$_markdowns/$i
    mkdir --parents $dst
    model=$(dirname $i)

    rm --force $_commit_lock
    find $dst -name '*.md' \
	| while read; do
	md=$(realpath --relative-to=$dst "$REPLY")
	src="$_pdfs/$md"
	src=$(sed -e's/\.md/.pdf/' <<< "$src")
	if [ ! -f "$src" ]; then
	    (cd $dst && git rm "$md")
	    touch $_commit_lock
	fi
    done
    if [ -e $_commit_lock ]; then
	(cd $_markdowns \
	    && git commit \
		   --all \
		   --message="Document removal using $_automator:$model"
	)
    fi

    params="--source $_pdfs --destination $dst"
    case $model in
	zerox) python $_scripts/_zerox/run.py $params --model gpt-4o ;;
	marker) python $_scripts/_marker/run.py $params ;;
	*)
	    echo Unrecognized method \"$_method\"
	    exit 1
	    ;;
    esac

    (cd $_markdowns \
	 && git add $i \
	 && git commit \
		--all \
		--message="Document addition using $_automator:$model"
    )
done

if [ $_instance ]; then
    aws ec2 stop-instances --instance-id $_instance
fi
