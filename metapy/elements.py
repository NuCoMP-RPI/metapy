from .zaid_helper import elements_to_z, zaid_mass

def _element_factory(name:str):
    class SingletonElement():
        def __new__(self):
            if not hasattr(self, 'instance'):
                self.instance = super(self.__class__, self).__new__(self)
                self.z = elements_to_z()[name.upper()]
                self.mass = 0
                self.name = name
                self.fraction = 1
                self.unit = 'ATOM'
                self.lib = None
                self.meta = None
            return self.instance

        def __getitem__(self, mass, lib=None, meta=None):
            if isinstance(mass, tuple):
                self.mass = mass[0]
                self.lib = None
                self.meta = None
                if len(mass) == 2:
                    self.lib = mass[1]
                elif len(mass) == 3:
                    self.lib = mass[1]
                    self.meta = mass[2]
            else:
                self.mass = mass
            return self

        # By weight percent.
        def __mod__(self, other):
            #nuclide = Nuclide(self.zaid(), other, 'WEIGHT', self.lib)
            self.fraction = float(other)
            self.unit = 'WEIGHT%'
            return _Element(self) #nuclide

        # By atomic fraction.
        def __matmul__(self, other):
            #nuclide = Nuclide(self.zaid(), other, 'ATOM', self.lib)
            self.fraction = float(other)
            self.unit = 'ATOM'
            return _Element(self) #nuclide

        # By weight fraction.
        def __mul__(self, other):
            #nuclide = Nuclide(self.zaid(), other, 'ATOM', self.lib)
            self.fraction = float(other)
            self.unit = 'WEIGHT'
            return _Element(self) #nuclide

        def as_nuclide(self, nuclide_cls):
            return nuclide_cls(self.zaid(), self.fraction, self.unit, self.lib)

        def __add__(self, other):
            """"""
            """if isinstance(other, Element):
                return Mixture([self.as_nuclide(), other.as_nuclide()])"""
            """if isinstance(other, _Mixture):
                other.elements = [_Element(self)] + other.elements
                return other
            else:"""
            return correct_units(_Element(self), other)
                #return _Mixture([_Element(self), _Element(other)])

        def zaid(self):
            if self.meta is None:
                a = str(self.mass)
                if self.mass == 0:
                    return self.z*1000
                elif len(a) == 2:
                    a = '0' + a
                elif len(a) == 1:
                    a = '00' + a
                return int(str(self.z) + a)
            else:
                return int(str(self.z) + str(self.mass + 300 + 100*self.meta))

    return SingletonElement()

def correct_units(left, right):
        """When adding 2 _Elements, apply units from right side of operand."""
        try:
            right = _Element(right)
            if isinstance(left, _Mixture):
                if right.unit == 'WEIGHT%':
                        right.unit = 'WEIGHT'
                        right.fraction /= 100.0
                if left.unit == right.unit:
                    # same units
                    pass
                elif right.unit == 'ATOM':
                    left.weight_to_atom(left.fraction)
                else:
                    left.atom_to_weight(left.fraction)
                #left.elements.append(right)

                return _Mixture(list(left.elements.values()) + [right])
            else:
                left = _Element(left)
                # Weights as fractions.
                if left.unit == 'WEIGHT%':
                        left.unit = 'WEIGHT'
                        left.fraction /= 100.0
                if right.unit == 'WEIGHT%':
                        right.unit = 'WEIGHT'
                        right.fraction /= 100.0
                
                if left.unit == right.unit:
                    # same units.
                    pass
                elif right.unit == 'ATOM':
                    left.fraction = ((left.fraction * zaid_mass(right.fraction, 
                                                                right.meta) 
                                                                * right.fraction) 
                                    / ((1 - left.fraction) 
                                    * zaid_mass(left.fraction, left.meta)))
                    left.unit = 'ATOM'
                else:
                    left.fraction = 1 - right.fraction
                    left.unit = 'WEIGHT'
                
                return _Mixture([left, right])

        except:
            if isinstance(left, _Mixture) is False:
                left = _Element(left)
                if left.unit == 'WEIGHT%':
                        left.unit = 'WEIGHT'
                        left.fraction /= 100.0
                if left.unit == right.unit:
                    # same units
                    pass
                elif right.unit == 'ATOM':
                    left.fraction = ((left.fraction * zaid_mass(right.fraction, 
                                                                right.meta) 
                                                                * right.fraction) 
                                    / ((1 - left.fraction) 
                                    * zaid_mass(left.fraction, left.meta)))
                    left.unit = 'ATOM'
                else:
                    left.fraction = 1 - right.fraction
                    left.unit = 'WEIGHT'

                return _Mixture([left] + list(right.elements.values()))
            else:
                if left.fraction != 1.0:
                    left.apply_fraction()
                if right.fraction != 1.0:
                    right.apply_fraction()
                if left.unit == right.unit:
                    pass
                elif right.unit == 'ATOM':
                    left.weight_to_atom(left.fraction)
                else:
                    left.atom_to_weight(left.fraction)
                return _Mixture(list(left.elements.values()) 
                                + list(right.elements.values()))
        
class _Element():
    def __init__(self, element):
        """
        """
        if isinstance(element, _Element):
            self.zaid = element.zaid
        else:
            self.zaid = element.zaid()
        self.name = element.name
        self.z = element.z
        self.mass = element.mass
        self.meta = element.meta
        if element.unit == 'WEIGHT%':
            self.fraction = element.fraction / 100.0
            self.unit = 'WEIGHT'
        else:
            self.fraction = element.fraction
            self.unit = element.unit
        self.lib = element.lib

        # Need to reset the singleton after use.
        if isinstance(element, _Element) is False:
            element.mass = 0
            element.fraction = 1
            element.unit = 'ATOM'
            element.lib = None
            element.meta = None

    def __add__(self, other):
        return correct_units(self, other)

    def __str__(self):
        string = str(self.name) + '[' + str(self.mass)
        if self.lib is not None:
            string += ', ' + str(self.lib)
        string += ']'
        if self.unit == 'ATOM':
            string += '@'
        elif self.unit == 'WEIGHT':
            string += '*'
        else:
            string += '%'
        string += str(self.fraction)
        return string

    def __repr__(self) -> str:
        return str(self)

    def nuclides(self, nuclide_cls):
        _nuclides = []
        _nuclides.append(self.as_nuclide(nuclide_cls))
        return _nuclides

    def as_nuclide(self, nuclide_cls):
            return nuclide_cls(self.zaid, self.fraction, self.unit, self.lib)

#TODO: Add check for adding same element to mixture.
class _Mixture():
    """Contains a list of Elements."""
    def __init__(self, elements=[]):
        _elements = dict()
        for el in elements:
            if el.zaid in _elements:
                _elements[el.zaid].fraction += el.fraction
            else:
                _elements[el.zaid] = el
        self.elements = _elements
        self.fraction = 1.0
        self.unit = list(self.elements.values())[0].unit
        #self.mass = 0
        """for el in self.elements:
            if self.unit == 'ATOM':
                self.mass += zaid_mass(el.zaid, el.meta) * el.fraction
            else:
                self.mass += el.fraction / zaid_mass(el.zaid, el.meta)
            if self.unit == 'WEIGHT%':
                self.mass /= 100.0"""

    """@property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        _elements = dict()
        for el in elements:
            if el.zaid in self._elements:
                _elements[el.zaid].fraction += el.fraction
            else:
                _elements[el.zaid] = el
        self._elements = _elements"""


    # By weight percent.
    def __mod__(self, other):
        #nuclide = Nuclide(self.zaid(), other, 'WEIGHT', self.lib)
        self.fraction = float(other)
        if list(self.elements.values())[0].unit == 'ATOM':
            self.atom_to_weight(self.fraction, 'WEIGHT%')
        else:
            self.unit = 'WEIGHT%'
        return self

    # By atomic fraction.
    def __matmul__(self, other):
        self.fraction = float(other)
        if list(self.elements.values())[0].unit != 'ATOM':
            self.weight_to_atom(self.fraction)
        else:
            self.unit = 'ATOM'
        return self

    # By weight fraction.
    def __mul__(self, other):
        self.fraction = float(other)
        if list(self.elements.values())[0].unit == 'ATOM':
            self.atom_to_weight(self.fraction)
        else:
            self.unit = 'WEIGHT'
        return self

    def weight_to_atom(self, mult=1.0):
        #mass = 0
        norm = 0
        for el in self.elements.values():
            el.fraction = el.fraction / zaid_mass(el.zaid, el.meta)
            norm += el.fraction
            """if norm == 1:
                norm = el.fraction
            elif el.fraction < norm:
                norm = el.fraction"""
            el.unit = 'ATOM'
        self.unit = 'ATOM'
        for el in self.elements.values():
            el.fraction = el.fraction * mult / norm
        self.fraction = 1.0
        #self.mass = mass

    def atom_to_weight(self, mult=1.0, unit='WEIGHT'):
        mass = 0
        #norm = 1
        for el in self.elements.values():
            mass += (el.fraction * zaid_mass(el.zaid, el.meta))
            """if norm == 1:
                norm = el.fraction
            elif el.fraction < norm:
                norm = el.fraction"""
        #mass /= norm
        self.unit = unit
        for el in self.elements.values():
            el.fraction = mult * (el.fraction * zaid_mass(el.zaid, el.meta)) / mass
            if unit == 'WEIGHT%':
                el.fraction *= 100.0
            el.unit = unit
        self.fraction = 1.0
        #self.mass = mass * mult

    def apply_fraction(self):
        if self.unit == 'WEIGHT%':
            self.fraction /= 100.0
        for el in self.elements.values():
            el.fraction *= self.fraction
        self.fraction = 1.0
        #if self.unit != 'ATOM':
            #self.mass *= self.fraction


    def __add__(self, other):
        return correct_units(self, other)
        """if isinstance(other, _Mixture):
            other.elements = self.elements + other.elements
            return other
        else:
            self.elements.append(_Element(other))
            return self"""
    
    def nuclides(self, nuclide_cls):
        _nuclides = []
        for el in self.elements.values():
            _nuclides.append(el.as_nuclide(nuclide_cls))
        return _nuclides

H = _element_factory('H')
HE = _element_factory('HE')
LI = _element_factory('LI')
BE = _element_factory('BE')
B = _element_factory('B')
C = _element_factory('C')
N = _element_factory('N')
O = _element_factory('O')
F = _element_factory('F')
NE = _element_factory('NE')
NA = _element_factory('NA')
MG = _element_factory('MG')
AL = _element_factory('AL')
SI = _element_factory('SI')
P = _element_factory('P')
S = _element_factory('S')
CL = _element_factory('CL')
AR = _element_factory('AR')
K = _element_factory('K')
CA = _element_factory('CA')
SC = _element_factory('SC')
TI = _element_factory('TI')
V = _element_factory('V')
CR = _element_factory('CR')
MN = _element_factory('MN')
FE = _element_factory('FE')
CO = _element_factory('CO')
NI = _element_factory('NI')
CU = _element_factory('CU')
ZN = _element_factory('ZN')
GA = _element_factory('GA')
GE = _element_factory('GE')
AS = _element_factory('AS')
SE = _element_factory('SE')
BR = _element_factory('BR')
KR = _element_factory('KR')
RB = _element_factory('RB')
SR = _element_factory('SR')
Y = _element_factory('Y')
ZR = _element_factory('ZR')
NB = _element_factory('NB')
MO = _element_factory('MO')
TC = _element_factory('TC')
RU = _element_factory('RU')
RH = _element_factory('RH')
PD = _element_factory('PD')
AG = _element_factory('AG')
CD = _element_factory('CD')
IN = _element_factory('IN')
SN = _element_factory('SN')
SB = _element_factory('SB')
TE = _element_factory('TE')
I = _element_factory('I')
XE = _element_factory('XE')
CS = _element_factory('CS')
BA = _element_factory('BA')
LA = _element_factory('LA')
CE = _element_factory('CE')
PR = _element_factory('PR')
ND = _element_factory('ND')
PM = _element_factory('PM')
SM = _element_factory('SM')
EU = _element_factory('EU')
GD = _element_factory('GD')
TB = _element_factory('TB')
DY = _element_factory('DY')
HO = _element_factory('HO')
ER = _element_factory('ER')
TM = _element_factory('TM')
YB = _element_factory('YB')
LU = _element_factory('LU')
HF = _element_factory('HF')
TA = _element_factory('TA')
W = _element_factory('W')
RE = _element_factory('RE')
OS = _element_factory('OS')
IR = _element_factory('IR')
PT = _element_factory('PT')
AU = _element_factory('AU')
HG = _element_factory('HG')
TL = _element_factory('TL')
PB = _element_factory('PB')
BI = _element_factory('BI')
PO = _element_factory('PO')
AT = _element_factory('AT')
RN = _element_factory('RN')
FR = _element_factory('FR')
RA = _element_factory('RA')
AC = _element_factory('AC')
TH = _element_factory('TH')
PA = _element_factory('PA')
U = _element_factory('U')
NP = _element_factory('NP')
PU = _element_factory('PU')
AM = _element_factory('AM')
CM = _element_factory('CM')
BK = _element_factory('BK')
CF = _element_factory('CF')
ES = _element_factory('ES')
FM = _element_factory('FM')
MD = _element_factory('MD')
NO = _element_factory('NO')
LR = _element_factory('LR')
RF = _element_factory('RF')
DD = _element_factory('DD')
SG = _element_factory('SG')
BH = _element_factory('BH')
HS = _element_factory('HS')
MT = _element_factory('MT')
DS = _element_factory('DS')
RG = _element_factory('RG')
CN = _element_factory('CN')
NH = _element_factory('NH')
FL = _element_factory('FL')
MC = _element_factory('MC')
LV = _element_factory('LV')
TS = _element_factory('TS')
OG = _element_factory('OG')
