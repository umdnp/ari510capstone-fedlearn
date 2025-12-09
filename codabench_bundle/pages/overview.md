# ICU Prolonged Stay Prediction Challenge

## Overview

Welcome to the ICU Prolonged Stay Prediction Challenge! This competition challenges you to build machine learning models that predict whether ICU patients will have prolonged hospital stays (>3 days) based on clinical data available at admission.

## Why This Matters

Predicting ICU length of stay is critical for:
- **Resource Planning**: Allocate beds, staff, and equipment efficiently
- **Patient Care**: Identify high-risk patients who may need additional support
- **Cost Management**: Improve hospital resource utilization
- **Clinical Decision Support**: Help healthcare providers plan discharge and follow-up care

## The Challenge

**Task**: Binary classification
- **Input**: Clinical features from ICU admission
- **Output**: Prediction of prolonged stay (0 = ≤3 days, 1 = >3 days)
- **Evaluation**: F1 Score (macro-averaged)

## Dataset

- **Source**: eICU Collaborative Research Database (demo version)
- **Training**: 1,512 ICU stays with labels
- **Test**: 1,008 ICU stays (labels hidden)
- **Features**: 80+ clinical features including demographics, vital signs, lab values, and APACHE scores
- **Class Balance**: 78.2% not prolonged, 21.8% prolonged

## Getting Started

1. **Download the starting kit** - Includes baseline notebook achieving F1 = 0.7547
2. **Explore the data** - Understand features, missing values, class distribution
3. **Build your model** - Try different algorithms, feature engineering, ensembles
4. **Submit predictions** - Upload CSV with binary predictions for test set
5. **See your score** - Get immediate feedback on the leaderboard

## Baseline Performance

A simple Logistic Regression baseline achieves:
- **F1 Score (Macro)**: 0.7547
- **Accuracy**: 0.8075

Can you beat it?

## Competition Timeline

- **Development Phase**: Ongoing - Submit up to 5 times per day
- **Final Phase**: January 15, 2026 - Select your best 2 submissions

## Prizes

This is an educational competition. Recognition will be given to top performers.

## Get Help

- Review the baseline notebook for a complete example
- Check the data documentation for feature descriptions
- Ask questions in the forum
- Collaborate and learn from other participants!

Good luck! 🏥📊
