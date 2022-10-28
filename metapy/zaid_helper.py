import h5py as h5
from inspect import getsourcefile
from os.path import join, dirname

#M_NEUTRON = 1.008664967 #amu

"""Functions for ZAID conversions.
"""
def z_to_elements():
    e = dict()
    e[1] = 'H'
    e[2] = 'He'
    e[3] = 'Li'
    e[4] = 'Be'
    e[5] = 'B'
    e[6] = 'C'
    e[7] = 'N'
    e[8] = 'O'
    e[9] = 'F'
    e[10] = 'Ne'
    e[11] = 'Na'
    e[12] = 'Mg'
    e[13] = 'Al'
    e[14] = 'Si'
    e[15] = 'P'
    e[16] = 'S'
    e[17] = 'Cl'
    e[18] = 'Ar'
    e[19] = 'K'
    e[20] = 'Ca'
    e[21] = 'Sc'
    e[22] = 'Ti'
    e[23] = 'V'
    e[24] = 'Cr'
    e[25] = 'Mn'
    e[26] = 'Fe'
    e[27] = 'Co'
    e[28] = 'Ni'
    e[29] = 'Cu'
    e[30] = 'Zn'
    e[31] = 'Ga'
    e[32] = 'Ge'
    e[33] = 'As'
    e[34] = 'Se'
    e[35] = 'Br'
    e[36] = 'Kr'
    e[37] = 'Rb'
    e[38] = 'Sr'
    e[39] = 'Y'
    e[40] = 'Zr'
    e[41] = 'Nb'
    e[42] = 'Mo'
    e[43] = 'Tc'
    e[44] = 'Ru'
    e[45] = 'Rh'
    e[46] = 'Pd'
    e[47] = 'Ag'
    e[48] = 'Cd'
    e[49] = 'In'
    e[50] = 'Sn'
    e[51] = 'Sb'
    e[52] = 'Te'
    e[53] = 'I'
    e[54] = 'Xe'
    e[55] = 'Cs'
    e[56] = 'Ba'
    e[57] = 'La'
    e[58] = 'Ce'
    e[59] = 'Pr'
    e[60] = 'Nd'
    e[61] = 'Pm'
    e[62] = 'Sm'
    e[63] = 'Eu'
    e[64] = 'Gd'
    e[65] = 'Tb'
    e[66] = 'Dy'
    e[67] = 'Ho'
    e[68] = 'Er'
    e[69] = 'Tm'
    e[70] = 'Yb'
    e[71] = 'Lu'
    e[72] = 'Hf'
    e[73] = 'Ta'
    e[74] = 'W'
    e[75] = 'Re'
    e[76] = 'Os'
    e[77] = 'Ir'
    e[78] = 'Pt'
    e[79] = 'Au'
    e[80] = 'Hg'
    e[81] = 'Tl'
    e[82] = 'Pb'
    e[83] = 'Bi'
    e[84] = 'Po'
    e[85] = 'At'
    e[86] = 'Rn'
    e[87] = 'Fr'
    e[88] = 'Ra'
    e[89] = 'Ac'
    e[90] = 'Th'
    e[91] = 'Pa'
    e[92] = 'U'
    e[93] = 'Np'
    e[94] = 'Pu'
    e[95] = 'Am'
    e[96] = 'Cm'
    e[97] = 'Bk'
    e[98] = 'Cf'
    e[99] = 'Es'
    e[100] = 'Fm'
    e[101] = 'Md'
    e[102] = 'No'
    e[103] = 'Lr'
    e[104] = 'Rf'
    e[105] = 'Db'
    e[106] = 'Sg'
    e[107] = 'Bh'
    e[108] = 'Hs'
    e[109] = 'Mt'
    e[110] = 'Ds'
    e[111] = 'Rg'
    e[112] = 'Cn'
    e[113] = 'Nh'
    e[114] = 'Fl'
    e[115] = 'Mc'
    e[116] = 'Lv'
    e[117] = 'Ts'
    e[118] = 'Og'

    return e

def elements_to_z():
    e = dict()
    e['H'] = 1
    e['HE'] = 2
    e['LI'] = 3
    e['BE'] = 4
    e['B'] = 5
    e['C'] = 6
    e['N'] = 7
    e['O'] = 8
    e['F'] = 9
    e['NE'] = 10
    e['NA'] = 11
    e['MG'] = 12
    e['AL'] = 13
    e['SI'] = 14
    e['P'] = 15
    e['S'] = 16
    e['CL'] = 17
    e['AR'] = 18
    e['K'] = 19
    e['CA'] = 20
    e['SC'] = 21
    e['TI'] = 22
    e['V'] = 23
    e['CR'] = 24
    e['MN'] = 25
    e['FE'] = 26
    e['CO'] = 27
    e['NI'] = 28
    e['CU'] = 29
    e['ZN'] = 30
    e['GA'] = 31
    e['GE'] = 32
    e['AS'] = 33
    e['SE'] = 34
    e['BR'] = 35
    e['KR'] = 36
    e['RB'] = 37
    e['SR'] = 38
    e['Y'] = 39
    e['ZR'] = 40
    e['NB'] = 41
    e['MO'] = 42
    e['TC'] = 43
    e['RU'] = 44
    e['RH'] = 45
    e['PD'] = 46
    e['AG'] = 47
    e['CD'] = 48
    e['IN'] = 49
    e['SN'] = 50
    e['SB'] = 51
    e['TE'] = 52
    e['I'] = 53
    e['XE'] = 54
    e['CS'] = 55
    e['BA'] = 56
    e['LA'] = 57
    e['CE'] = 58
    e['PR'] = 59
    e['ND'] = 60
    e['PM'] = 61
    e['SM'] = 62
    e['EU'] = 63
    e['GD'] = 64
    e['TB'] = 65
    e['DY'] = 66
    e['HO'] = 67
    e['ER'] = 68
    e['TM'] = 69
    e['YB'] = 70
    e['LU'] = 71
    e['HF'] = 72
    e['TA'] = 73
    e['W'] = 74
    e['RE'] = 75
    e['OS'] = 76
    e['IR'] = 77
    e['PT'] = 78
    e['AU'] = 79
    e['HG'] = 80
    e['TL'] = 81
    e['PB'] = 82
    e['BI'] = 83
    e['PO'] = 84
    e['AT'] = 85
    e['RN'] = 86
    e['FR'] = 87
    e['RA'] = 88
    e['AC'] = 89
    e['TH'] = 90
    e['PA'] = 91
    e['U'] = 92
    e['NP'] = 93
    e['PU'] = 94
    e['AM'] = 95
    e['CM'] = 96
    e['BK'] = 97
    e['CF'] = 98
    e['ES'] = 99
    e['FM'] = 100
    e['MD'] = 101
    e['NO'] = 102
    e['LR'] = 103
    e['RF'] = 104
    e['DD'] = 105
    e['SG'] = 106
    e['BH'] = 107
    e['HS'] = 108
    e['MT'] = 109
    e['DS'] = 110
    e['RG'] = 111
    e['CN'] = 112
    e['NH'] = 113
    e['FL'] = 114
    e['MC'] = 115
    e['LV'] = 116
    e['TS'] = 117
    e['OG'] = 118

    return e

def zaid_mass(zaid, meta=None):
    path = dirname(getsourcefile(lambda:0))
    masses = h5.File(join(path, 'masses.h5'), 'r')

    if meta is None:
        return float(masses['ZAID'][str(zaid)][()])
    else:
        zaid -= 300 - 100*meta
        return float(masses['ZAID'][str(zaid)][()])

def zaid_to_element(zaid):
    path = dirname(getsourcefile(lambda:0))
    e = z_to_elements()
    xsdir = h5.File(join(path, 'xslist.h5'), 'r')
    zaids_h5 = xsdir['ZAID']

    zaid_num = str(zaid)
    if zaid_num not in list(zaids_h5.keys()):
        a = int(zaid_num[-3:])
        if a >= 300:
            # Metastable state.
            pass
        else:
            print('\nZAID WARNING! User input: ' + zaid_num 
                  + ' (interpretted as ' + str(zaid) + ') has no MCNP XS!')

    try:
        zaid_num = e[int(zaid_num[:-3])] + str(int(zaid_num[-3:]))
    except:
        print('\nERROR! Element with atomic number ' + zaid_num[:-3] 
              + ' does not exist!')
    
    xsdir.close()
    return zaid_num

def element_to_zaid(zaid):
    """Converts periodic table style element names into MCNP ZAIDs.
    For example, 'U235' will become '92235' in the input deck. Returns a string 
    of the MCNP ZAID.
    """
    path = dirname(getsourcefile(lambda:0))
    e = elements_to_z()
    xsdir = h5.File(join(path, 'xslist.h5'), 'r')
    zaids_h5 = xsdir['ZAID']
    string = str(zaid)
    # Check if numerical ZAID was provided.
    try:
        int(string)
        zaid_num = string
    except:
        string = str(zaid)
        try:
            z = str(e[''.join(c for c in string if c.isalpha()).upper()])
        except:
            print('\nERROR! Element ' + zaid + ' does not exist!')
        a = ''.join(c for c in string if c.isdigit())
        if len(a) == 0:
            a = '000'
        elif len(a) == 1:
            a = '00' + a
        elif len(a) == 2:
            a = '0' + a
        zaid_num = z + a
    # The converted ZAID can now be checked against the available XS.
    if zaid_num not in list(zaids_h5.keys()):
        a = int(zaid_num[-3:])
        if a >= 300:
            # Metastable state.
            pass
        else:
            print('\nZAID WARNING! User input: ' + string + ' (interpretted as '
                   + zaid_num + ')' + 'not found!')
    xsdir.close()
    return zaid_num

#TODO: Add lib checks back in.
def library_check(zaid, library):
    """Checks XS libraries for a ZAID. 
    """
    path = dirname(getsourcefile(lambda:0))
    xsdir = h5.File(join(path, 'xslist.h5'), 'r')
    lib = str(library).lower()
    # Confirms that the ZAID exists.
    try:
        libs_h5 = xsdir['ZAID'][element_to_zaid(zaid)]
    except:
        print('\nZAID WARNING! User input: ' + zaid + ' not found!')
        return library

    # Libs can just have the number and no letter, either format qualifies.
    found = False
    for i in range(len(libs_h5)):
        num = libs_h5[i][:2]
        if bytes(lib, 'utf-8') == num or bytes(lib, 'utf-8') == libs_h5[i]:
            found = True
            break

    if found == False:
        print('\nWARNING! XS file for ' + zaid + '.' + lib + ' not found!')
        print('Please check available XS libraries!')
        return library
    else:
        return library