from typing import List, Tuple, Dict

import json
import heapq

# from memory_profiler import profile


# @profile(precision=10)
def user_mentions(file_path: str) -> Dict[str, int]:
    """Contar la cantidad de menciones que tiene cada usuario

    Args:
        file_path (str): ubicación del archivo con los tweets

    Returns:
        Dict[str, int]: Contador de número de menciones por usuario
    """
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            for username in [mention['username'] for mention in (json.loads(line).get('mentionedUsers') or [])]:
                if users.get(username):
                    users[username] += 1
                else:
                    users[username] = 1
    return users

# @profile(precision=10)
def top_users(users: Dict[str, int]) -> List[Tuple[str, int]]:
    """Obtener los 10 usuarios más populares, es decir, los que más menciones tienen.

    Args:
        users (Dict[str, int]): Contador de todos los usuarios con sus respectivas cantidades de menciones para

    Returns:
        List[Tuple[str, int]]: Top 10 de usuarios mencionados
    """
    min_heap = []
    for user, count in users.items():
        if len(min_heap) < 10:
            heapq.heappush(min_heap, (count, user))
        else:
            heapq.heappushpop(min_heap, (count, user))
    return [(user, count) for count, user in heapq.nlargest(10, min_heap)]

# @profile(precision=10)
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """Dado un archivo de tweets, obtener los 10 usuarios con más menciones entre todos los tweets 

    Args:
        file_path (str): Ubicación del archivo de tweets

    Returns:
        List[Tuple[str, int]]: Top 10 de usuarios con más menciones.
    """
    mentions = user_mentions(file_path)
    
    top = top_users(mentions)
    
    del mentions
    return top


if __name__ == '__main__':
    print(q3_memory('./data/farmers-protest-tweets-2021-2-4.json'))