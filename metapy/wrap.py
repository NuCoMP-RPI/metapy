from py4j.protocol import Py4JError, Py4JJavaError, register_output_converter, REFERENCE_TYPE
from py4j.java_collections import JavaList
from py4j.java_gateway import JavaObject
from re import compile, sub, search
from enum import Enum
from metapy.gateway import gateway, is_instance_of, get_documentation
from metapy.util import camel_to_snake_case

override_sets = {'mcnpy': {},
                'serpy': {},
                'kenopy': {}}

# Object meaning java.lang.Object
_OBJECT_METHODS = ('clone', 
                   'equals', 
                   'finalize', 
                   'getClass', 
                   'hashCode', 
                   'notify', 
                   'notifyAll', 
                   'toString', 
                   'wait')
_NOTIFIER_METHODS = ('eAdapters', 'eDeliver', 'eNotify', 'eSetDeliver')
_E_OBJECT_METHODS = ('eResource', 
                     'eContainer', 
                     'eContainingFeature', 
                     'eContainmentFeature', 
                     'eContents',
                     'eAllContents',
                     'eCrossReferences',
                     'eClass',
                     'eGet',
                     'eSet',
                     'eIsSet',
                     'eUnset',
                     'eIsProxy')
_INTERNAL_E_OBJECT_METHODS = ('eBaseStructuralFeatureID',
                              'eBasicRemoveFromContainer',
                              'eBasicSetContainer',
                              'eContainerFeatureID',
                              'eDerivedOperationID',
                              'eDerivedStructuralFeatureID',
                              'eDirectResource',
                              'eGet',
                              'eInternalContainer',
                              'eInternalResource',
                              'eInverseAdd',
                              'eInverseRemove',
                              'eInvoke',
                              'eIsSet',
                              'eNotificationRequired',
                              'eObjectForURIFragmentSegment',
                              'eProxyURI',
                              'eResolveProxy',
                              'eSet',
                              'eSetClass',
                              'eSetProxyURI',
                              'eSetResource',
                              'eSetStore',
                              'eSetting',
                              'eStore',
                              'eUnset',
                              'eURIFragmentSegment')
_E_MODEL_ELEMENT_METHODS = ('getEAnnotation', 'getEAnnotations')
_E_FACTORY_METHODS = ('convertToString',
                      'create',
                      'createFromString',
                      'getEPackage',
                      'setEPackage')
#TODO: Generalize to other packages
_DOC_PATTERNS = (compile('<em>[\w\s_]*</em>}'),
                compile('#get[A-Z][\w_]*\s<em>'),
                compile('#is[A-Z][\w_]*\s<em>'),
                (compile('<\/?\w*>'), ''),
                (compile('{@link\s[\w.#]*\s'), ''),
                (compile('}\s:\s'), ' : '),
                (compile('{@link\sgov.lanl.mcnp.mcnp'), 'mcnpy'),
                (compile('{@link\sfi.vtt.serpent.serpent'), 'serpy'),
                (compile('}'), ''),
                (compile('EList of'), 'iterable of'))
                #(compile(':\sString'), ': str'),
                #(compile(':\sdouble'), ': float'))

# Used as a function in the output converter.
def wrap_e_object(target_id, gateway_client, wrappers, package):
    #print(inspect.stack(context=1), '\n')
    object = JavaObject(target_id, gateway_client)
    wrap_it = True
    """i = 0
    for frame in reversed(inspect.stack(context=1)):
        i = i + 1
        print(i, str(object))
        if frame is not None:
            if frame[4] is not None:
                if frame[4][0] == '        self._e_object = e_factory.create(e_class)\n':
                    wrap_it = False
                    break"""
    if wrap_it is True:
        # Use string to avoid infinite loop.
        cls = str(object)
        if len(override_sets[package]) == 0:
            override_sets[package] = wrappers
        if cls.find('mcnp.impl') > 0:
            wrappers = override_sets['mcnpy']
        elif cls.find('serpent.impl') > 0:
            wrappers = override_sets['serpy']
        elif cls.find('keno.impl') > 0:
            wrappers = override_sets['kenopy']
        cls = cls[cls.find('impl.')+5:cls.find('Impl')]

    if wrap_it is True:
        if cls in wrappers:
            wrapped = wrappers[cls]()
            try:
                wrapped._e_object = object
                return wrapped
            except:
                return object
    return object

def delegate_methods(methods):
    """Delegate methods to `self._e_object`."""
    delegated_methods = {}
    for method in methods:
        def delegate_method(method=method):
            def delegated_method(self, *args, **kwargs):
                return getattr(self._e_object, method)(*args, **kwargs)
            return delegated_method
        delegated_methods[method] = delegate_method(method)
    return delegated_methods

#def delegation():
# These classes do nothing but delegate methods to self._e_object
Object = type('Object', (object,), delegate_methods(_OBJECT_METHODS))
Notifier = type('Notifier', (Object,), delegate_methods(_NOTIFIER_METHODS))
_e_object_body = delegate_methods(_E_OBJECT_METHODS)
_e_object_body['_e_object'] = None
EObject = type('EObject', (Notifier,), _e_object_body)
InternalEObject = type('InternalEObject', (EObject,), 
                        delegate_methods(_INTERNAL_E_OBJECT_METHODS))
#    return Object, Notifier, _e_object_body, EObject, InternalEObject

EModelElement = type('EModelElement', (InternalEObject,), 
                      delegate_methods(_E_MODEL_ELEMENT_METHODS))
EFactory = type('EFactory', (EModelElement,), 
                 delegate_methods(_E_FACTORY_METHODS))

# Setter decorators applied to all properties
def replace_if_contained(feature):
    """Replace previous containing reference with a copy of the value."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if is_instance_of(feature, EReference) and feature.isContainment():
                try:
                    containing_feature = value.eContainingFeature()
                except:
                    containing_feature = None
                if containing_feature is not None:
                    value_copy = gateway.copier.copy(value._e_object)
                    gateway.copier.copyReferences()
                    value.eContainer().eSet(containing_feature, value_copy._e_object)
            return setter(self, value)
        return setter_decorated
    return decorator

def is_enum(value, feature):
    """Originally within string_or_int_to_enum.
    Serparate so it can be used by set_e_list."""
    EAttribute = gateway.jvm.org.eclipse.emf.ecore.EAttribute
    if is_instance_of(feature, EAttribute):
        EEnum = gateway.jvm.org.eclipse.emf.ecore.EEnum
        data_type = feature.getEAttributeType()
        str_or_int = isinstance(value, str) or isinstance(value, int)
        if is_instance_of(data_type, EEnum) and str_or_int:
            # String enums require upper case.
            if isinstance(value, str):
                value = value.upper()
            literal = data_type.getEEnumLiteral(value)
            if literal is None:
                literal = data_type.getEEnumLiteralByLiteral(value)
            if literal is not None:
                value = literal.getInstance()
    return value

def string_or_int_to_enum(feature):
    """Replace string or int with enum if applicable."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            value = is_enum(value, feature)
            return setter(self, value)
        return setter_decorated
    return decorator

def return_value_converter(feature, value):
    # Some functions will return numerical values as strings. This is usually
    # because alternate options like a Jump need to be supported. We want the 
    # numbers as numbers while in Python. The exceptions to this are 'name' 
    # features and cases like libraries where leading zeros are possible.
    if isinstance(value, str) and feature.getName() != 'name':
        try:
            if float(value)%1 == 0:
                if int(value) != 0 and value.startswith('0') is False:
                    return int(value)
                elif int(value) == 0 and len(value) == 1:
                    return int(value)
                else:
                    return value
            else:
                return float(value)
        except ValueError:
            return value
    else:
        # Want to return the emum literal istead of the java object.
        # TODO: Test for more emum types (works on cell importances)
        EAttribute = gateway.jvm.org.eclipse.emf.ecore.EAttribute
        if is_instance_of(feature, EAttribute):
            EEnum = gateway.jvm.org.eclipse.emf.ecore.EEnum
            data_type = feature.getEAttributeType()
            if isinstance(value, JavaList):
                if is_instance_of(data_type, EEnum):
                    e_list = []
                    for v in value:
                        val_str = v.toString()
                        if val_str == '¥×¥':
                            val_str = None
                        e_list.append(val_str)
                    return e_list
            if is_instance_of(data_type, EEnum):
                val_str = value.toString()
                # Enums cannot have nothing for their literal which makes the 
                # grammar technically incorrect in certain cases. E.g. on MCNP 
                # surfaces, the BC enum needs an option for vacuum even though
                # the syntax for this option is simply not the other options.
                # To avoid false validation of the literal, we set it to 
                # characters that would be very abnormal for the user to type.
                # Thus any literal of yen-sign, multiplication-sign, yen-sign
                # should be trated as None.
                if val_str == '¥×¥':
                    return None
                return val_str

        return value

def value_converter(setter, feature, value, numeric_ids):
    """Provides type conversions when using setters."""
    try:
        if numeric_ids is True:
            # Because somehow the API allows any string as an ID... 
            # Now ID/name must be numeric.
            if isinstance(value, str) and feature.getName() == 'name':
                try:
                    int(value)
                except ValueError:
                    raise Exception('"' + value + '" is an invalid ID number')
            elif isinstance(value, str) and feature.getName() == 'comment':
                if value[0] != '$':
                    value = '$ ' + value
        setter.eSet(feature, value)
    except (ValueError, Py4JJavaError, AttributeError):
        if isinstance(value, Enum):
            value_enum = is_enum(value.value, feature)
            setter.eSet(feature, value_enum)
        elif isinstance(value, int):
            try:
                setter.eSet(feature, float(value))
            except (ValueError, Py4JJavaError):
                setter.eSet(feature, str(value))
        # IDs/names are always INTs
        elif isinstance(value, float) and feature.getName() == 'name':
            # Only for round numbers.
            if value%1 == 0:
                try:
                    setter.eSet(feature, int(value))
                except (ValueError, Py4JJavaError):
                    setter.eSet(feature, str(value))
            else:
                raise Exception('"' + str(value) + '" of type '
            + str(type(value)) + ' is invalid for feature "'
            + str(feature.getName()) + '"')
        # For other cases where numbers are stored as strings.
        elif isinstance(value, float):
            try:
                setter.eSet(feature, int(value))
            except (ValueError, Py4JJavaError):
                setter.eSet(feature, str(value))
        elif isinstance(value, str):
            try:
                setter.eSet(feature, float(value))
            except (ValueError, Py4JJavaError):
                setter.eSet(feature, int(value))
        else:
                raise Exception('"' + str(value) + '" of type '
            + str(type(value)) + ' is invalid for feature "'
            + str(feature.getName()) + '"')

def set_wrapped_reference(feature, EObject):
    """Set references to Python wrappers of EObjects."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            returned = setter(self, value)  # this should be None anyways
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if (is_instance_of(feature, EReference) and 
                    isinstance(value, EObject)):
                setattr(self, '_'+camel_to_snake_case(feature.getName()), value)
                if feature.isContainment():
                    value._eContainer = self  # needed in replace_if_contained
            return returned
        return setter_decorated
    return decorator

# Getter decorator applied to all properties
def get_wrapped_reference(feature):
    """Get references to Python wrappers of EObjects."""
    def decorator(getter, feature=feature):
        def getter_decorated(self):
            got = getter(self)
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if is_instance_of(feature, EReference) and got is not None:
                wrapped_reference = getattr(
                    self, '_'+camel_to_snake_case(feature.getName()), None)
                if (wrapped_reference is not None and
                        got.equals(wrapped_reference._e_object)):
                    return wrapped_reference
            return got
        return getter_decorated
    return decorator
            
def javadoc_to_docstring(e_class):
    """Reformats JavaDoc into NumPy docstring.
    """
    javadoc = get_documentation(e_class)
    if javadoc is not None:
        lines = javadoc.splitlines()
        docstring = ''

        for line in lines:
            find_name2 = search(_DOC_PATTERNS[1], line)
            find_name3 = search(_DOC_PATTERNS[2], line)
            if find_name2 is not None:
                new_name = camel_to_snake_case(line[find_name2.start()+4:find_name2.end()-5])
                line = sub(_DOC_PATTERNS[0], new_name, line)
            elif find_name3 is not None:
                new_name = camel_to_snake_case(line[find_name3.start()+3:find_name3.end()-5])
                line = sub(_DOC_PATTERNS[0], new_name, line)
            for pattern in _DOC_PATTERNS[3:]:
                line = sub(pattern[0], pattern[1], line)
            line = line.replace('String', 'str').replace('double', 'float').replace('Integer', 'int').replace('Double', 'float').replace('name : str', 'name : int').replace('EObject', 'Object')

            docstring += line + '\n'
        
        return docstring
    else:
        return 'Python class for ' + e_class.toString()


def set_e_list(setter, feature, values, overrides):
    e_list = setter.eGet(feature, True)
    for value in values:
        # Objects with 'name' have IDs and can be referenced.
        # We want to reference the original object, don't copy!
        if hasattr(value, 'name') and hasattr(value, '_e_object'):
            e_list.addUnique(value._e_object)
        elif type(value).__qualname__ in overrides:
            value_copy = gateway.copier.copy(value._e_object)
            gateway.copier.copyReferences()
            e_list.addUnique(value_copy._e_object)
        else:
            if isinstance(value, Enum):
                value = value.value
            value = is_enum(value, feature)
            try:
                e_list.addUnique(value)
            except:
                if isinstance(value, int):
                    e_list.addUnique(float(value))
                elif isinstance(value, float):
                    e_list.addUnique(int(value))
                else:
                    raise Exception('"' + str(value) + '" of type '
                + str(type(value)) + ' is invalid for feature "'
                + str(feature.getName()) + '"')

def e_class_body(e_class, e_factory, overrides, numeric_ids=False, package=None):
    """Return a Python class body which implements an EClass."""
    def __init__(self, *args, **kwargs):
        #This might be a little sketchy, but the output converter for 
        #automatic-wrapping is turned off and on. EObjects need to be 
        #unwrapped for self._e_object = e_factory.create(e_class). Otherwise,
        #we create an infinite loop of wrappers. In this case, we actually 
        #want the unwrapped EObject. After this, we can turn the auto-wrapping
        #back on. Not sure if there's a more elegant way to handle this.
        register_output_converter(REFERENCE_TYPE, 
                (lambda target_id, 
                gateway_client: JavaObject(target_id, gateway_client)))
        self._e_object = e_factory.create(e_class)
        #add_adapter(self)
        #print(self._e_object)
        register_output_converter(REFERENCE_TYPE, 
            (lambda target_id, 
            gateway_client: wrap_e_object(target_id, gateway_client, overrides, package)))
        if args or kwargs:
            self._init(*args, **kwargs)
    def _init(self):
        raise NotImplementedError  # this should be unreachable
    def __str__(self):
        return self.toString()
    def __hash__(self):
        return self.hashCode()
    def __eq__(self, other):
        # Tests structural equality, not identity
        equals = gateway.equalityHelper.equals
        if isinstance(other, EObject):
            return equals(self._e_object, other._e_object)
        try:
            return equals(self._e_object, other)
        except Py4JError:
            return False
    def __copy__(self):
        copy = gateway.copier.copy(self._e_object)
        gateway.copier.copyReferences()
        return copy
    #class Java:
    #    implements = ['gov.lanl.mcnp.mcnp.'+e_class.getName(),
    #                  'org.eclipse.emf.ecore.InternalEObject']
    body = {attr.__name__: attr for attr in 
            (__init__, _init, __str__, __hash__, __eq__, __copy__)}
    # Convert javadoc metamodel annotations to docstrings.
    body['__doc__'] = javadoc_to_docstring(e_class)

    e_classes = [e_class]
    for e_cls in e_classes:
        for e_super_class in e_cls.getESuperTypes():
            e_classes.append(e_super_class)
        for feature in e_cls.getEStructuralFeatures():
            def make_property(feature=feature):
                #@get_wrapped_reference(feature)
                def getter(self):
                    #print('GETTER RETURN TYPE:', self._e_object.eGet(feature, True))
                    return return_value_converter(feature, self._e_object.eGet(feature, True))
                @replace_if_contained(feature)
                #@set_wrapped_reference(feature)
                @string_or_int_to_enum(feature)
                def setter(self, value):
                    if type(value).__qualname__ in overrides:
                        EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
                        if is_instance_of(feature, EReference):
                            # This makes intersections with 3+ nodes work.
                            # TODO: make sure this is a real fix.
                            try:
                                self.eSet(feature, value._e_object)
                            except:
                                set_e_list(self, feature, value, overrides)
                        else:
                            value_copy = gateway.copier.copy(value._e_object)
                            gateway.copier.copyReferences()
                            self.eSet(feature, value_copy._e_object)
                    elif isinstance(value, tuple) or isinstance(value, list):
                        set_e_list(self, feature, value, overrides)
                    else:
                        value_converter(self, feature, value, numeric_ids)
                            
                return property(getter, setter)
            snake_name = camel_to_snake_case(feature.getName())
            body[snake_name] = make_property(feature)
            cap_name = feature.getName().capitalize()
            body['get'+cap_name] = body[snake_name].fget
            body['set'+cap_name] = body[snake_name].fset

    return body

def wrap_e_package(e_package, overrides, package, wrap_e_class):
    """Wrap every EClass contained in an EPackage."""
    wrappers = {}
    e_factory = e_package.getEFactoryInstance()
    for classifier in e_package.getEClassifiers():
        EClass = gateway.jvm.org.eclipse.emf.ecore.EClass
        if not is_instance_of(classifier, EClass):
            continue
        wrappers[classifier.getName()] = wrap_e_class(classifier, e_factory, InternalEObject, overrides, package)
    return wrappers

def wrap_e_factory(e_factory):
    pass  # TODO

# Apply overrides to nested subclasses.
# Can provide a custom naming prefix and classes to ignore.
def _subclass_overrides(klass, prefix=None, ignore=[], package_name='', overrides={}):
    for method in klass.__dict__.values():
        if str(method).startswith('<class') and method not in ignore:
            for cls in method.__bases__:
                # Only the basic wrappers start with package_name+'.wrap'.
                if package_name + '.wrap' in str(cls):
                    overrides[cls.__name__] = method
                    if prefix is None:
                        base_name = cls.__name__ + 'Base'
                    else:
                        base_name = prefix + cls.__name__ + 'Base'
                    break
            globals().update({base_name: method})
            # For multiple levels of nesting.
            _subclass_overrides(method, prefix, ignore, package_name, overrides)