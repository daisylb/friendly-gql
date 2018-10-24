# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import graphql as gql
from graphql.type.definition import GraphQLType
import typing as t


def convert_type(type: t.Any) -> t.Optional[GraphQLType]:
    if type is str:
        return gql.GraphQLNonNull(gql.GraphQLString)
    if type is int:
        return gql.GraphQLNonNull(gql.GraphQLInt)
    return None


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
