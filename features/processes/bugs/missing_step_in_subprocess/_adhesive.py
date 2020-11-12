import adhesive


adhesive.process_start()\
    .subprocess_start()\
    .subprocess_start()\
        .task("not existing")\
    .subprocess_end()\
    .subprocess_end()\
    .process_end()\
    .build()

