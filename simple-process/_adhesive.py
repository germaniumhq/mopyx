import adhesive


@adhesive.task(re='List files in (.*)')
def list_files_in_folder(context, folder):
    context.workspace.run(f"""
        ls {folder}
    """)


@adhesive.task('Check if /etc/passwd is present')
def check_if_etc_passwd_is_present(context):
    # a return code different than 0 will throw an exception
    context.workspace.run("""
        ls /etc/passwd
    """)


adhesive.bpmn_build("simple.bpmn")
