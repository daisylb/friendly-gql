# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import graphql as gql
from graphql.type.definition import GraphQLType
import typing as t
import typing_inspect

NoneType = type(None)

converter_registry = []


@converter_registry.append
def convert_scalars(type) -> t.Optional[GraphQLType]:
    if type is str:
        return gql.GraphQLString
    if type is int:
        return gql.GraphQLInt
    return None


def extract_optional(type):
    """If this is a type wrapped in an Optional, return it.

    Else, return None.
    """

    if typing_inspect.is_union_type(type):
        args = typing_inspect.get_args(type)
        if len(args) != 2:
            return None
        if args[0] is NoneType:
            return args[1]
        if args[1] is NoneType:
            return args[0]


def convert_type(type: t.Any) -> t.Optional[GraphQLType]:
    # special handling for typing.Optional
    
    nullable = False
    optional_inner_type = extract_optional(type)
    if optional_inner_type is not None:
        nullable = True
        type = optional_inner_type

    for converter in converter_registry:
        gql_type = converter(type)
        if gql_type is not None:
            break
    else:
        return None

    if not nullable:
        gql_type = gql.GraphQLNonNull(gql_type)

    return gql_type


def convert_function(function: t.Callable) -> gql.GraphQLField:
    gql_return_type = convert_type(function.__annotations__["return"])
    gql_args = {
        name: gql.GraphQLArgument(convert_type(annotation))
        for name, annotation in function.__annotations__.items()
        if name != "return"
    }

    def resolver(root, info, **kwargs):
        return function(**kwargs)

    return gql.GraphQLField(gql_return_type, args=gql_args, resolve=resolver)
