from typing import List, Tuple

import json
import re
from collections import Counter

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

def count_emojis(file_path: str) -> Counter:
    """Contar la cantidad de emojis por tweet.

    Args:
        file_path (str): Ubicación del archivo con los tweets

    Returns:
        Counter: Contador de emojis
    """
    emojis_cnt = Counter()
    emojis_pattern = extract_emojis_pattern()
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)    
            emojis = emojis_pattern.findall(tweet.get('content'))
            for em in emojis:
                emojis_cnt.update(em.strip().rstrip('\uFE0F'))
    return emojis_cnt

def top_emojis(emojis: Counter) -> List[Tuple[str, int]]:
    """Obtener los 10 emojis más populares. 

    Args:
        emojis (Counter): Contador de emojis

    Returns:
        List[Tuple[str, int]]: Lista de los 10 emojis mas usados con sus conteos
    """
    return emojis.most_common(10)
    
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """Calcular los emojis más populares

    Args:
        file_path (str): Ubicación del archivo con tweets

    Returns:
        List[Tuple[str, int]]: Lista de los 10 emojis más usados y sus respectivos conteos.
    """
    emojis = count_emojis(file_path)
    
    top = top_emojis(emojis)
    
    return top

if __name__ == '__main__':
    print(q2_time('./data/farmers-protest-tweets-2021-2-4.json'))