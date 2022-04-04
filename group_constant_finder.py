import math


#returns 5 group_constant that is highly likely to have the highest compressability as a list
#lowest_range: lowest group_constant you want to check
#highest_range: highest group_constant you want to check
def group_constant_finder(bn_str : str, lowest_range : int, highest_range: int)->list:
    #key:group_constant
    #value:compressability
    compressability=dict()
    for group_constant in range(lowest_range,highest_range):
        #probability of num of keys
        key_prob=dict()
        #number of groups, including leftover
        group_num=int(len(bn_str)/group_constant)+1
        #python can't handle large number division, and since all cases have same total cases, 
        #probability will be substituted with number of cases for specific key_variety
        for key_variety in range(1,2**group_constant):
            key_prob[key_variety]=(math.comb(2**group_constant,key_variety))*(key_variety**group_num-(key_variety-1)**group_num)
        key_prob=dict(sorted(key_prob.items(), key=lambda group: group[1], reverse=True))
        highest_probability_key=list(key_prob.keys())[0]
        compressability[group_constant]=math.log2(highest_probability_key)*group_num
    compressability=dict(sorted(compressability.items(), key=lambda group: group[1], reverse=False))
    if(highest_range-lowest_range+1)<5:
        return list(compressability.keys())[:highest_range-lowest_range+1]
    return list(compressability.keys())[:5]




