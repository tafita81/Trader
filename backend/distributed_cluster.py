# Cluster distribuído usando Ray (paralelismo simples)
import ray

ray.init(ignore_reinit_error=True)

@ray.remote
def run_strategy_batch(engine_state, data_batch):
    # engine_state pode ser pesos/modelo serializado
    results = []
    for row in data_batch:
        # simulação simples de cálculo
        signal = sum(row.values())
        results.append(signal)
    return results


def run_distributed(data_rows, n_workers=4):
    chunk_size = max(1, len(data_rows)//n_workers)
    futures = []

    for i in range(0, len(data_rows), chunk_size):
        chunk = data_rows[i:i+chunk_size]
        futures.append(run_strategy_batch.remote({}, chunk))

    results = ray.get(futures)

    # flatten
    flat = [item for sub in results for item in sub]
    return flat
