from collections import Counter

def check_multiple_duplicates(lst: list):
    count = Counter(lst)
    
    for item in count:
        if count[item] > 2:
            return False ## 중복이 있을 떄 False Return
    
    return True ## 중복이 없을 때 True Return