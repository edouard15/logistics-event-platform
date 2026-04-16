import json
import time

fixed_name = "vpc"

result = {
    "name": f"{fixed_name}-{int(time.time())}",
}

print(json.dumps(result))
