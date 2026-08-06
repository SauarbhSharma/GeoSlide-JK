# GeoSlide-JK 2.0 — "GeoSlide Saathi" Multilingual AI Assistant Architecture

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Target Release:** GeoSlide-JK v2.5

---

## 1. Assistant Vision & Core Persona

**"GeoSlide Saathi"** (GEOSLIDE ASSISTANT) is a domain-bounded conversational AI assistant designed to answer citizen and authority queries regarding landslide susceptibility, road corridor status, and pre-monsoon preparedness in Jammu & Kashmir.

---

## 2. Phased Rollout Roadmap

To ensure 100% data grounding and zero unverified advice, GeoSlide Saathi follows a 5-phase rollout strategy:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ PHASE 1:        │ ──► │ PHASE 2:        │ ──► │ PHASE 3:        │ ──► │ PHASE 4:        │ ──► │ PHASE 5:        │
│ Structured FAQ  │     │ Grounded Text   │     │ Multilingual    │     │ Voice Input /   │     │ Official        │
│ Decision Tree   │     │ RAG Assistant   │     │ (Hindi/Urdu/Dog)│     │ Output (Speech) │     │ Workflow Link   │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

- **Phase 1: Structured FAQ Decision Tree (Immediate v2.0):** Deterministic interactive Q&A cards addressing top 20 commuter & authority questions without LLM inference.
- **Phase 2: Grounded Text RAG Assistant (v2.1):** LLM (e.g. Gemini 1.5 Flash) connected strictly via Retrieval-Augmented Generation (RAG) to GeoSlide-JK database & docs.
- **Phase 3: Multilingual Text (v2.2):** Support for English, Hindi, Urdu, Kashmiri, and Dogri text.
- **Phase 4: Voice Input / Output (v2.5):** Speech-to-Text and Text-to-Speech integration for low-literacy commuters.
- **Phase 5: Official Workflow Integration (v3.0):** Direct integration into NHAI work-order dispatches.

---

## 3. Strict Hallucination Safeguards & Citation Enforcement

GeoSlide Saathi operates under 4 strict system prompt constraints:

1. **Strict Database Grounding:** Saathi MUST answer queries using ONLY verified database records retrieved from `/api/v1/location-check`, `/api/v1/terrain/value`, and audited project documentation.
2. **Prohibition of Invented Road Closures:** If a user asks *"Is NH-44 open right now?"*, Saathi MUST NOT invent live status. It MUST reply: *"GeoSlide-JK measures terrain slope instability. For live road blockage and traffic clearance status, please check official J&K Traffic Police advisories at @JKTrafficPolice."*
3. **Mandatory Provenance Citation:** Every answer MUST state its data source (e.g., *"[Source: GeoSlide-JK 100m XGBoost Model, ROC-AUC 0.8694]"*).
4. **Fallback Protocol:** If requested data is missing, Saathi MUST output: *"I do not have verified geospatial data for this specific location. Please consult local district authorities."*
