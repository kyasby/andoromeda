import andoromeda as ad
import json

m1 = ad.mdgFiware()
data = {
  'people': {'right': 0, 'left': 0},
  'car': {'right': 64, 'left': 46},
  'truck': {'right': 150, 'left': 55},
  'bus': {'right': 23, 'left': 23},
  'motorcycle': {'right': 15, 'left': 1},
}
m1.show_config()
m1.sendData(json.dumps(data), '2021-05-10 14:08:00.016578+09:00')