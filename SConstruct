###############################################################################
##
##  Copyright (C) 2012-2015 Tavendo GmbH
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

SVG_FILES = [
   ## Spec Figures
   ##
   'appcode.svg',
   'sessions.svg',
   'sessions2.svg',
   'sessions3.svg',
   'sessions4.svg',
   'hello.svg',
   'hello_denied.svg',
   'hello_authenticated.svg',
   'goodbye.svg',
   'pubsub_publish1.svg',
   'pubsub_publish2.svg',
   'pubsub_subscribe1.svg',
   'pubsub_subscribe2.svg',
   'rpc_call1.svg',
   'rpc_call2.svg',
   'rpc_cancel1.svg',
   'rpc_cancel2.svg',
   'rpc_progress1.svg',
   'rpc_register1.svg',
   'rpc_register2.svg',

   ## Unified Routing
   ##
   'unified_routing_broker_dealer.svg',
   'unified_routing_pubsub_broker.svg',
   'unified_routing_rpc_client_server.svg',
   'unified_routing_rpc_dealer.svg',
   'unified_routing_wamp_iot.svg',

   ## WAMP logos
   ##
   'wamp_logo.svg',
   'wamp_logo_tiny.svg',
   'wamp_logo_tiny_white.svg',
   'li_edge.svg',

   ## Misc
   ##
   '3rd_party_logos/record-evolution.svg',
   '3rd_party_logos/computer-associates.svg',
   '3rd_party_logos/tavendo.svg',
   '3rd_party_logos/kitware.svg',
   '3rd_party_logos/logo_genesi_wampws_site.svg'
]

IMG_SOURCE_DIR = "visuals/wamp2"
IMG_GEN_DIR    = "website/wampws/static/img/gen"

# Directory to be uploaded to Amazon S3 bucket
UPLOAD_DIR = 'website/wampws/build'

# Contains fingerprints of uploaded files
UPLOADED_DIR = 'website/wampws/build_uploaded'

# The Tavendo Amazon S3 Bucket to upload to
BUCKET = 'wamp.ws'

# The Bucket Prefix to upload files to
BUCKET_PREFIX = ''


###
### Do not touch below this unless you know what you are doing;)
###

import os
import pkg_resources

taschenmesser = pkg_resources.resource_filename('taschenmesser', '..')

## use this for Taschenmesser development only
#taschenmesser = "../../infrequent/taschenmesser"
#taschenmesser = "../../../taschenmesser"

env = Environment(tools = ['default', 'taschenmesser'],
                  toolpath = [taschenmesser],
                  ENV  = os.environ)


# Process SVGs
#
imgs = env.process_svg(SVG_FILES, IMG_SOURCE_DIR, IMG_GEN_DIR)

Alias("img", imgs)


# Upload to Amazon S3
#
uploaded = env.s3_dir_uploader(UPLOADED_DIR, UPLOAD_DIR, BUCKET, BUCKET_PREFIX)

Depends(uploaded, imgs)

Clean(uploaded, UPLOADED_DIR)

Alias("upload", uploaded)
