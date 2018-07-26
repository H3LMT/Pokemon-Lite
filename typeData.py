#functions to parse through types and return in an integer format or vice-versa

def typeToIndex(type):
    types = ['X', 'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying',
             'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    if(type in types):
        return types.index(type)-1
    else: return None

def indexToType(index,abbreviated = False):
    if(abbreviated==False):
        types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying',
                 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
        return types[index]
    else:
        types = ['NOR', 'FIR', 'WAT', 'ELE', 'GRA', 'ICE', 'FIG', 'POI', 'GRO', 'FLY',
                 'PSY', 'BUG', 'ROC', 'GHO', 'DRA', 'DAR', 'STE', 'FAI']
        return types[index]

