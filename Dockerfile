FROM python:3.5-slim AS builder

WORKDIR /site
ARG BUILD_MODE=prod
ENV BUILD_MODE=${BUILD_MODE}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \        
    openssh-client \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN fab build:${BUILD_MODE}

FROM alpine:latest AS final

COPY --from=builder /site/output /output

RUN echo "Build date: $(date)" | tee -a /output/build_info.txt

RUN apk add --no-cache rsync

ENTRYPOINT ["sh", "-c", "rsync -av /output/ /mnt/what-if/ && echo 'Copied'"]
