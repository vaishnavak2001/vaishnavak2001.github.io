# Public GitHub project review

Reviewed 2026-10-02. All 38 public, owner-listed repositories returned by the GitHub API were inventoried (none marked as forks). The previous portfolio listed 28 entries: its valid repository links are retained; PhysioNet digitization is included under the ECG repository; EEG Seizure Detection had only a profile link and no matching public repository, so it is not presented as a verified project.

Scope: README documentation and recursive file inventories for every repository, plus structural review of 72 selected source/notebook files. 71 source/notebook files were parsed; the main ECG classification notebook is malformed JSON, while two digitization notebooks were successfully reviewed. The portfolio repository was reviewed locally. This was not a full code audit or an execution of these projects. No application credentials, configuration values, datasets, notebook outputs, or company folders were read.

Descriptions prioritize implementation evidence over generated README claims. Runtime availability, benchmark figures, medical validity, security guarantees, and production adoption were not independently established. The site therefore distinguishes applications, prototypes, notebooks, learning collections, and README-only concepts.

## Editorial decisions

- DataPilot, Enterprise Guild, WellTrack, and Pneumonia receive new case studies; ControlGym and Retinopathy retain existing case studies.
- The Skin Disorder project uses tabular features, rather than image segmentation.
- WellTrack uses rule-based scoring in its main app; its training pipeline is described separately.
- MediForge includes scaffolding and a dummy-model training/export script. It is presented as a prototype, without unsupported specialist-model or diagnostic-confidence claims.
- The browser image-analysis prototype uses generic MobileNet, without a validated skin-lesion model.
- DroneGym, Autonomous Job Application Agent, and Anti-Gravity contain only READMEs. Their status is explicit in the collection.
- GenderDetc is described as dataset-label classification, without implying that an image establishes a person’s gender.

## Inventory

| Repository | Portfolio title / format | Implementation evidence sampled |
| --- | --- | --- |
| [DataPilot-AI](https://github.com/vaishnavak2001/DataPilot-AI) | DataPilot AI / Application | src/graph.py; src/database.py; src/agents.py; src/visualizer.py |
| [THE_GUILD_V3](https://github.com/vaishnavak2001/THE_GUILD_V3) | Enterprise Guild / Prototype | enterprise-guild-mvp/app/agent.py; enterprise-guild-mvp/mcp_server.py |
| [Web3-Adventurer-s-Guild-MVP](https://github.com/vaishnavak2001/Web3-Adventurer-s-Guild-MVP) | Web3 Adventurer’s Guild / Prototype | web3-adventurers-guild/app/agent.py; web3-adventurers-guild/app/mcp_server.py |
| [chatbot_organization_website](https://github.com/vaishnavak2001/chatbot_organization_website) | Organization Website Chatbot / Application | app/core/orchestrator.py; app/core/retriever.py; app/core/reranker.py |
| [Venture-Analyst-Agent](https://github.com/vaishnavak2001/Venture-Analyst-Agent) | Venture Analyst / Prototype | app.py; src/agents.py; src/graph.py |
| [Multi-Agent-Researcher](https://github.com/vaishnavak2001/Multi-Agent-Researcher) | Multi-Agent Researcher / Prototype | agent_graph.py; app.py |
| [Autonomous-Analyst-Agent](https://github.com/vaishnavak2001/Autonomous-Analyst-Agent) | Autonomous Analyst / Prototype | agent_backend.py; app.py; evaluate.py |
| [career_agent](https://github.com/vaishnavak2001/career_agent) | Career Agent / Prototype | app/agent/orchestrator.py; app/tools/match_scorer.py; app/tools/resume_builder.py |
| [restaurant-rag-agent](https://github.com/vaishnavak2001/restaurant-rag-agent) | Restaurant Knowledge Assistant / Prototype | backend/rag_engine.py; backend/voice_server.py |
| [Project_RAG_Chatbot](https://github.com/vaishnavak2001/Project_RAG_Chatbot) | DocChat AI / Application | app.py; ingest.py; rag.py |
| [capstone-project-the-agentops-guardian-5dgai](https://github.com/vaishnavak2001/capstone-project-the-agentops-guardian-5dgai) | AgentOps Guardian / Notebook | capstone-project-the-agentops-guardian-5dgai.ipynb |
| [capstone-project-the-The-AI-Website-Creator-5dgai](https://github.com/vaishnavak2001/capstone-project-the-The-AI-Website-Creator-5dgai) | AI Website Creator / Notebook | Capstone Project 2  The AI Website Creator 3.ipynb |
| [ControlGym-mass-spring-damper](https://github.com/vaishnavak2001/ControlGym-mass-spring-damper) | ControlGym / Experiment | src/train_ppo_msd.py; controllers/classical_controllers.py; controllers/benchmark.py |
| [Welltrack-ai](https://github.com/vaishnavak2001/Welltrack-ai) | WellTrack AI / Prototype | app.py; models/train_model.py; models/predict.py; app/notifications.py |
| [Diabetic-Retinopathy-Detection](https://github.com/vaishnavak2001/Diabetic-Retinopathy-Detection) | Diabetic Retinopathy Classification / Notebook | Diabetic-Retinopathy-Detection-Google-Colab.ipynb; Diabetic-Retinopathy-Detection-Jypter-notebook.ipynb |
| [Pneumonia-chest-X-Ray-classification](https://github.com/vaishnavak2001/Pneumonia-chest-X-Ray-classification) | Pneumonia Image Classification / Notebook | Pneumonia chest X-Ray classification-Jypter-notebook.ipynb; Pneumonia-chest-X-Ray-classification-Google-colab.ipynb |
| [ecg-classification-cnn-lstm](https://github.com/vaishnavak2001/ecg-classification-cnn-lstm) | ECG Classification & Digitization / Notebooks | physionet-cognitive-digitization-system-7-0.ipynb; physionet-ecg-digitization-guardian-ops-mas.ipynb |
| [skin-disorder-detection](https://github.com/vaishnavak2001/skin-disorder-detection) | Skin Disorder Classification / Notebook | Project-Skin Disorder Detection.ipynb |
| [TrafSignDetc](https://github.com/vaishnavak2001/TrafSignDetc) | Traffic Sign Recognition / Notebook | TrafSignDetc_final_complete.ipynb |
| [PRCP_1002_Handwritten_Digits_Recognition](https://github.com/vaishnavak2001/PRCP_1002_Handwritten_Digits_Recognition) | Handwritten Digit Recognition / Notebook | PRCP_1002_Handwritten_Digits_Recognition.ipynb |
| [CATS-DOGS](https://github.com/vaishnavak2001/CATS-DOGS) | Cats & Dogs Classification / Notebooks | PRAICP-1011_complete_using_jupyter.ipynb; PRAICP-1011_completeusingcolab.ipynb; cats&dogscomplete1usingcolab.ipynb |
| [GenderDetc_complete_using_colab](https://github.com/vaishnavak2001/GenderDetc_complete_using_colab) | Face Dataset Classification Study / Notebook | PRAICP-1001-GenderDetc_complete_using_colab.ipynb |
| [Bike-Rental-Prediction](https://github.com/vaishnavak2001/Bike-Rental-Prediction) | Bike Rental Prediction / Notebooks | PRCP-1018 - Bike Rental Prediction.ipynb; PROJECT-PRCP-1018 - Bike Rental Prediction.ipynb |
| [Car_Price_Prediction](https://github.com/vaishnavak2001/Car_Price_Prediction) | Car Price Prediction / Notebook | Car_Price_Prediction.ipynb |
| [fifa_cluster](https://github.com/vaishnavak2001/fifa_cluster) | FIFA Player Clustering / Notebook | PROJECT_1_PRCP_1004_Fifa20(final).ipynb |
| [IABAC_CDS_Project_2_INX_Future_Emp_Data_V1.6](https://github.com/vaishnavak2001/IABAC_CDS_Project_2_INX_Future_Emp_Data_V1.6) | Employee Performance Analysis / Notebooks | IABAC_CDS_PROJECT.ipynb; IABAC_CDS_PROJECT_FINAL.ipynb |
| [COMP1-TITANIC-](https://github.com/vaishnavak2001/COMP1-TITANIC-) | Titanic Survival Prediction / Notebook | Titanic.ipynb |
| [Advertising_Sales_-_Linear_Regression_-](https://github.com/vaishnavak2001/Advertising_Sales_-_Linear_Regression_-) | Advertising & Sales Regression / Notebook | Advertising_Sales_(_Linear_Regression_).ipynb |
| [Admission_Prediction_-Linear_Regression-](https://github.com/vaishnavak2001/Admission_Prediction_-Linear_Regression-) | Graduate Admission Regression / Notebook | Admission_Prediction(Linear_Regression).ipynb |
| [medtrack-ai](https://github.com/vaishnavak2001/medtrack-ai) | MediForge AI / Prototype | MediForge-v5-Free/src/App.jsx; MediForge-v5-Free/scripts/train_free.py |
| [Privacy-First-Skin-Lesion-Analyzer](https://github.com/vaishnavak2001/Privacy-First-Skin-Lesion-Analyzer) | Browser Image Analysis / Prototype | src/utils/analysis.js; src/hooks/useModel.js |
| [vaishnavak2001.github.io](https://github.com/vaishnavak2001/vaishnavak2001.github.io) | This Portfolio / Website | Local portfolio implementation |
| [ai-bootcamp-](https://github.com/vaishnavak2001/ai-bootcamp-) | AI Bootcamp Explorations / Learning collection | agent_backend.py; agent_graph.py; app.py |
| [Data_science](https://github.com/vaishnavak2001/Data_science) | Data Science Notebooks / Learning collection | 01_Linear Regression/Linear Regression-Python Implementation.ipynb; 01_Linear Regression/Linear_Regression.ipynb; 02_Logistic Regression/Python Implementation.ipynb |
| [Python](https://github.com/vaishnavak2001/Python) | Python Foundations / Learning collection | 01-Introduction-Python.ipynb; ML.ipynb; Pandas/Data Manipulation-02.ipynb |
| [dronegym-rl-quadcopter-attitude](https://github.com/vaishnavak2001/dronegym-rl-quadcopter-attitude) | DroneGym Concept / README only | README and complete file inventory |
| [Autonomous-Job-Application-Agent](https://github.com/vaishnavak2001/Autonomous-Job-Application-Agent) | Job Application Agent Concept / README only | README and complete file inventory |
| [anti-gravity-test1](https://github.com/vaishnavak2001/anti-gravity-test1) | Anti-Gravity Experiment / README only | README and complete file inventory |
