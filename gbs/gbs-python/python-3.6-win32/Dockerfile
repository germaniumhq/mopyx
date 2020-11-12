FROM ubuntu:16.04

RUN useradd -m --home-dir /germanium germanium

ENV DEBIAN_FRONTEND noninteractive

ARG WINE_VERSION=winehq-stable
ARG PYTHON_VERSION=3.6.4
ARG PYINSTALLER_VERSION=3.3

# we need wine for this all to work, so we'll use the PPA
RUN set -x \
    && dpkg --add-architecture i386 \
    && apt-get update -qy \
    && apt-get install --no-install-recommends --allow-unauthenticated -qfy apt-transport-https software-properties-common wget xvfb \
    && wget -nv https://dl.winehq.org/wine-builds/Release.key \
    && apt-key add Release.key \
    && add-apt-repository 'https://dl.winehq.org/wine-builds/ubuntu/' \
    && apt-get update -qy \
    && apt-get install --no-install-recommends --allow-unauthenticated -qfy $WINE_VERSION winbind cabextract \
    && apt-get clean \
    && wget -nv https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
    && chmod +x winetricks \
    && mv winetricks /usr/local/bin

# wine settings
ENV WINEARCH win32
ENV WINEDEBUG fixme-all
ENV WINEPREFIX /germanium/wine


USER germanium

RUN set -x \
    && winetricks win7 \
    && echo 'assoc .py=PythonScript' | wine cmd \
    && echo 'ftype PythonScript=c:\Python36\python.exe "%1" %*' | wine cmd \
    && while pgrep wineserver >/dev/null; do echo "Waiting for wineserver"; sleep 1; done \
    && rm -rf /tmp/.wine-*

COPY override* /germanium/

ENV W_TMP /tmp/wine-tmp

# install Microsoft Visual C++ Redistributable for Visual Studio 2017 dll files
RUN set -x \
    && rm -f "$W_TMP"/* \
    && wget -P "$W_TMP" https://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x86.exe \
    && cabextract -q --directory="$W_TMP" "$W_TMP"/vc_redist.x86.exe \
    && cabextract -q --directory="$W_TMP" "$W_TMP/a10" \
    && cabextract -q --directory="$W_TMP" "$W_TMP/a11" \
    && cd "$W_TMP" \
    && rename 's/_/\-/g' *.dll \
    && cp *.dll $WINEPREFIX/drive_c/windows/system32/ \
    && cat /germanium/override-dll.reg >> /germanium/wine/user.reg \
    && while pgrep wineserver >/dev/null; do echo "Waiting for wineserver"; sleep 1; done \
    && rm -rf /tmp/.wine-*

USER root
RUN chmod +x /germanium/override-dll.sh && /germanium/override-dll.sh

USER germanium

RUN wget -P "$W_TMP" https://repo.continuum.io/miniconda/Miniconda3-4.4.10-Windows-x86.exe && \
    xvfb-run wine $W_TMP/Miniconda3-4.4.10-Windows-x86.exe /InstallationType=JustMe /S /D=C:\\Miniconda3

