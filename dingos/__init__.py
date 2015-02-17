# Copyright (c) Siemens AG, 2013
#
# This file is part of MANTIS.  MANTIS is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2
# of the License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import re



__version__ = '0.3.0'

REVISION = __version__


# Below, default values used in DINGO are defined.


# Dingos allows for extensions with another template basis othan the
# Grappelli templates that are used by default. Such an extension
# would have to create a 'dingos/templates/<extension_name>' directory
# and reimplement the existing Dingos template structure in that
# directory.

DINGOS_TEMPLATE_FAMILY  = 'grappelli'

# The namespace uri should be used for qualifying identifiers if
# neither namespace nor namespace uri is explicitly provided for an identifier.

DINGOS_DEFAULT_ID_NAMESPACE_URI = 'enter.a.value.in.settings'


# The DINGOS_MISSING_ID_NAMESPACE_URI_PREFIX should be used s prefix for namespace
# information used in identifiers for which no namespace uri can be determined.

DINGOS_MISSING_ID_NAMESPACE_URI_PREFIX = 'https://github.com/siemens/django-dingos/wiki/namespaces_identifiers_missing'


# The DINGOS_NAMESPACE is used as default namespace for
# datatypes and information-object types created by DINGO.

DINGOS_NAMESPACE_URI = 'https://github.com/siemens/django-dingos/wiki/namespaces_dingos_types'
DINGOS_NAMESPACE_SLUG = 'DingosDefaultNameSpace'

DINGOS_DEFAULT_FACT_DATATYPE = 'String'

# The DINGOS_ID_NAMESPACE_URI is used as qualifier for identifiers
# of internal objects created by DINGO, such as information
# objects containing meta data of relations.

DINGOS_ID_NAMESPACE_URI = 'https://github.com/siemens/django-dingos/wiki/namespaces_dingos_identifiers'
DINGOS_ID_NAMESPACE_SLUG = 'DingosDefaultIdNameSpace'


# The DINGOS_GENERIC_FAMILY is used to provide a default family name for generic imports

DINGOS_GENERIC_FAMILY_NAME = 'generic'

# The DINGOS_IOBJECT_FAMILY_NAME is used as family name for all internally created objects
# such as PLACEHOLDERS that should by default be visible to a normal user.


DINGOS_IOBJECT_FAMILY_NAME = 'DINGOS'

# The DINGOS_INTERNAL_IOBJECT_FAMILY_NAME is used as family name for all internally created objects
# such as USER_CONFIGURATION, SAVED_SEARCHES, etc. that should by default not be visible to a normal user.
# of internally created information objects.

DINGOS_INTERNAL_IOBJECT_FAMILY_NAME = 'DINGOS_internal'

# We Dingo's revision both as revision for families and object types
# of internally created information objects.


DINGOS_REVISION_NAME = REVISION

# Below, we define names used for internally created objects:

DINGOS_RELATION_TYPE_FACTTERM_NAME = '@@RelationType'

DINGOS_RELATION_METADATA_OBJECT_TYPE_NAME = 'RelationMetadata'

DINGOS_PLACEHOLDER_TYPE_NAME = 'PLACEHOLDER'

DINGOS_DEFAULT_IMPORT_MARKING_TYPE_NAME = "ImportInfo"


DINGOS_USER_DATA_TYPE_NAME = 'USER_DATA'

DINGOS_USER_PREFS_TYPE_NAME = 'USER_PREFS'

DINGOS_SAVED_SEARCHES_TYPE_NAME = 'SAVED_SEARCHES'


# Values larger than DINGOS_MAX_VALUE_SIZE_WRITTEN_TO_DB are
# not written to the data base but stored on the file system or
# written to a special blob table

DINGOS_MAX_VALUE_SIZE_WRITTEN_TO_VALUE_TABLE = 2048


# values for the LARGE_VALUE_DESTINATION are 'BLOB_TABLE' and 'FILE_SYSTEM'

DINGOS_VALUES_TABLE = 0
DINGOS_FILE_SYSTEM = 1
DINGOS_BLOB_TABLE = 2

DINGOS_LARGE_VALUE_DESTINATION = DINGOS_BLOB_TABLE



# The DINGOS_BLOB_ROOT absolutely has to be set in the DINGOS settings.
# If that is not the case, the attempt to read the value from the settings

DINGOS_BLOB_ROOT = None

# read_settings.py will instantiate the DINGOS_BLOB_STORAGE with a file storage handler
# that can also be used by importers to write file content to disk.

DINGOS_BLOB_STORAGE = None

DINGOS_DEFAULT_USER_PREFS = {
    'dingos' : { 'widgets' :
                     {'embedded_in_objects' :
                          {'lines' : {'@description': """Max. number of objects displayed in
                                                        widget listing the objects in which the
                                                        current object is embedded.""",
                                      '_value' : '5'}
                          } ,
                      },
                 'view' :
                     {'pagination':
                          {'lines' : {'@description': """Max. number of lines displayed in
                                                    paginated views.""",
                                      '_value' : '20'},
                           },
                      'orientation' : {'@description': """Layout orientation. Possible values are 'vertical' and
                                                          'horizontal'.""",
                                       '_value' : 'horizontal'}
                     }

    }
}

# It does not make sense to specifiy default saved searches here (anyhow, the specification of
# saved searches via the defaults is more to show the concept of saved searches than for
# actual use. To specify saved searches in the settings file under ``DINGOS`` settings,
# do as follows::
#
#  ...
#    'DINGOS_DEFAULT_SAVED_SEARCHES' : {
#        'dingos' : [
#            { 'priority' : "0",
#              'title' : 'Filter for STIX Packages',
#              'view' : 'url.dingos.list.infoobject.generic',
#              'parameter' : 'iobject_type=72',
#              }
#        ],
#        }
#  ...
#
#

DINGOS_DEFAULT_SAVED_SEARCHES = {'dingos': []}


# Allowed keys for query conditions

DINGOS_QUERY_ALLOWED_KEYS = {}




DINGOS_QUERY_ALLOWED_KEYS['object'] = (
    ("^import_timestamp$","create_timestamp"),
    ("^timestamp$","timestamp"),
    ("^identifier\.namespace$","identifier.namespace.uri"),
    ("^name$","name"),
    ("^object_type\.name$","iobject_type.name"),
    ("^object_type\.namespace$","iobject_type.namespace.uri"),
    ("^identifier\.uid$","identifier.uid"),
    ("^object_family$","iobject_family.name")
   )

DINGOS_QUERY_ALLOWED_KEYS['fact'] = (
    ("^@\[.*\]$","\g<0>"),
    ("^\[.*\]","\g<0>"),
    ("^fact_term$","fact_term.term"),
    ("^value$","fact_values.value"),
    ("^attribute$","fact_term.attribute")
    )

# Allowed columns for query result formatting
DINGOS_QUERY_ALLOWED_COLUMNS = {}

DINGOS_QUERY_ALLOWED_COLUMNS['InfoObject'] = {
    "import_timestamp": ("create_timestamp",[]),
    "timestamp": ("timestamp",[]),
    "name": ("name",[]),
    "identifier": ("identifier",['identifier','identifier__namespace']),
    "identifier.uid": ("identifier.uid",['identifier']),
    "identifier.namespace": ("identifier.namespace.uri",['identifier__namespace']),
    "object_type": ("iobject_type",['iobject_type','iobject_type__namespace']),
    "object_type.name": ("iobject_type.name",['iobject_type']),
    "object_type.namespace": ("iobject_type.namespace.uri",['iobject_type__namespace']),
    "object_family": ("iobject_family.name",['iobject_family']),
}

DINGOS_QUERY_ALLOWED_COLUMNS['InfoObject2Fact'] = {
    "fact_term": ("fact.fact_term.term",['fact__fact_term']),
    "fact_term_with_attribute": ("fact.fact_term",['fact__fact_term']),
    "value": ("fact.fact_values.value",["fact__fact_values"]),
    "attribute": ("fact.fact_term.attribute",['fact__fact_term']),
    "object.import_timestamp": ("iobject.create_timestamp",['iobject']),
    "object.timestamp": ("iobject.timestamp",['iobject']),
    "object.identifier.namespace": ("iobject.identifier.namspace.uri",['iobject__identifier__namespace']),
    "object.name": ("iobject.name",['iobject']),
    "object.object_type.name": ("iobject.iobject_type.name",['iobject__iobject_type']),
    "object.object_type.namespace": ("iobject.iobject_type.namespace.uri",['iobject__iobject_type.namespace']),
    "object.identifier.uid": ("iobject.identifier.uid",['iobject__identifier']),
    "object.object_family": ("iobject.iobject_family",['iobject__iobject_family']),
    "object.identifier": ("iobject.identifier",['iobject__identifier','iobject__identifier__namespace']),
    "object.object_type": ("iobject.iobject_type",['iobject__iobject_type','iobject__iobject_type__namespace']),
}

# DINGOS_OBJECTTYPE_ICON_MAPPING
#
# A mapping used to associate InfoObject types with icons
# that are displayed in the graph view.
#
# The InfoObject-type icon mapping has the form::
#
#     { <object-type namespace uri> : {<object-type name>) : <image info dict>,
#                                     ...},
#        ...
#     }
#
# where the image-info dict is a key-value mapping of image attributes like so::
#
#      {'xlink:href': "/static/img/...',
#        'x': -15,
#        'y': -15,
#        'width': 30,
#        'height' : 30
#      }
#

DINGOS_OBJECTTYPE_ICON_MAPPING = {}


# DINGOS_OBJECTTYPE_VIEW_MAPPING
#
# A mapping used to associate InfoObject types with specialized views
#
# The InfoObject-type icon mapping has the form::
#
#     { <object-type namespace uri> : {<object-type name>) : <view name>
#                                     ...},
#        ...
#     }


DINGOS_OBJECTTYPE_VIEW_MAPPING = {}


# DINGOS_OBJECTTYPE_ICON_RELIST_MAPPING
#
# Used to find map an InfoObject type to an icon,
# in case the DINGOS_OBJECTTYPE_ICON_MAPPING yielded
# no result.
#
# The mapping has the form::
#
#     { <object-type namespace uri> : [(<regexp>, <image info dict>),
#                                     ...],
#        ...
#     }
#
# where the regular expression is to match on Infoobject type names and
# the image-info dict is a key-value mapping of image attributes like so::
#
#      {'xlink:href': "/static/img/...',
#        'x': -15,
#        'y': -15,
#        'width': 30,
#        'height' : 30
#      }
#

DINGOS_OBJECTTYPE_ICON_RELIST_MAPPING = {}


# Registry for exporters

DINGOS_SEARCH_POSTPROCESSOR_REGISTRY = {}

DINGOS_SEARCH_EXPORT_MAX_OBJECTS_PROCESSING = 5000


DINGOS_INFOOBJECT_GRAPH_TYPES = [{'info_object_family_re':   r'.*',
                                  'info_object_type_re':      r'.*',
                                  'default_mode':           'up_and_down',
                                  'available_modes':        [{'mode_key':           'up_and_down',
                                                              'menu_name':          'Up+Down',
                                                              'title':              'Up&Down',
                                                              'description':        'Follow references up and down',
                                                              'traversal_args':     {'direction': 'both',
                                                                                     'max_nodes': 150},
                                                              'postprocessor':      'mantis_stix_importer.graph_postprocessors.standard_postprocessor'},
                                                             {'mode_key':           'full',
                                                              'menu_name':          'Full',
                                                              'title':              'Full',
                                                              'description':        'Full graph traversal.',
                                                              'traversal_args':     {'direction': 'full',
                                                                                     'max_nodes': 150},
                                                              'postprocessor':      'mantis_stix_importer.graph_postprocessors.standard_postprocessor'
                                                              },
                                                             {'mode_key':           'up',
                                                              'menu_name':          'Up',
                                                              'title':              'Up',
                                                              'description':        'Follow references up.',
                                                              'traversal_args':     {'direction': 'up',
                                                                                     'max_nodes': 150,
                                                                                     'reverse_direction': True},
                                                              'postprocessor':      'mantis_stix_importer.graph_postprocessors.standard_postprocessor'},
                                                             {'mode_key':           'down',
                                                              'menu_name':          'Down',
                                                              'title':              'Down Graph',
                                                              'description':        'Follow references down.',
                                                              'traversal_args':     {'direction': 'down',
                                                                                     'max_nodes': 150},
                                                              'postprocessor':      'mantis_stix_importer.graph_postprocessors.standard_postprocessor'},
                                                             {
                                                                 'mode_key' : 'corr_auto',
                                                                 'menu_name' : 'Corr. auto',
                                                                 'title' : 'Correlation',
                                                                 'description' : 'Show correlations with other InfoObjects',
                                                                 'traversal_args' : {'direction' : 'down',
                                                                                     'max_nodes' : 0},
                                                                 'postprocessor' : 'mantis_malte.correlation_postprocessor',
                                                                 'postprocessor_args' : {'unfolding': 'auto'}

                                                                 },
                                                                                                                          {
                                                                 'mode_key' : 'corr_small',
                                                                 'menu_name' : 'Corr S',
                                                                 'title' : 'Correlation (Small)',
                                                                 'description' : 'Show correlations with other InfoObjects, only displaying '
                                                                                 'the correlated top-level objects; the correlation is symbolized '
                                                                                 'with a red edge',
                                                                 'traversal_args' : {'direction' : 'down',
                                                                                     'max_nodes' : 0},
                                                                 'postprocessor' : 'mantis_malte.correlation_postprocessor',
                                                                 'postprocessor_args' : {'unfolding': 'minimal'}

                                                                 },
                                                                                                                                                                                       {
                                                                 'mode_key' : 'corr_medium',
                                                                 'menu_name' : 'Corr M',
                                                                 'title' : 'Correlation (Medium)',
                                                                 'description' : 'Show correlations with other InfoObjects, displaying the '
                                                                                 'correlated objects (linked with a red edge) that have been found with direct link '
                                                                                 'to the top level object(s) from which they are reachable.',
                                                                 'traversal_args' : {'direction' : 'down',
                                                                                     'max_nodes' : 0},
                                                                 'postprocessor' : 'mantis_malte.correlation_postprocessor',
                                                                 'postprocessor_args' : {'unfolding': 'concise'}

                                                                 },
                                                                                                                                                                                                                                                    {
                                                                 'mode_key' : 'corr_large',
                                                                 'menu_name' : 'Corr L',
                                                                 'title' : 'Correlation (Large)',
                                                                 'description' : 'Show correlations with other InfoObjects, displaying the '
                                                                                 'correlated objects that have been found (linked with a red edge) '
                                                                                 'along with intermediate objects between the corresponding top-level '
                                                                                 'objects.',
                                                                 'traversal_args' : {'direction' : 'down',
                                                                                     'max_nodes' : 0},
                                                                 'postprocessor' : 'mantis_malte.correlation_postprocessor',
                                                                 'postprocessor_args' : {'unfolding': 'full'}

                                                                 }
                                                             ]}]

#if tags should match specific requirements, add regex to check here
DINGOS_TAGGING_REGEX = [
     re.compile(r"^INVES-[0-9]+(-[A-Za-z0-9]+)?$")
]


DINGOS_MANTIS_ACTIONABLES_CONTEXT_TAG_REGEX = [
    re.compile(r"^INVES-[0-9]+(-[A-Za-z0-9]+)?$")
]


DINGOS_TAGGING_PROCESSING = {
    'dingos' : 'dingos.view_classes.processTagging',
    'actionables' : 'mantis_actionables.views.processActionablesTagging'
}



DINGOS_TAGGING_POSTPROCESSING = {'Fact':'mantis_actionables.mantis_import.update_and_transfer_tags'}


