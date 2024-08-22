from typing import List, Tuple, Dict
from datetime import datetime

import json
from collections import defaultdict
import heapq

def group_by_date(file_path: str) -> Tuple[defaultdict, Dict[datetime.date, str]]:
    dates = defaultdict(int)
    user_by_date = defaultdict(lambda: defaultdict(int))
    dates_max_usr = {}
    with open(file_path, 'r') as file:
        # Revisar cada fila de tweets (un total de m)
        for line in file:
            tweet = json.loads(line)
            date = datetime.fromisoformat(tweet.get('date')).date()
            # Conteo de tweeets por dia
            dates[date] += 1
            # Llevar el registro de el usuario con mas tweets para cada dia
            user_by_date[date][tweet.get('user').get('username')] += 1
            if dates_max_usr.get(date, (None, 0))[1] < user_by_date[date][tweet.get('user').get('username')]:
                dates_max_usr[date] = (tweet.get('user').get('username'), user_by_date[date][tweet.get('user').get('username')])
    
    return dates, dates_max_usr

def popular_dates(dates: defaultdict) -> List[Tuple[int, datetime.date]]:
    # Crear el min-heap con las fechas más populares
    min_heap = []
    for date, count in dates.items():
        if len(min_heap) < 10:
            heapq.heappush(min_heap, (count, date))
        elif count > min_heap[0][0]:
            heapq.heapreplace(min_heap, (count, date))
    
    return min_heap

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # agrupar por fecha (O(m))
    dates, dates_max_usr = group_by_date(file_path)
    
    # Calcular el min-heam (O(nlog10))
    min_heap = popular_dates(dates)
    
    # Retornar las fechas más populares (O(10))
    return [(date, dates_max_usr[date][0]) for _, date in heapq.nlargest(10, min_heap)] 
                    
    

if __name__ == '__main__':
    print(q1_time('./data/farmers-protest-tweets-2021-2-4.json'))