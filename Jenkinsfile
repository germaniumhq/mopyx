germaniumPyExePipeline(
    name: "germanium-build-monitor",
    repo: [
        "git@bitbucket.org:bmustiata/germanium-build-monitor.git",
        "git@github.com:germaniumhq/felix.git",
    ],

    binaries: [
        "Win 32": [
            platform: "python:3.6-win32",
            prefix: "/_gbs/win32/",
            exe: "/src/dist/felixbm.exe",
            dockerTag: "germaniumhq/germanium-build-monitor:win32",
        ],

        "Lin 64": [
            platform: "python:3.6",
            prefix: "/_gbs/lin64/",
            exe: "/src/dist/felixbm",
            dockerTag: "germaniumhq/germanium-build-monitor:lin64",
        ]
    ],

    publishAnsiblePlay: "bin/publish.yml",
)
