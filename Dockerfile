FROM python:3.13-slim AS builder

WORKDIR /site
ARG BUILD_MODE=prod
ENV BUILD_MODE=${BUILD_MODE}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pelican -s pelicanconf-${BUILD_MODE}.py

FROM alpine:latest AS final

COPY --from=builder /site/output /output

RUN echo "Build date: $(date)" | tee -a /output/build_info.txt

RUN apk add --no-cache rsync

ENTRYPOINT ["sh", "-c", "rsync -av /output/ /mnt && echo 'Copied'; date | tee /mnt/updated.txt"]
