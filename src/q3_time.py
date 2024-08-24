from typing import List, Tuple

import orjson as json
from collections import Counter


def user_mentions(file_path: str) -> Counter:
    """Contar la cantidad de menciones que tiene cada usuario

    Args:
        file_path (str): ubicación del archivo con los tweets

    Returns:
        defaultdict[str, int]: Contador de número de menciones por usuario
    """
    users = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            mentions = tweet.get('mentionedUsers')
            if mentions:
                users.update(t['username'] for t in mentions)
    return users

def top_users(users: Counter) -> List[Tuple[str, int]]:
    """Obtener los 10 usuarios más populares, es decir, los que más menciones tienen.

    Args:
        users (Counter): Contador de todos los usuarios con sus respectivas cantidades de menciones para

    Returns:
        List[Tuple[str, int]]: Top 10 de usuarios mencionados
    """
    return users.most_common(10)

        
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """Dado un archivo de tweets, obtener los 10 usuarios con más menciones entre todos los tweets 

    Args:
        file_path (str): Ubicación del archivo de tweets

    Returns:
        List[Tuple[str, int]]: Top 10 de usuarios con más menciones.
    """
    mentions = user_mentions(file_path)
    
    top = top_users(mentions)
    
    return top


if __name__ == '__main__':
    print(q3_time('./data/farmers-protest-tweets-2021-2-4.json'))