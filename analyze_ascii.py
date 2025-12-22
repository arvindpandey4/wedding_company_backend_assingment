import requests
from collections import Counter

try:
    url = 'https://69465581ed253f51719dd78e.mockapi.io/get-students/students_data'
    response = requests.get(url)
    data = response.json()

    diffs = []
    details = []

    for s in data:
        n = s.get('name', '')
        c = s.get('country', '')
        
        if n and c:
            # Case sensitive analysis as per user code
            first_char = n[0]
            last_char = c[-1]
            diff = abs(ord(first_char) - ord(last_char))
            diffs.append(diff)
            # details.append(f"{n} ({first_char}/{ord(first_char)}) - {c} ({last_char}/{ord(last_char)}) = {diff}")

    most_common = Counter(diffs).most_common(5)
    print(f"Top 5 most common differences: {most_common}")
    
    min_diff = min(diffs) if diffs else 0
    print(f"Minimum difference found: {min_diff}")

except Exception as e:
    print(f"Error: {e}")
