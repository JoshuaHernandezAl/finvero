class DeleteUseCase:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, task_id):
        self.repository.delete_one(task_id)