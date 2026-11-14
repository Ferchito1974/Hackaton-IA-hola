import json,sys
sys.stdout.buffer.write(json.loads(sys.stdin.buffer.read().decode('utf-8').strip()).encode('utf-8'))
