from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import os
def exec():
  cur_dir = os.getcwd()
  destination_path = os.path.join(cur_dir,'backend', 'Config', 'CTransformersModelList.json')
  html = urlopen("https://huggingface.co/TheBloke/PuddleJumper-13B-GGML")
  soup = BeautifulSoup(html, "lxml")

  target_div = soup.find("div", {"class": "max-w-full overflow-auto"})
  tbody = target_div.find('tbody')
  tr_elements = tbody.find_all('tr')

  result = []

  for tr in tr_elements:
    td_elements = tr.find_all('td')
    if len(td_elements) >= 4:
        data = {
            "model_name": td_elements[0].get_text(),
            "Max RAM required": td_elements[3].get_text(),
        }
        result.append(data)
  with open(destination_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  exec()
