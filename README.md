# 🐾 Parasite EGG Object Detection (Yolo + Fast API)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLO](https://img.shields.io/badge/Ultralytics_YOLO-v11-blue.svg)](https://https://www.ultralytics.com/yolo/)

<!-- [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/) -->

<!-- ![demo](/Demo_Output.jpg?raw=true "demo") -->

<!-- ## Project Live Demo

Click here for [Live Demo](https://cats-n-dogs-classification.streamlit.app) -->

## Project Overview

ParasitePath AI is a specialized diagnostic tool designed to assist pathologists in identifying parasitic eggs from microscope slide images. By combining high-speed object detection with **_Explainable AI (xAI)_** and **_Retrieval-Augmented Generation (RAG)_**, the system not only identifies species but also provides clinically grounded treatment summaries.

This project demonstrates the transition from a research-based model to a production-ready AI application.

## Features

- **Real-time Detection:** Powered by a customized YOLOv11m model trained for high-precision parasite egg localization.
- **Clinical RAG:** Integrates a Vector Database (ChromaDB) of WHO guidelines to provide instant treatment context for detected species.
- **Explainable AI (xAI):** Utilizes EigenGrad-CAM heatmaps to highlight morphological features (e.g., shell texture) ensuring clinical trust.
- **Production Architecture:** Decoupled FastAPI backend and Streamlit frontend for scalable, high-performance deployment.

## Tech Stack

- **Framework:** PyTorch
- **Architecture:** Yolov11 (Pre-trained on ImageNet)
- **Frontend:** Streamlit
- **Deployment:** Docker
- **Libraries:** Torchvision, PIL, NumPy,Ultralytics,FastAPI

## Installation & Usage

### Prerequisites

- Python 3.8 or higher
- pip or conda for package management

### Setup

Clone the repository:

```bash
git clone https://github.com/Frizz-0/Parasite_Egg_OBD.git
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

<!-- ## Results

The model achieves:

- 99% accuracy on the test set
- 0.03 cross-entropy loss
- Training time of ~20 minutes on GPU T4 -->

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->
