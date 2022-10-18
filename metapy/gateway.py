import py4j.java_gateway
from py4j.java_gateway import JavaGateway
gateway = JavaGateway(auto_field=True, auto_convert=True, eager_load=True)

def ePackage(package):
    if package.lower() == 'mcnpy':
        return gateway.ePackageMcnp
    elif package.lower() == 'serpy':
        return gateway.ePackageSerpent
    else:
        raise Exception('UNSUPPORTED PACKAGE ERROR! for code "' + package + '"')

def is_instance_of(java_object, java_class, gateway=gateway):
    return py4j.java_gateway.is_instance_of(gateway, java_object, java_class)

def copy(object):
    return gateway.copier.copy(object._e_object)

def get_documentation(e_class):
    """Retrieve metamodel annotations."""
    return gateway.getDocs(e_class)

def print_deck(deck):
    if str(type(deck)) == "<class 'mcnpy._deck.Deck'>":
        return gateway.printDeckMcnp(deck)
    elif str(type(deck)) == "<class 'serpy.deck.Deck'>":
        return gateway.printDeckSerpent(deck)
    else:
        raise Exception('SERIALIZATION ERROR! for deck of type: ' + str(type(deck)))

def load_file(filename):
    try:
        return gateway.loadFileMcnp(filename)
    except:
        try:
            return gateway.loadFileSerpent(filename)
        except:
            raise Exception('PARSING ERROR! for file: ' + filename)

def deck_resource(deck):
    if str(type(deck)) == "<class 'mcnpy._deck.Deck'>":
        return gateway.deckResourceMcnp(deck.__copy__(), 'deck.serpent')
    elif str(type(deck)) == "<class 'serpy.deck.Deck'>":
        return gateway.deckResourceSerpent(deck.__copy__(), 'deck.serpent')
    else:
        raise Exception('DECK RESOURCE ERROR! for deck of type: ' + str(type(deck)))