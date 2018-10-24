# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import convert
import graphql as gql
import typing as t


def test_convert_type():
    converted = convert.convert_type(int)
    assert isinstance(converted, gql.GraphQLType)


def test_convert():
    def function(foo: int, bar: int) -> str:
        return f"{foo} {bar}"

    query_type = gql.GraphQLObjectType(
        "Query", {"function": convert.convert_function(function)}
    )
    schema = gql.GraphQLSchema(query=query_type)
    result = gql.graphql_sync(
        schema,
        """
        query {
            function(foo: 1, bar: 2)
        }
        """,
    )
    assert result.data == {"function": "1 2"}

def test_convert_optional():
    def function(arg: int) -> t.Optional[int]:
        if arg > 0:
            return arg
        return None

    query_type = gql.GraphQLObjectType(
        "Query", {"function": convert.convert_function(function)}
    )
    schema = gql.GraphQLSchema(query=query_type)
    result = gql.graphql_sync(
        schema,
        """
        query {
            function(arg: -1)
        }
        """,
    )
    assert result.data == {"function": None}