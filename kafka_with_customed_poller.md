# 🚀 Next: Design a service with Custom Python Poller and Kafka

## Steps:
1. **Write a custom Python polling script** to query a metadata source for changes.
2. **Wrap that poller** as a Kafka Connect source
3. **Run it as a Service in Docker** via Docker Compose
4. **Schedule the poller** using cron inside the container

This approach allows you to:
* Have full control over logic
* Tolerate rate limits from the source
* Track timestamps in your own state

## The **Docker Compose environment** includes:

* **Kafka** (Confluent platform)
* **Neo4j**
* **Kafka UI** (to inspect topics)
* **Custom Python Poller** that pulls from the metadata source and produces to Kafka

---

## Project Layout

```
source-sync/
├── 🐳docker-compose.yml
├── 🧠poller/
│   ├── 🐳Dockerfile
│   ├── 🐍poll_source.py
│   ├── 🐍requirements.txt
│   └── ✅state.json  ← stores last sync timestamp
└── 📄.env           ← stores sensitive configs
```

---

## Once completed, run it

1. Run:

```bash
docker-compose up --build
```

2. Check Kafka UI to see your Kafka topic populated

3. Verify your Neo4j is up and ready

## Schedule the poller
Updated poller

```
poller/
├── Dockerfile
├── poll_collibra.py
├── requirements.txt
├── cronjob.txt         👈 Add
└── state.json          
```

Update Dockerfile, rebuild and Start

```bash
docker-compose build poller
docker-compose up -d poller