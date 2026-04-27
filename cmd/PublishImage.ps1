docker build -f "Dockerfile" -t "split-api:latest" .
docker tag split-api:latest us-central1-docker.pkg.dev/bill-splitter-ezesaidman/split-app-repo/split-api:latest
docker push us-central1-docker.pkg.dev/bill-splitter-ezesaidman/split-app-repo/split-api:latest
