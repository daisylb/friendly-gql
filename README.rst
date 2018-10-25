friendly-gql
============

A friendlier, more concise GraphQL server library for Python, using type annotations.

This is a very early work in progress, but the goal is that code like this in Graphene:

.. code-block:: python

    class CreatePerson(graphene.Mutation):
        class Arguments:
            name = graphene.String()

        ok = graphene.Boolean()
        person = graphene.Field(lambda: Person)

        def mutate(self, info, name):
            person = Person(name=name)
            ok = True
            return CreatePerson(person=person, ok=ok)

...can instead be written like this:

.. code-block:: python

    def create_person(name: str) -> {'ok': bool, 'person': Person}:
        return {'ok': True, 'person': Person(name=name)}

Setting up a development environment
------------------------------------

.. code-block:: sh

    # install poetry: https://poetry.eustace.io/docs/#installation
    poetry install
    poetry run pytest