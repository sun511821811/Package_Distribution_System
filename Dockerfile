FROM python:3.9-slim-bookworm

# Install system dependencies
# OpenJDK 17 is required for Android SDK tools
RUN apt-get update && apt-get install -y \
    default-jdk-headless \
    build-essential \
    curl \
    unzip \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Install Android SDK Command Line Tools
RUN mkdir -p $ANDROID_HOME/cmdline-tools \
    && curl -o cmdline-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \
    && unzip cmdline-tools.zip -d $ANDROID_HOME/cmdline-tools \
    && mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest \
    && rm cmdline-tools.zip

# Accept Licenses and Install SDK Packages
# build-tools;34.0.0, platforms;android-35, and NDK (26.1.10909125 is a stable LTS version)
RUN yes | sdkmanager --licenses \
    && sdkmanager "platform-tools" "build-tools;34.0.0" "platforms;android-35" "ndk;26.1.10909125"

# Set NDK Environment Variable
ENV ANDROID_NDK_HOME=$ANDROID_HOME/ndk/26.1.10909125
ENV PATH=$PATH:$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install apk-secure from GitHub
RUN pip install --no-cache-dir https://raw.githubusercontent.com/sun511821811/apk_secure_tool/main/dist/apk_secure_tool-0.1.0-py3-none-any.whl

# Copy Config Patch
COPY docker_apk_secure_config.yaml /app/docker_apk_secure_config.yaml

# Copy Project Files
COPY . .

# Create directories for uploads and temp
RUN mkdir -p uploads temp_downloads temp_work temp_execution temp_keystores

# Script to patch config and start app
RUN echo '#!/bin/bash\n\
# Patch apk-secure config\n\
cp /app/docker_apk_secure_config.yaml /usr/local/lib/python3.9/site-packages/apk_secure/config/config.yaml\n\
\n\
# Run the command passed to docker run\n\
exec "$@"' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
