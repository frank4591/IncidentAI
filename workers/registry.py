from workers.base import Worker


class DefaultWorkerRegistry:

    def __init__(self, workers: list[Worker]):
        self._workers = {
            worker.capability: worker
            for worker in workers
        }

    def resolve(self, capability: str) -> Worker:

        if capability not in self._workers:
            raise KeyError(
                f"No worker registered for capability: {capability}"
            )

        return self._workers[capability]