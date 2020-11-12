
germaniumPyExePipeline(
    runFlake8: false,
    repo: "git@github.com:germaniumhq/germaniumhq-drivers-python.git",
    versionManager: "-l ./version_values.yml",

    preBuild: {
        stage('Test') {
            def parallelTests = [:]

            parallelEach(["python:2.7", "python:3.6"], { platform ->
                node {
                    checkoutWithVersionManager("-l ./version_values.yml")

                    gbs().test([
                        platform: platform,
                        dockerTag: "germanium_drivers_test_${platform}"
                    ]).inside("--link vnc-server -v /dev/shm:/dev/shm --privileged") {
                        junitReports("/src/reports") {
                            // we export the DISPLAY, because we can't do variable references in the
                            // docker.image(..).inside(HERE) because they are not yet defined.
                            sh """
                                export DISPLAY=\$VNC_SERVER_PORT_6000_TCP_ADDR:0
                                cd /src
                                . bin/prepare_firefox.sh
                                behave --junit --no-color -t ~@ie -t ~@edge -t ~@nofirefox
                            """
                        }
                    }
                }
            })
        }
    },

    binaries: [
        "Python 3": [
            platform: "python:3.6",
            dockerTag: "germanium_drivers_py3",
            versionManager: "-l ./version_values.yml",
            // Since it's a sdist publish, just publish from python 3
            publishPypi: "sdist",
        ],
        "Python 2.7": [
            platform: "python:2.7",
            dockerTag: "germanium_drivers_py2",
            versionManager: "-l ./version_values.yml"
        ]
    ],
)

