import textwrap
import uuid
from typing import Optional


def prepare(context,
            platform: str,
            tag: Optional[str]=None,
            gbs_prefix: Optional[str]=None) -> str:

    gbs_prefix = "/" if not gbs_prefix else gbs_prefix

    template = textwrap.dedent(f"""\
        FROM germaniumhq/{platform}

        #======================================
        # Install prerequisite software
        #======================================
        USER root

        COPY --chown=germanium:germanium {gbs_prefix}_gbs/install-software /src{gbs_prefix}_gbs/install-software
        RUN echo "################################################################################" &&\
            echo "# INSTALL SOFTWARE" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/install-software/install-software.sh &&\
            chown -R germanium:germanium /src

        #======================================
        # Prepare dependencies for download
        #======================================
        USER germanium

        # build1
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build1 /src{gbs_prefix}_gbs/prepare-build1
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 1" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build1/prepare-build1.sh

        # build2
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build2 /src{gbs_prefix}_gbs/prepare-build2
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 2" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build2/prepare-build2.sh

        # build3
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build3 /src{gbs_prefix}_gbs/prepare-build3
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 3" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build3/prepare-build3.sh
        """)

    return build_docker_image(context, template, tag)


def test(context,
         platform: str,
         tag: Optional[str]=None,
         gbs_prefix: Optional[str]=None) -> str:

    gbs_prefix = "/" if not gbs_prefix else gbs_prefix

    template = textwrap.dedent(f"""\
        FROM germaniumhq/{platform}

        #======================================
        # Install prerequisite software
        #======================================
        USER root

        COPY --chown=germanium:germanium {gbs_prefix}_gbs/install-software /src{gbs_prefix}_gbs/install-software
        RUN echo "################################################################################" &&\
            echo "# INSTALL SOFTWARE" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/install-software/install-software.sh &&\
            chown -R germanium:germanium /src

        #======================================
        # Prepare dependencies for download
        #======================================
        USER germanium

        # build1
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build1 /src{gbs_prefix}_gbs/prepare-build1
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 1" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build1/prepare-build1.sh

        # build2
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build2 /src{gbs_prefix}_gbs/prepare-build2
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 2" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build2/prepare-build2.sh

        # build3
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build3 /src{gbs_prefix}_gbs/prepare-build3
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 3" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build3/prepare-build3.sh

        # test1
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-test1 /src{gbs_prefix}_gbs/prepare-test1
        RUN echo "################################################################################" &&\
            echo "# PREPARE TEST 1" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-test1/prepare-test1.sh

        # sources are copied only after the test stage
        COPY --chown=germanium:germanium . /src

        # test2
        RUN echo "################################################################################" &&\
            echo "# PREPARE TEST 2" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-test2/prepare-test2.sh

        """)

    return build_docker_image(context, template, tag)

def build(context,
          platform: str,
          tag: Optional[str]=None,
          gbs_prefix: Optional[str]=None) -> str:
    gbs_prefix = "/" if not gbs_prefix else gbs_prefix

    template = textwrap.dedent(f"""\
        FROM germaniumhq/{platform}

        #======================================
        # Install prerequisite software
        #======================================
        USER root

        COPY --chown=germanium:germanium {gbs_prefix}_gbs/install-software /src{gbs_prefix}_gbs/install-software
        RUN echo "################################################################################" &&\
            echo "# INSTALL SOFTWARE" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/install-software/install-software.sh &&\
            chown -R germanium:germanium /src

        #======================================
        # Prepare dependencies for download
        #======================================
        USER germanium

        # build1
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build1 /src{gbs_prefix}_gbs/prepare-build1
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 1" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build1/prepare-build1.sh

        # build2
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build2 /src{gbs_prefix}_gbs/prepare-build2
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 2" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build2/prepare-build2.sh

        # build3
        COPY --chown=germanium:germanium {gbs_prefix}_gbs/prepare-build3 /src{gbs_prefix}_gbs/prepare-build3
        RUN echo "################################################################################" &&\
            echo "# PREPARE BUILD 3" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/prepare-build3/prepare-build3.sh

        # sources are copied only after the test stage
        COPY --chown=germanium:germanium . /src

        # run the build
        RUN echo "################################################################################" &&\
            echo "# RUN BUILD" && \
            echo "################################################################################" &&\
            cd /src && \
            /src{gbs_prefix}_gbs/run-build.sh
        """)
    return build_docker_image(context, template, tag)


def build_docker_image(
        context,
        template: str,
        tag: Optional[str]=None) -> str:
    """ Build a new docker image """
    # FIXME: probably a better temp file/folder creation is needed
    filename = f"/tmp/Dockerfile.{str(uuid.uuid4())}"
    try:
        context.workspace.write_file(filename, template)

        if tag:
            return context.workspace.run(
                f"docker build -q -t {tag} -f {filename} .",
                capture_stdout=True
            ).strip()

        return context.workspace.run(
            f"docker build -q -f {filename} .",
            capture_stdout=True,
        ).strip()
    finally:
        context.workspace.rm(filename)

