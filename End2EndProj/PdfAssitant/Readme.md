## Building Multi Agentic AI RAG With Vector Databse


docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:16


  1. Install Dcoker Desktop
  2. run in Terminal - git bash
  3. Docker will start in docker desktop

  Run
  1. go to directory 
  2. python pddassistant_1.py



  my postgres data credentials

  ai/ai
  5432


