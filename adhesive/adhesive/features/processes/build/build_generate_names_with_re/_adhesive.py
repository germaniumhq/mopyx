import adhesive


@adhesive.task('Run? things?')
def run_things(context):
    print("yay run em")


adhesive.build()
