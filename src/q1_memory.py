from typing import List, Tuple, Dict

import json
from collections import defaultdict
from datetime import datetime
import heapq

from memory_profiler import profile

# @profile(precision=4)
def group_by_date(file_path: str) -> Dict[str, Dict[str, int]]:
    """Revisar todos los tweets para agruparlos por fecha

    Args:
        file_path (str): Ubicacion del archivo con los tweets

    Returns:
        Dict[str, Dict[str, int]]: Tweets por Usuario por Fecha
    """
    #dates = {}
    user_by_date = {}
    
    with open(file_path, 'r') as file:
        # Revisar cada fila de tweets (un total de m)
        for line in file:
            date = datetime.fromisoformat(json.loads(line)['date']).date().strftime('%Y%m%d')
            # Conteo de tweets por usuario para fecha
            username = json.loads(line).get('user').get('username')
            if user_by_date.get(date, {}).get(username):
                user_by_date[date][username] += 1
            else:
                if user_by_date.get(date):
                    user_by_date[date][username] = 1
                else:
                    user_by_date[date] = {username: 1}
                    
            del date
            del username
                    
    return user_by_date

# @profile(precision=4)
def popular_dates(dates: Dict[str, int]) -> List[str]:
    """Calcular las 10 fechas con mas tweet

    Args:
        dates (Dict[str, int]): Cantidad de tweets por usuario por fecha

    Returns:
        List[str]: Top 10 fechas de mayor a menor
    """
    # Hay que sumar la cantidad de tweeets totales entre todos los uusarios de una fecha
    return [date for date, _ in heapq.nlargest(10, dates.items(), key=lambda x: sum(x[1].values()))]
 
# @profile(precision=4)
def popular_users(user_by_date: Dict[str, int], min_heap: List[Tuple[str, int]]) -> List[str]:
    """Calculate the most popular user for each of the top 10 dates.

    Args:
        user_by_date (Dict[str, int]): Amount of tweets by user by date
        min_heap (List[Tuple[str, int]]): Min-Heap tree with the top 10 dates 

    Returns:
        List[str]: List of most popular contributor by date
    """
    return [max(user_by_date[date].items(), key=lambda x: x[1])[0] for date in min_heap]            

# @profile(precision=4)
def q1_memory(file_path: str) -> List[Tuple[str, int]]:
    """Find the 10 dates with the most tweets and the user with the most tweets for each of those dates, all while optimizing memory usage.

    Args:
        file_path (str): file with the list of tweets

    Returns:
        List[Tuple[str, int]]: Top 10 most popular dates with its most popular user
    """
    # agrupar por fecha
    dates_by_user = group_by_date(file_path)
    
    # Calcular el min-heap
    min_heap = popular_dates(dates_by_user)
    
    users = popular_users(dates_by_user, min_heap)
    
    result = [(date, user) for date, user in zip(min_heap, users)] 
    
    # Delete from memory
    del dates_by_user
    del min_heap
    del users
    
    return result


if __name__ == '__main__':
    print(q1_memory('./data/farmers-protest-tweets-2021-2-4.json'))