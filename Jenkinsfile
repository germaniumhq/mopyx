germaniumPyExePipeline(
    repo: "git@github.com:bmustiata/version-manager-py.git",
    binaries: [
        "Lin 64": [
            exe: "/src/dist/version-manager",
            platform: "python:3.6",
            dockerTag: "version_manager:${env.BUILD_NUMBER}",
            publishPypi: "sdist"
        ]
    ]
)

