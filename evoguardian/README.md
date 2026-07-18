# EvoGuardian 🛡️

EvoGuardian is a prototype submission for the **Sentient Open Source AGI Grant Program**. It demonstrates an on-device scam protection agent powered by a self-improving loop inspired by **Sentient EvoSkill**.

## How to Run Locally

1. Open your terminal and navigate to the project directory:
   ```bash
   cd evoguardian
   ```

2. Start the local server (requires Python 3.x, no external dependencies needed):
   ```bash
   python3 server.py
   ```

3. Open your browser and navigate to:
   [http://localhost:8000](http://localhost:8000)

## Features Included
- **Agent Simulator:** Enter custom text/SMS messages, run classification, and view step-by-step reasoning traces.
- **EvoSkill Loop:** Run simulated prompt mutations to watch the agent's validation accuracy automatically evolve from 37.5% to 100% based on feedback evaluation.
