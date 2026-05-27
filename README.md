# abusive-comments-detection-system

# Abusive Comment Detection System

An AI-powered system designed to detect and filter abusive, toxic, and harmful comments from online platforms using NLP, OCR, and Deep Learning techniques.
The project analyzes comments collected through the YouTube Data API and identifies offensive content automatically to help maintain safer online communities.
The system also supports OCR-based text extraction from images using Tesseract OCR and processes the extracted content for abuse detection.

---

# Objectives
- Detect abusive and toxic comments
- Filter harmful user-generated content
- Analyze YouTube comments automatically
- Extract text from images using OCR
- Build a scalable backend using DDD architecture
  
# Features
- Abusive comment classification
- YouTube comment analysis
- OCR-based text extraction
- NLP preprocessing pipeline
- Pre-trained BERT based prediction model
- REST API support using FastAPI
- Clean Domain-Driven Design (DDD) architecture
- 
# Tech Stack
- Python
- FastAPI
- Pre-trained BERT Model
- Hugging Face Transformers
- TensorFlow / PyTorch
- Tesseract OCR
- OpenCV
- YouTube Data API
- NLP
- 
# Why FastAPI?
FastAPI is used to build high-performance REST APIs for the abuse detection system.

It helps:
- Connect the ML model with external applications
- Process comments through APIs
- Return prediction results in JSON format
- Handle moderation and OCR requests efficiently

# Model Used
This project uses a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model for abusive comment classification.

BERT helps understand contextual meaning in text, improving the accuracy of toxic comment detection compared to traditional NLP approaches.

# Project Structure
```bash
src/
├── domain/
├── application/
├── infrastructure/
├── presentation/

# Workflow
Fetch comments using YouTube Data API
Preprocess and clean text
Extract text from images using Tesseract OCR
Pass text through the pre-trained BERT model
Predict whether content is abusive or safe
Return moderation results through FastAPI endpoints


# Example
Input
"You are stupid and useless"
Output
{
  "label": "abusive",
  "score": 0.97
}

# Project Status:
 Repository setup completed and development in progress.

# Future Improvements
Multi-language abuse detection
Real-time chat moderation
Advanced transformer models
Admin dashboard and analytics
