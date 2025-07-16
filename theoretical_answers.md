# AI Ethics Assignment - Theoretical Answers

## Part 1: Short Answer Questions (30%)

### Q1: Define algorithmic bias and provide two examples of how it manifests in AI systems.

**Answer:**

Algorithmic bias refers to systematic and repeatable errors in AI systems that create unfair outcomes, such as privileging one arbitrary group of users over others. It occurs when algorithms produce results that are systematically prejudiced due to erroneous assumptions in the machine learning process.

**Two Examples:**

1. **Facial Recognition Bias**: Modern facial recognition systems have shown significantly higher error rates for people with darker skin tones, particularly Black women. This bias stems from training datasets that predominantly contain images of light-skinned individuals, leading to poor performance on underrepresented groups.

2. **Credit Scoring Algorithms**: Some credit scoring systems have been found to systematically assign lower credit scores to applicants from certain zip codes or demographic groups, even when controlling for relevant financial factors. This perpetuates historical discrimination patterns present in the training data.

### Q2: Explain the difference between transparency and explainability in AI. Why are both important?

**Answer:**

**Transparency** refers to the openness about how an AI system works, including disclosure of its existence, purpose, data sources, and general methodology. It's about making the process visible and accessible to stakeholders.

**Explainability** refers to the ability to understand and interpret how an AI system arrives at specific decisions or predictions. It involves providing clear, human-understandable explanations for individual outputs.

**Why Both Are Important:**

- **Transparency** builds trust by allowing stakeholders to understand what data is being used and how the system operates at a high level
- **Explainability** enables accountability by allowing users to understand specific decisions, identify potential errors, and contest unfair outcomes
- Together, they enable informed consent, regulatory compliance, and the ability to detect and correct biases
- They are essential for high-stakes applications like healthcare, criminal justice, and financial services

### Q3: How does GDPR (General Data Protection Regulation) impact AI development in the EU?

**Answer:**

GDPR significantly impacts AI development through several key requirements:

1. **Right to Explanation**: Article 22 provides individuals with the right not to be subject to decisions based solely on automated processing, including profiling, which significantly affects them. This requires explainable AI systems.

2. **Data Minimization**: AI systems must only process data that is adequate, relevant, and limited to what is necessary for the specific purpose (Article 5).

3. **Consent and Legal Basis**: AI developers must establish a clear legal basis for processing personal data, often requiring explicit consent for AI applications.

4. **Privacy by Design**: AI systems must incorporate data protection principles from the design phase and throughout the development lifecycle (Article 25).

5. **Data Subject Rights**: Individuals have rights to access, rectify, erase, and port their data, which affects how AI systems store and process personal information.

6. **Impact Assessments**: High-risk AI processing requires Data Protection Impact Assessments (DPIAs) before deployment.

## Part 2: Ethical Principles Matching

**Correct Matches:**

A) **Justice** → Fair distribution of AI benefits and risks.

B) **Non-maleficence** → Ensuring AI does not harm individuals or society.

C) **Autonomy** → Respecting users' right to control their data and decisions.

D) **Sustainability** → Designing AI to be environmentally friendly.

---

## Case Study Analysis (40%)

### Case 1: Biased Hiring Tool - Amazon's AI Recruiting Tool

**Background:** Amazon's AI recruiting tool was found to systematically penalize female candidates by downgrading resumes that included words like "women's" (as in "women's chess club captain") and showed bias against graduates from all-women's colleges.

#### 1. Source of Bias Identification:

**Primary Sources of Bias:**

a) **Training Data Bias**: The system was trained on resumes submitted to Amazon over a 10-year period, during which the tech industry was male-dominated. This historical bias was learned and amplified by the algorithm.

b) **Proxy Variables**: The model learned to associate certain keywords and educational backgrounds with gender, using these as proxies for discrimination.

c) **Feedback Loop Bias**: The system was trained to identify patterns in successful hires, perpetuating existing gender imbalances in the workforce.

#### 2. Three Fixes to Make the Tool Fairer:

**Fix 1: Diverse and Balanced Training Data**

- Re-train the model using a more balanced dataset that represents diverse successful candidates
- Supplement historical data with synthetic data or external datasets to reduce gender imbalance
- Implement temporal weighting to give more importance to recent, more diverse hiring data

**Fix 2: Bias Detection and Mitigation Techniques**

- Implement fairness constraints during model training (e.g., demographic parity, equal opportunity)
- Remove or neutralize gender-indicative features and words from the training process
- Use adversarial debiasing techniques to minimize the model's ability to predict gender from resume features

**Fix 3: Human-AI Collaboration Framework**

- Implement the tool as a decision support system rather than an automated decision-maker
- Require human review for all recommendations, especially for candidates from underrepresented groups
- Establish diverse hiring committees to review AI recommendations and provide oversight

#### 3. Fairness Evaluation Metrics:

**Metric 1: Demographic Parity**

- Measure: P(selected|male) = P(selected|female)
- Ensures equal selection rates across gender groups

**Metric 2: Equal Opportunity**

- Measure: P(selected|qualified, male) = P(selected|qualified, female)
- Ensures qualified candidates have equal chances regardless of gender

**Metric 3: Calibration**

- Measure: P(qualified|score=s, male) = P(qualified|score=s, female)
- Ensures prediction accuracy is consistent across groups

### Case 2: Facial Recognition in Policing

**Background:** Facial recognition systems used in law enforcement have shown higher misidentification rates for minorities, leading to potential wrongful arrests and civil rights violations.

#### 1. Ethical Risks Discussion:

**Primary Ethical Risks:**

a) **Wrongful Arrests and False Accusations**: Higher false positive rates for minorities can lead to innocent people being arrested, prosecuted, and potentially imprisoned.

b) **Privacy Violations**: Mass surveillance capabilities infringe on citizens' right to privacy and anonymity in public spaces.

c) **Discriminatory Enforcement**: Disproportionate targeting of minority communities can exacerbate existing inequalities in the criminal justice system.

d) **Erosion of Civil Liberties**: Creates a surveillance state that can chill free speech, assembly, and other constitutional rights.

e) **Lack of Consent**: Citizens cannot opt out of being subjected to facial recognition in public spaces.

#### 2. Responsible Deployment Policy Recommendations:

**Policy 1: Accuracy and Bias Standards**

- Mandate minimum accuracy thresholds (e.g., >99.5%) across all demographic groups before deployment
- Require regular bias audits with results published publicly
- Establish independent oversight bodies to monitor system performance

**Policy 2: Limited Use Cases and Human Oversight**

- Restrict use to serious crimes (e.g., violent felonies, terrorism) rather than minor offenses
- Require human verification before any arrest based on facial recognition matches
- Implement time limits on data retention and require judicial warrants for identification

**Policy 3: Transparency and Accountability**

- Mandate public disclosure when facial recognition technology is used
- Provide clear appeals processes for individuals wrongly identified
- Require comprehensive training for law enforcement on system limitations and bias risks

**Policy 4: Community Engagement**

- Involve community stakeholders in deployment decisions
- Provide opt-out mechanisms where technically feasible
- Regular public reporting on usage statistics and accuracy metrics

---

_This document provides comprehensive theoretical analysis of AI ethics principles and detailed case study solutions as required by the assignment guidelines._
