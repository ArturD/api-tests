
class SingleThreadExecutor:
  def execute(self, tasks):
    for task in tasks:
      yield task.execute()
