Alternative to reload().
This works by executing the module in a scratch namespace, and then
patching classes, methods and functions in place.  This avoids the
need to patch instances.  New objects are copied into the target
namespace.
Some of the many limitiations include:
- Code using metaclasses is not handled correctly
- Code creating global singletons is not handled correctly
- Functions and methods using decorators (other than classmethod and
  staticmethod) is not handled correctly
- Dependent modules are not reloaded
- When a dependent module contains 'from foo import bar', and
  reloading foo deletes foo.bar, the dependent module continues to use
  the old foo.bar object rather than failing
- Frozen modules and modules loaded from zip files aren't handled
  correctly
- Classes involving __slots__ are not handled correctly. Only support slots class to slots class non-data members change.
