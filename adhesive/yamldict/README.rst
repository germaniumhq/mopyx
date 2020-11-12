``Yamldict`` is a library that allows accessing YAML content as a kind
of a dictionary. Its primary purpose is to allow reading and writing
YAML content with ease.

To achieve that it has the following features:

Features
========

1. Easy creation of complex structures from string or files:

   .. code:: python

       myyaml = yamldict.create("""
       - "item 1"
       - "item 2"
       """)

2. Not a dictionary. That means a property such as ``get`` is still
   accessible from the object and isn’t a method on a dictionary.

   .. code:: python

       >>> x = yamldict.YamlDict()
       >>> x.get = "x"
       >>> x
       YamlDict() {'get': 'x'}

3. Accessible via properties, or indexes:

   .. code:: python

       assert myyaml["item"] == myyaml.item

4. Handles chained missing properties without creating them unless
   asked:

   .. code:: python

       >>> myyaml = yamldict.YamlDict()
       >>> assert not myyaml.this.property.doesnt.exist
       >>> myyaml
       YamlDict() {}
       >>> myyaml.some.other.property = "3"
       >>> myyaml
       YamlDict() {'some': {'other': {'property': '3'}}}

5. It supports deep copying.

6. It’s integrated as a PyYaml serializer.

7. It supports pickle serialization.

8. Type support, so you don’t need to do anything in projects using
   mypy.
