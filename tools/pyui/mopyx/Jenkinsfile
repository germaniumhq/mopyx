germaniumPyExePipeline(
    repo: "git@github.com:germaniumhq/mopyx.git",

    preBuild: {
        stage('Test') {
            node {
                checkoutWithVersionManager()

                gbs().test([
                    platform: 'python:3.6',
                    dockerTag: 'mopyx-test'
                ]).inside {
                    sh """
                        cd /src
                        python -m unittest
                    """
                }
            }
        }
    },

    binaries: [
        "Lin 64": [
            platform: "python:3.6",
            dockerTag: "mopyx",
            publishPypi: "sdist"
        ]
    ]
)

