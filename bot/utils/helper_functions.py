def try_get_value(_dict, key, default_val):
    return _dict[key] if key in _dict else default_val

def find_closest_user(iterable, name):
    new_list = []

def longest_common_subsequence(name1, name2):
    new_name1 = name1.lower().replace(" ", "")
    new_name2 = name2.lower().replace(" ", "") #lowercase and remove all spaces
    
    return lcs(new_name1, new_name2, len(new_name1), len(new_name2))

def lcs(name1, name2, m, n) -> int:
    if m == 0 or n == 0:
        return 0
    elif name1[m-1] == name2[n-1]:
        return 1 + lcs(name1, name2, m-1, n-1)
    else:
        return max(lcs(name1, name2, m-1, n), lcs(name1, name2, m, n-1))
    
if __name__ == "__main__":
    print(longest_common_subsequence("Curly", "curly"))