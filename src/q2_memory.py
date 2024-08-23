from typing import List, Tuple, Dict

import re
import json
import heapq

# from memory_profiler import profile

# @profile(precision=4)
def extract_emojis_pattern():
    # Regular expression pattern for emojis
    return re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE
    )

# @profile(precision=4)
def count_emojis(file_path: str) -> Dict[str, int]:
    emojis_cnt = {}
    emojis_pattern = extract_emojis_pattern()
    with open(file_path, 'r') as file:
        for line in file:  
            for em in emojis_pattern.findall(json.loads(line).get('content')):
                for e in em.strip().rstrip('\uFE0F'):
                    if emojis_cnt.get(e):
                        emojis_cnt[e] += 1
                    else:
                        emojis_cnt[e] = 1
    del emojis_pattern
    return emojis_cnt

# @profile(precision=4)
def top_emojis(emojis: Dict[str, int]) -> List[Tuple[str, int]]:
    return heapq.nlargest(10, emojis.items(), key=lambda x: x[1])

# @profile(precision=4)
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emojis = count_emojis(file_path)
    
    top = top_emojis(emojis)
    
    return top


if __name__ == '__main__':
    print(q2_memory('./data/farmers-protest-tweets-2021-2-4.json'))