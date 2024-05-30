docker run -d --gpus=all -v /home/stankod1/scraper/llm/myollamamodels:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker stop ollama
docker rm ollama

# upgrade
docker pull ollama/ollama
# rerun the container
docker run -d --gpus=all -v /home/stankod1/scraper/llm/myollamamodels:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# non interact
docker exec ollama ollama run gemma:2b
# interacti
docker exec -it ollama ollama run gemma:2b

# client
docker exec -it ollama ollama run gemma:2b
# run model
ollama run llama2

# logs
docker logs ollama

# mapping on the same network (home network)
OLLAMA_HOST=0.0.0.0.11434 docker run -d --gpus=all -v /home/stankod1/scraper/llm/myollamamodels:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# use tailscale for exposing globaly (exposing port is stupid if we dont have authentication!)

https://github.com/ollama/ollama/tree/main?tab=readme-ov-file