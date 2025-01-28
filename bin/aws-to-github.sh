#!/bin/bash

ROOT=`git rev-parse --show-toplevel`

source $ROOT/venv/bin/activate || exit 1

_scripts=$ROOT/src/build
_workflows=(
    zerox/openai_gpt-4o
    # marker/default # run on g4dn.4xlarge
)
_automator=`basename $ROOT`

while getopts 's:d:b:i:h' option; do
    case $option in
        s) _pdfs="$OPTARG" ;;
        d) _markdowns=$OPTARG ;;
        b) _bucket=$OPTARG ;;
        i) _instance=$OPTARG ;;
        h)
            cat <<EOF
Usage: $0
 -d Github repository that will act as a destination for
    generated Markdown's.
 -b AWS bucket containing PDFs (must have s3:// prefix).
 -s [optional] Local source directory containing PDFs. If
    not specified all files from S3 will be downloaded.
 -i [optional] The E2 instance on which this script is
    being run. Specifying this option will shut the
    instance down once this script is complete.
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
# Download files from S3 to the local storage location
#
aws s3 sync $_bucket $_pdfs/ --no-progress --delete || exit 1

#
# The destination is assumed to be a Github repository. This prep's
# the repository for the forthcoming Markdown output.
#
(cd $_markdowns \
     && git switch main \
     && git checkout -b $_automator/`date +%Y%m%d-%H%M%S`
) || exit 1

#
# Generate the Markdown's!
#
for i in ${_workflows[@]}; do
    dst=$_markdowns/$i
    mkdir --parents $dst
    model=$(dirname $i)

    # Remove files that exist in the destination (Github) but not
    # S3. The destination will become a mirror of S3: non existent S3
    # files are assumed not to exist for a reason.
    c_lock=`mktemp`
    find $dst -name '*.md' \
        | while read; do
        md=$(realpath --relative-to=$dst "$REPLY")
        src="$_pdfs/$md"
        src=$(sed -e's/\.md/\.pdf/' <<< "$src")
        if [ ! -f "$src" ]; then
            (cd $dst && git rm "$md")
            echo $REPLY >> $c_lock
        fi
    done
    if [ `stat --printf=%s $c_lock` -gt 0 ]; then
        (cd $_markdowns \
            && git commit \
                   --all \
                   --message="Document removal using $_automator:$model"
        )
    fi
    rm $c_lock

    # Pick the Markdown conversion process and run it
    params="--source $_pdfs --destination $dst"
    case $model in
        zerox) python $_scripts/_zerox/run.py $params --model gpt-4o ;;
        marker) python $_scripts/_marker/run.py $params ;;
        *)
            echo Unrecognized method \"$_method\"
            exit 1
            ;;
    esac

    # Add the files to Git
    (cd $_markdowns \
         && git add $i \
         && git commit \
                --all \
                --message="Document addition using $_automator:$model"
    )
done

#
# If an EC2 instance was specified, shut it down.
#
if [ $_instance ]; then
    aws ec2 stop-instances --instance-id $_instance
fi
