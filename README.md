---
title: FET2SNN
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# FET2SNN

Pre-TCAD analytical simulation tool for GAA Nanosheet FET to Spiking Neural Network (SNN) accelerator design.

## Features
- **FET2SNN Analytics**: GAA Nanosheet FET device characteristic predictions.
- **SNN Simulator**: Spiking Neural Network simulation with custom Leaky Integrate-and-Fire (LIF) neuron models.
- **TCAD Viewer**: Visualizer for TCAD device structures and parameters.
- **Cadence Workbench**: Thermal-Aware GAA-FET compact model generator for Cadence Virtuoso workflows.

## Deployment on Hugging Face Spaces

This project is configured with a Dockerfile for automated deployment to Hugging Face Spaces.

### Automated Sync via GitHub Actions
Every time you push to the `main` branch of this GitHub repository, it can automatically sync to your Hugging Face Space:
1. Create a Space on Hugging Face (choose **Docker** SDK).
2. Generate a **Write** token from your Hugging Face [Settings > Tokens](https://huggingface.co/settings/tokens).
3. In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add a secret named `HF_TOKEN` containing your Hugging Face token.
4. Update the `.github/workflows/sync-to-hub.yml` file to match your Hugging Face space repository ID (replace `nagamanoj-27/FET2SNN` under `huggingface_repo_id` if it is different).
