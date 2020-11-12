from gbs_pipeline import pipeline_build_gbs_images


pipeline_build_gbs_images({
    "base_containers": {
        "node8": "germaniumhq/node:8",
        "node12": "germaniumhq/node:12",
    },
})

