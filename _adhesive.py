from gbs_pipeline import pipeline_build_gbs_images


pipeline_build_gbs_images({
    "base_containers": {
        "jdk8": "germaniumhq/jdk:8",
    },
})

