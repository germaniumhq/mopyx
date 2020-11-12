import adhesive


@adhesive.task('Notificare Succes')
def notificare_succes(context: adhesive.Token) -> None:
    pass


@adhesive.task('Backup {loop.value}')
def backup_loop_value_(context: adhesive.Token) -> None:
    pass


@adhesive.task('Arhivam serverul {loop,value}')
def arhivam_serverul_loop_value_(context: adhesive.Token) -> None:
    pass


adhesive.bpmn_build("test.bpmn", initial_data={
  "servers": ["a", "b", "c"],
})
