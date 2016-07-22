#!/bin/bash
mkdir -p common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/warc/
mkdir -p common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wat/
mkdir -p common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wet/

ccfiles=(
     'common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/warc/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.gz'
     'common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wat/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wat.gz'
     'common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wet/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wet.gz'
     'crawl-data/CC-MAIN-2016-26/segments/1466783391519.0/warc/CC-MAIN-20160624154951-00000-ip-10-164-35-72.ec2.internal.warc.gz'
   );

for f in ${ccfiles[@]}
do
  mkdir -p `dirname $f`
  echo "Downloading `basename $f` ..."
  echo "---"
  wget https://aws-publicdatasets.s3.amazonaws.com/$f -O $f
done
