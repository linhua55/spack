##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Schema for mirror configuration files."""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack module file configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'definitions': {
        'array_of_strings': {
            'type': 'array',
            'default': [],
            'items': {
                'type': 'string'
            }
        },
        'dictionary_of_strings': {
            'type': 'object',
            'patternProperties': {
                r'\w[\w-]*': {  # key
                    'type': 'string'
                }
            }
        },
        'dependency_selection': {
            'type': 'string',
            'enum': ['none', 'direct', 'all']
        },
        'module_file_configuration': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': {
                'filter': {
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'properties': {
                        'environment_blacklist': {
                            'type': 'array',
                            'default': [],
                            'items': {
                                'type': 'string'
                            }
                        }
                    }
                },
                'autoload': {
                    '$ref': '#/definitions/dependency_selection'},
                'prerequisites': {
                    '$ref': '#/definitions/dependency_selection'},
                'conflict': {
                    '$ref': '#/definitions/array_of_strings'},
                'load': {
                    '$ref': '#/definitions/array_of_strings'},
                'suffixes': {
                    '$ref': '#/definitions/dictionary_of_strings'},
                'environment': {
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'properties': {
                        'set': {
                            '$ref': '#/definitions/dictionary_of_strings'},
                        'unset': {
                            '$ref': '#/definitions/array_of_strings'},
                        'prepend_path': {
                            '$ref': '#/definitions/dictionary_of_strings'},
                        'append_path': {
                            '$ref': '#/definitions/dictionary_of_strings'}
                    }
                }
            }
        },
        'module_type_configuration': {
            'type': 'object',
            'default': {},
            'anyOf': [
                {'properties': {
                    'hash_length': {
                        'type': 'integer',
                        'minimum': 0,
                        'default': 7
                    },
                    'whitelist': {
                        '$ref': '#/definitions/array_of_strings'},
                    'blacklist': {
                        '$ref': '#/definitions/array_of_strings'},
                    'naming_scheme': {
                        'type': 'string'  # Can we be more specific here?
                    }
                }},
                {'patternProperties': {
                    r'\w[\w-]*': {
                        '$ref': '#/definitions/module_file_configuration'
                    }
                }}
            ]
        }
    },
    'patternProperties': {
        r'modules:?': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': {
                'prefix_inspections': {
                    'type': 'object',
                    'patternProperties': {
                        # prefix-relative path to be inspected for existence
                        r'\w[\w-]*': {
                            '$ref': '#/definitions/array_of_strings'}}},
                'enable': {
                    'type': 'array',
                    'default': [],
                    'items': {
                        'type': 'string',
                        'enum': ['tcl', 'dotkit', 'lmod']}},
                'lmod': {
                    'allOf': [
                        # Base configuration
                        {'$ref': '#/definitions/module_type_configuration'},
                        {
                            'core_compilers': {
                                '$ref': '#/definitions/array_of_strings'
                            },
                            'hierarchical_scheme': {
                                '$ref': '#/definitions/array_of_strings'
                            }
                        }  # Specific lmod extensions
                    ]},
                'tcl': {
                    'allOf': [
                        # Base configuration
                        {'$ref': '#/definitions/module_type_configuration'},
                        {}  # Specific tcl extensions
                    ]},
                'dotkit': {
                    'allOf': [
                        # Base configuration
                        {'$ref': '#/definitions/module_type_configuration'},
                        {}  # Specific dotkit extensions
                    ]},
            }
        },
    },
}
