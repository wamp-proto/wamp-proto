###############################################################################
##
##  Copyright (C) 2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


import sys, os
from optparse import OptionParser

from boto.s3.connection import S3Connection
from boto.s3.key import Key


def percent_cb(complete, total):
   sys.stdout.write("%d %%\n" % round(100. * float(complete) / float(total)))
   sys.stdout.flush()


def upload_files(bucketname, srcdir):
   print bucketname, srcdir
   conn = S3Connection()
   bucket = conn.get_bucket(bucketname)

   for path, dir, files in os.walk(srcdir):
      for file in files:

         filekey = os.path.relpath(os.path.join(path, file), srcdir).replace('\\', '/')
         filepath = os.path.normpath(os.path.join(path, file))

         #print "filekey: ", filekey
         #print "filepath: ", filepath

         key = bucket.lookup(filekey)
         if key:
            fingerprint = key.etag.replace('"', '')
         else:
            fingerprint = None
            key = Key(bucket, filekey)

         fp = str(key.compute_md5(open(filepath, "rb"))[0])
         fs = os.path.getsize(filepath)

         if fingerprint != fp:
            print "Uploading file %s (%d bytes, %s MD5) .." % (filekey, fs, fp)
            key.set_contents_from_filename(filepath, cb = percent_cb, num_cb = 100)
            key.set_acl('public-read')
         else:
            print "File %s already on S3 and unchanged." % filekey


if __name__ == "__main__":
   parser = OptionParser()
   parser.add_option ("-b",
                      "--bucket",
                      dest = "bucket",
                      help = "Amazon S3 bucket name.")

   parser.add_option ("-d",
                      "--directory",
                      dest = "directory",
                      help = "Directory to upload.")

   (options, args) = parser.parse_args ()

   directory = os.path.join(os.path.dirname(__file__),  options.directory)

   upload_files(options.bucket, directory)
