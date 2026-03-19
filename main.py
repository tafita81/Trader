import time
from backend.pipeline import run_pipeline

if __name__ == '__main__':
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print('Erro:', e)
        time.sleep(3600)