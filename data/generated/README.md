# Synthetic company knowledge base

This directory includes `company_knowledge_base.csv`, an export of **50,000 unique synthetic enterprise documents** across **26 projects**, with 20 document types, classification metadata, department, owner, and allowed-role fields. Project Bumblebee is included.

The same canonical records are stored in `../company_copilot.db`, table `documents`, so the application can query them locally. The CSV is included so the full corpus is visible, searchable, and usable independently of the application. Every record is fictional and marked synthetic; do not treat it as real-company information.

Validation counts are in `../../reports/data_validation.json`.
