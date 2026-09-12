# CLAUDE CODE MASTER PROMPT

# Build a Complete AI Home Intelligence Hub

You are a senior full-stack engineer, AI product architect, UI/UX designer, frontend engineer, and intelligent-systems developer.

Build a **complete, polished, production-quality web application** called **AI Home Intelligence Hub**.

This is not a basic CRUD application, generic chatbot, or simple dashboard.

The product should feel like a premium intelligent home-management platform where users can create a digital model of their home and receive useful, explainable recommendations for:

* Home organization
* Furniture placement
* Space utilization
* Energy usage
* Maintenance
* Security awareness
* Comfort
* Accessibility
* Home improvements
* Room-by-room optimization

The final application must have a strong frontend experience, meaningful AI-agent orchestration, functional interactions, and a polished visual identity.

---

# 1. CORE CONCEPT

The platform helps users understand and improve their home through a digital home profile.

The primary experience should be:

```text
User
 ↓
Create Home Profile
 ↓
Add Rooms
 ↓
Define Room Dimensions
 ↓
Add Furniture and Appliances
 ↓
Set Lifestyle and Preferences
 ↓
Add Energy, Maintenance, and Security Information
 ↓
AI Home Intelligence System
 ↓
Analyze Home
 ↓
Generate Home Intelligence Report
 ↓
Explore Recommendations
 ↓
Compare Improvement Scenarios
 ↓
Apply Changes to Digital Home Model
 ↓
Track Tasks and Improvements
```

The user should not feel like they are simply chatting with an AI.

The product should feel like:

```text
Digital Home Planner
+
AI Interior and Space Advisor
+
Home Maintenance Assistant
+
Energy Intelligence Tool
+
Personal Home Operating System
```

The application must provide structured outputs, visual summaries, actionable recommendations, and interactive room-level exploration.

---

# 2. REQUIRED TECHNOLOGY

Use exactly the following technology pattern.

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* OpenAI Python SDK
* Jinja2

## Frontend

* HTML
* Tailwind CSS
* Vanilla JavaScript

## AI Model

Use:

```text
OpenAI GPT-4.1-mini
```

The OpenAI API key must remain server-side.

Do not expose the API key in frontend JavaScript.

## Do not use

* React
* Next.js
* Vue
* Angular
* Node.js frontend
* Separate frontend server
* PostgreSQL
* MongoDB
* Redis
* Docker unless absolutely required
* Unnecessary microservices
* Complex authentication
* Payment systems
* External infrastructure that is not required for the core experience

FastAPI must serve the complete website.

Run with:

```bash
uvicorn app.main:app --reload --port 8000
```

Website:

```text
http://localhost:8000
```

---

# 3. IMPORTANT EXISTING STYLES FILE

Before changing the interface:

1. Inspect the existing project structure.
2. Locate the existing styles file.
3. Understand existing CSS variables, utilities, spacing, typography, components, and design conventions.
4. Reuse compatible styles where appropriate.
5. Do not blindly delete useful existing styles.
6. Refactor only when necessary.
7. Keep the styling system maintainable.
8. If the existing styles are empty or insufficient, create a complete professional design system.

Inspect the existing project before modifying it.

Do not assume the project is empty.

---

# 4. DESIGN DIRECTION

Create a premium, modern, calm, intelligent home-technology experience.

The visual language should feel like a combination of:

```text
Premium home-design magazine
+
Modern intelligent SaaS product
+
Digital twin interface
+
Architecture and space-planning tool
+
Personal home operating system
```

Use a refined light-theme design.

The interface should feel:

* Architectural
* Calm
* Spacious
* Precise
* Warm
* Professional
* Intelligent
* Editorial
* Highly usable
* Visually structured

Avoid:

* Generic AI dashboards
* Excessive cards inside cards
* Overuse of gradients
* Neon colors
* Excessive glassmorphism
* Dark sci-fi styling
* Template-looking layouts
* Unnecessary decorative elements
* Fake 3D visuals that do not provide useful information
* Interfaces that look like a student project

The design must have a clear product identity.

---

# 5. VISUAL IDENTITY

Use a sophisticated home-inspired palette.

## Base colors

* Warm white
* Soft ivory
* Light stone
* Pale taupe
* Architectural gray
* Muted charcoal
* Soft beige

## Accent colors

Use restrained accents such as:

* Olive
* Sage
* Muted terracotta
* Warm amber
* Dusty blue
* Deep forest green

Use color to communicate meaning:

* Green for healthy or optimized conditions
* Amber for attention required
* Red only for important warnings
* Blue for information
* Neutral tones for structure and layout

Do not use bright colors everywhere.

Do not use gradients as the main visual identity.

---

# 6. TYPOGRAPHY

Create a strong typographic hierarchy.

Use:

* Large editorial headings
* Clear section headings
* Comfortable body text
* Small descriptive labels
* Strong numerical emphasis
* Consistent button typography
* Readable forms
* Excellent line height

The interface should feel premium without making every element bold.

Use typography to distinguish:

* Home overview
* Room names
* Intelligence scores
* Recommendations
* Warnings
* Tasks
* Technical details
* AI explanations

---

# 7. RESPONSIVE DESIGN

The application must be fully responsive.

Support:

```text
Large desktop
Desktop
Laptop
Tablet
Mobile
```

Do not simply shrink the desktop version.

Create intentional layouts for small screens.

On mobile:

* Navigation must become usable
* Room cards must remain readable
* Digital floor-plan previews must remain usable
* Tables should become stacked layouts where appropriate
* Side panels should become bottom sheets or full-width sections
* Forms should use comfortable spacing
* Important actions must remain easy to access
* No horizontal page overflow
* No clipped content
* No tiny controls

---

# 8. GLOBAL NAVIGATION

Create a polished global navbar.

Desktop navigation:

```text
Logo
Home
My Home
Rooms
Insights
Recommendations
Tasks
About

[Analyze Home]
```

Include:

* Active navigation state
* Responsive mobile menu
* Clear primary CTA
* Subtle border or shadow on scroll
* Accessible keyboard navigation

Mobile navigation should include:

```text
Logo
Menu button
```

The mobile menu must contain all important navigation links.

---

# 9. MAIN APPLICATION PAGES

Create the following pages:

```text
/
 /home
 /rooms
 /rooms/{room_id}
 /insights
 /recommendations
 /tasks
 /settings
 /about
 /faq
 /contact
 /404
```

The exact routing structure may be adapted to the existing project, but all major experiences must be accessible.

---

# 10. HOME PAGE

Create a complete homepage that introduces the product.

Sections:

```text
Navbar
Hero
Home Intelligence Preview
How It Works
Core Capabilities
Room Intelligence Preview
Energy and Maintenance Preview
AI Recommendation Preview
Benefits
Privacy and Data Explanation
CTA
Footer
```

The homepage should immediately communicate:

```text
Understand your home.
Improve every space.
Make better decisions.
```

Suggested hero messaging:

```text
Your home, understood intelligently.

Build a digital model of your home and receive practical recommendations
for space, comfort, energy, maintenance, security, and everyday living.
```

Primary CTA:

```text
Build My Home
```

Secondary CTA:

```text
Explore Intelligence
```

Do not make the homepage look like an admin dashboard.

It should feel like a premium product landing page connected to a real application.

---

# 11. HOME SETUP EXPERIENCE

Create a guided home setup flow.

The setup should feel like a polished onboarding experience rather than a long ordinary form.

Use a multi-step interface:

```text
1. Home Profile
2. Rooms
3. Furniture
4. Appliances
5. Lifestyle
6. Energy
7. Maintenance
8. Security
9. Review
```

Show:

* Progress indicator
* Current step
* Completed steps
* Back and continue controls
* Save draft behavior
* Validation messages
* Helpful descriptions
* Empty states
* Review summary before analysis

The user must be able to move backward without losing entered information.

---

# 12. STEP 1: HOME PROFILE

Ask for:

* Home name
* Home type
* Approximate location or climate zone
* Number of residents
* Number of floors
* Approximate total area
* Ownership status
* Main goals

Home type options:

```text
Apartment
House
Villa
Studio
Townhouse
Shared Home
Office-Home
Other
```

Main goals may include:

```text
Improve organization
Use space better
Reduce energy waste
Improve comfort
Plan maintenance
Improve security awareness
Prepare for renovation
Make the home more accessible
Create a calmer environment
Track home improvements
```

Allow multiple goals.

Do not require exact personal address information.

Use broad location or climate information only when needed for recommendations.

---

# 13. STEP 2: ROOM BUILDER

Allow users to add multiple rooms.

Each room should include:

* Room name
* Room type
* Length
* Width
* Ceiling height
* Floor level
* Natural light level
* Window count
* Door count
* Primary purpose
* Current problems
* Preferred style
* Priority

Room types:

```text
Living Room
Bedroom
Kitchen
Bathroom
Dining Room
Home Office
Study
Balcony
Hallway
Storage Room
Laundry Room
Guest Room
Kids Room
Outdoor Area
Other
```

Allow:

* Add room
* Edit room
* Duplicate room
* Delete room
* Reorder rooms
* Mark room as high priority
* View room summary

Display rooms using polished visual cards.

Each room card should show:

* Room name
* Room type
* Approximate dimensions
* Main issue
* Room completion status
* Intelligence status
* Open room button

---

# 14. DIGITAL HOME MODEL

Create a visual digital representation of the home.

This does not need to be a real architectural CAD system.

However, it must feel interactive and useful.

Implement a simplified floor-plan representation using HTML, CSS, and SVG where appropriate.

The digital model should support:

* Multiple floors
* Room blocks
* Room labels
* Room dimensions
* Furniture markers
* Appliance markers
* Door and window indicators
* Room selection
* Highlighted priority rooms
* Basic room positioning
* Zoom controls where practical
* Reset view
* Responsive behavior

The digital model must be based on the user's entered data.

Do not create a fake static floor plan unrelated to the user's input.

If exact architectural geometry is not possible, use a clearly labeled simplified representation.

---

# 15. FURNITURE BUILDER

Allow users to add furniture to each room.

Furniture fields:

* Name
* Category
* Width
* Depth
* Height
* Position
* Current condition
* Usage frequency
* Importance
* Whether it can be moved
* Whether it blocks movement
* Notes

Furniture categories:

```text
Sofa
Bed
Desk
Chair
Dining Table
Wardrobe
Cabinet
Bookshelf
TV Unit
Coffee Table
Storage Box
Dresser
Kitchen Unit
Other
```

Display furniture in:

* Furniture list
* Room overview
* Simplified floor-plan preview
* Space utilization summary

Allow users to edit and remove furniture.

---

# 16. APPLIANCE BUILDER

Allow users to add appliances.

Appliance fields:

* Appliance name
* Category
* Approximate age
* Usage frequency
* Estimated power rating if known
* Typical daily usage
* Condition
* Maintenance status
* Energy-efficiency label if known
* Notes

Categories:

```text
Refrigerator
Air Conditioner
Fan
Washing Machine
Dryer
Water Heater
Oven
Microwave
Television
Computer
Lighting
Water Pump
Other
```

If the user does not know power consumption, allow the field to remain unknown.

Never present estimated energy data as measured data.

Clearly label estimates.

---

# 17. LIFESTYLE AND PREFERENCES

Ask questions that improve recommendations.

Examples:

* Do you work from home?
* Do you host guests often?
* Do you have children?
* Do you have pets?
* Do you prefer open spaces or more storage?
* Do you prefer minimal or decorative interiors?
* Do you prioritize comfort, efficiency, aesthetics, or practicality?
* Do you have mobility or accessibility considerations?
* Do you prefer low-cost changes or larger improvements?
* How much time do you have for maintenance?
* What is your preferred home style?

Style options:

```text
Minimal
Modern
Warm Contemporary
Traditional
Japandi-inspired
Industrial
Classic
Eclectic
Natural
Functional
Undecided
```

Do not turn these preferences into unsupported psychological claims.

---

# 18. ENERGY PROFILE

Create an energy information section.

Allow users to enter:

* Electricity provider or tariff label
* Approximate monthly bill
* Currency
* Typical monthly consumption if known
* Main cooling method
* Main heating method
* Lighting type
* Solar availability
* Backup power availability
* Peak usage periods
* Frequently used appliances
* Energy concerns

The system should distinguish between:

```text
User-provided data
Estimated data
AI-generated recommendations
```

Do not claim exact savings without reliable measurements.

Use language such as:

```text
Potential improvement
Estimated opportunity
Possible reduction
Requires measurement
```

---

# 19. MAINTENANCE PROFILE

Allow users to track home maintenance.

Maintenance categories:

```text
Electrical
Plumbing
HVAC
Roof
Walls and Paint
Windows and Doors
Appliances
Pest Control
Water Systems
Safety Equipment
Furniture
Outdoor Areas
Other
```

Each maintenance item should include:

* Title
* Category
* Room
* Last checked date
* Next suggested check date
* Condition
* Priority
* Notes
* Status

Statuses:

```text
Not Started
Planned
In Progress
Completed
Needs Attention
```

Do not present AI suggestions as professional inspections.

---

# 20. SECURITY AWARENESS PROFILE

Create a non-invasive security-awareness section.

Allow users to record:

* Entry points
* Door locks
* Window locks
* Outdoor lighting
* Smoke alarms
* Carbon monoxide alarms where relevant
* Emergency exits
* First-aid kit availability
* Fire extinguisher availability
* Backup communication plan
* Important emergency notes

Do not request passwords, access codes, surveillance credentials, or sensitive security secrets.

The AI should provide general safety-awareness suggestions only.

Include a clear disclaimer:

```text
This feature provides general home-safety guidance.
It is not a professional security assessment or emergency service.
```

---

# 21. AI HOME INTELLIGENCE SYSTEM

Create a meaningful multi-agent architecture.

Use clear separation of responsibilities.

Suggested architecture:

```text
User Home Profile
        ↓
Home Data Validator
        ↓
Home Intelligence Orchestrator
        ↓
 ┌───────────────────────────────┐
 │                               │
Space Planning Agent       Organization Agent
Energy Insight Agent       Maintenance Agent
Comfort Agent              Safety Awareness Agent
Accessibility Agent        Improvement Planning Agent
Cost and Priority Agent    Critic and Validation Agent
 │                               │
 └───────────────┬───────────────┘
                 ↓
        Structured Intelligence Report
                 ↓
        Recommendation Renderer
```

The agents do not need to run as separate infrastructure services.

Implement them as clean Python modules or classes.

Each agent must have:

* A clear responsibility
* Defined input data
* Structured output
* Validation
* Error handling
* Explainable reasoning summary
* No unsupported claims

---

# 22. AGENT RESPONSIBILITIES

## Home Intelligence Orchestrator

Responsible for:

* Validating the home profile
* Selecting relevant agents
* Combining agent outputs
* Prioritizing recommendations
* Removing duplicates
* Creating the final report
* Ensuring recommendations match the user's goals

## Space Planning Agent

Analyze:

* Room dimensions
* Furniture sizes
* Movement paths
* Unused areas
* Crowded areas
* Furniture placement
* Functional zones

Return:

* Space issues
* Suggested layout changes
* Furniture movement suggestions
* Confidence level
* Explanation
* Expected benefit

Do not claim exact architectural compliance.

## Organization Agent

Analyze:

* Storage availability
* Clutter patterns
* Room purpose
* Frequently used items
* Furniture and storage units

Return:

* Organization opportunities
* Storage recommendations
* Decluttering sequence
* Room-by-room actions
* Difficulty level
* Estimated effort

## Energy Insight Agent

Analyze:

* User-provided energy information
* Appliance usage
* Cooling and heating habits
* Lighting information
* Peak usage periods

Return:

* Potential energy opportunities
* Appliance usage observations
* Behavioral suggestions
* Priority actions
* Measurement requirements

Do not invent exact savings.

## Maintenance Agent

Analyze:

* Maintenance records
* Appliance ages
* Condition
* Last inspection dates
* Home systems

Return:

* Overdue or upcoming maintenance items
* Suggested maintenance schedule
* Priority levels
* Suggested professional follow-up where appropriate

## Comfort Agent

Analyze:

* Natural light
* Room purpose
* Temperature concerns
* Noise concerns
* Furniture layout
* User preferences

Return:

* Comfort improvements
* Lighting suggestions
* Layout adjustments
* Ventilation considerations
* Noise-reduction ideas

## Safety Awareness Agent

Analyze:

* Entry points
* Smoke alarms
* Emergency exits
* Lighting
* Safety equipment
* User-provided concerns

Return:

* General safety-awareness suggestions
* Missing information
* Priority checks
* Clear limitations

## Accessibility Agent

Analyze:

* Room layout
* Movement paths
* Furniture placement
* Door and hallway information
* User-provided accessibility needs

Return:

* Possible accessibility improvements
* Obstruction warnings
* Clear-path suggestions
* Recommendations that require professional assessment

## Improvement Planning Agent

Analyze all relevant recommendations.

Return:

* Quick wins
* Low-cost improvements
* Medium-effort improvements
* Larger projects
* Suggested sequence
* Dependencies
* Required materials or services

## Cost and Priority Agent

Organize recommendations according to:

* Impact
* Effort
* Estimated cost range
* Urgency
* User goals
* Dependencies

All costs must be clearly labeled as estimates.

## Critic and Validation Agent

Check:

* Contradictory recommendations
* Duplicate suggestions
* Unsupported claims
* Missing assumptions
* Safety concerns
* Unrealistic recommendations
* Recommendations that exceed available data

The final output must not contain internal prompts or private reasoning traces.

Return concise explanations rather than hidden chain-of-thought.

---

# 23. HOME ANALYSIS EXPERIENCE

Create a premium analysis flow.

When the user clicks:

```text
Analyze My Home
```

Show a multi-stage progress interface:

```text
Reviewing home profile
Mapping rooms
Analyzing space usage
Reviewing organization
Checking energy opportunities
Reviewing maintenance
Evaluating safety awareness
Prioritizing improvements
Preparing your home intelligence report
```

Do not use a generic spinner only.

Use:

* Progress steps
* Completed states
* Current active state
* Helpful contextual messages
* Graceful failure state
* Retry action

After successful analysis, redirect to or reveal the Home Intelligence Report.

---

# 24. HOME INTELLIGENCE REPORT

Create a visually rich report page.

Include:

## Overall overview

* Home name
* Number of rooms
* Number of furniture items
* Number of appliances
* Number of open tasks
* Analysis date
* Data completeness indicator

## Intelligence categories

Display categories such as:

```text
Space
Organization
Energy
Maintenance
Comfort
Safety Awareness
Accessibility
Improvement Potential
```

Do not invent scientifically validated scores.

If scores are used, label them as:

```text
AI-generated planning indicators
```

Explain how they are calculated from the user's entered information.

## Priority summary

Show:

* Top 3 actions
* Quick wins
* High-priority issues
* Missing information
* Suggested next step

## Room-by-room overview

Each room should show:

* Main observations
* Top recommendations
* Space status
* Maintenance status
* Organization status
* Open room details button

---

# 25. RECOMMENDATION CARDS

Every recommendation must include:

* Title
* Category
* Room or area
* Why it matters
* Suggested action
* Expected benefit
* Effort level
* Estimated cost range if relevant
* Priority
* Confidence
* Assumptions
* Whether professional assessment is needed
* Add to tasks button
* Mark as completed button
* Dismiss button
* Save button

Priority options:

```text
Low
Medium
High
Urgent Attention
```

Use “Urgent Attention” only for reasonable safety or maintenance concerns, not ordinary design suggestions.

Do not create recommendations that only look functional.

Every action must work.

---

# 26. RECOMMENDATION FILTERING AND SORTING

Allow users to filter recommendations by:

* Category
* Room
* Priority
* Cost
* Effort
* Status
* Saved items
* Completed items

Allow sorting by:

* Highest priority
* Lowest effort
* Lowest estimated cost
* Highest potential impact
* Room
* Newest

Filtering and sorting should work locally without unnecessary AI requests.

---

# 27. WHAT-IF SCENARIOS

Create an interactive scenario feature.

Users should be able to explore changes such as:

```text
Move the sofa
Add storage
Remove a furniture item
Create a home office zone
Replace lighting
Reduce appliance usage
Add a maintenance task
Reorganize a room
Improve entryway organization
```

The scenario interface should show:

* Current state
* Proposed change
* Potential benefits
* Possible trade-offs
* Estimated effort
* Affected rooms
* Required follow-up actions

Allow users to compare:

```text
Current Home
vs.
Proposed Improvement
```

Do not claim that the scenario is an exact architectural or engineering simulation.

---

# 28. ROOM DETAIL PAGE

Each room must have a dedicated page or detailed panel.

Include:

* Room name
* Room type
* Dimensions
* Room purpose
* User preferences
* Digital room preview
* Furniture list
* Appliance list
* Current problems
* AI observations
* Recommendations
* Maintenance items
* Room tasks
* Edit room button
* Analyze room button

Room analysis should use only the relevant room data plus necessary home context.

Do not send the entire home profile to the AI when a room-level analysis is sufficient.

---

# 29. TASK MANAGEMENT

Create a functional home-improvement task system.

Each task should include:

* Title
* Description
* Category
* Room
* Priority
* Status
* Due date
* Estimated cost
* Estimated effort
* Notes
* Source recommendation

Statuses:

```text
To Do
In Progress
Blocked
Completed
Archived
```

Support:

* Add task
* Edit task
* Delete task
* Mark complete
* Reopen task
* Filter tasks
* Sort tasks
* View by room
* View by priority
* View timeline

Use local storage or JSON persistence as appropriate.

Do not create fake task buttons.

---

# 30. HOME IMPROVEMENT ROADMAP

Create a roadmap view.

Organize improvements into:

```text
Today
This Week
This Month
Later
```

The roadmap should consider:

* Priority
* Dependencies
* Effort
* Cost
* Room
* User goals

Show a clear explanation of why tasks are placed in a particular order.

---

# 31. DATA STORAGE

Since there is no login or database requirement, use a practical local data strategy.

Use:

* Browser localStorage for current user experience and saved state
* JSON files for seeded reference data or optional server-side submissions
* Reusable storage utilities
* Clear separation between frontend session data and server data

Do not claim cloud synchronization.

Do not claim long-term personalization beyond the available storage mechanism.

Suggested data files:

```text
app/data/
├── room_types.json
├── furniture_catalog.json
├── appliance_categories.json
├── maintenance_categories.json
├── recommendation_templates.json
├── feedback.json
└── contacts.json
```

---

# 32. API DESIGN

Implement clean FastAPI routes.

Example page routes:

```text
GET  /
GET  /home
GET  /rooms
GET  /rooms/{room_id}
GET  /insights
GET  /recommendations
GET  /tasks
GET  /settings
GET  /about
GET  /faq
GET  /contact
```

Example API routes:

```text
GET  /api/home
POST /api/home
PUT  /api/home
DELETE /api/home

GET  /api/rooms
POST /api/rooms
GET  /api/rooms/{room_id}
PUT  /api/rooms/{room_id}
DELETE /api/rooms/{room_id}

POST /api/ai/analyze-home
POST /api/ai/analyze-room
POST /api/ai/generate-recommendations
POST /api/ai/compare-scenario
POST /api/ai/energy-insights
POST /api/ai/maintenance-plan
POST /api/ai/organization-plan

GET  /api/recommendations
POST /api/recommendations/{recommendation_id}/save
POST /api/recommendations/{recommendation_id}/complete
POST /api/recommendations/{recommendation_id}/dismiss

GET  /api/tasks
POST /api/tasks
PUT  /api/tasks/{task_id}
DELETE /api/tasks/{task_id}

POST /api/feedback
POST /api/contact
```

Use proper Pydantic models for all request and response bodies.

---

# 33. PYDANTIC MODELS

Create structured models for:

```text
HomeProfile
Room
FurnitureItem
Appliance
LifestylePreferences
EnergyProfile
MaintenanceItem
SecurityProfile
HomeAnalysisRequest
RoomAnalysisRequest
Recommendation
RecommendationList
ScenarioRequest
ScenarioComparison
HomeTask
Feedback
ContactSubmission
```

Use validation for:

* Positive dimensions
* Valid room types
* Valid priority values
* Valid statuses
* Reasonable numeric ranges
* Optional fields
* Currency values
* Date formats

Do not allow malformed AI output to reach the frontend unchecked.

---

# 34. AI SERVICE

Create:

```text
app/services/openai_service.py
```

Centralize all OpenAI communication.

Functions may include:

```python
analyze_home()
analyze_room()
generate_recommendations()
generate_energy_insights()
generate_maintenance_plan()
compare_scenario()
```

Do not scatter OpenAI calls throughout route files.

The agent modules should sit above the OpenAI service.

The OpenAI service should handle:

* Model selection
* System instructions
* Structured output requests
* Timeouts
* Error handling
* Response parsing
* Logging without secrets

Use:

```text
gpt-4.1-mini
```

---

# 35. AI OUTPUT REQUIREMENTS

AI responses must be structured JSON.

Do not rely on free-form text parsing where structured output is possible.

Every recommendation should contain fields such as:

```json
{
  "title": "Improve living room circulation",
  "category": "space",
  "room_id": "living-room",
  "priority": "medium",
  "why_it_matters": "The current furniture arrangement may reduce clear movement space.",
  "recommended_action": "Consider repositioning the coffee table and sofa.",
  "expected_benefit": "Potentially clearer movement and easier cleaning.",
  "effort": "low",
  "estimated_cost": {
    "type": "none",
    "min": 0,
    "max": 0,
    "currency": "USD",
    "is_estimate": true
  },
  "confidence": "medium",
  "assumptions": [
    "Furniture can be moved."
  ],
  "requires_professional_assessment": false
}
```

The exact schema may be improved, but the output must remain predictable and validated.

Do not expose internal reasoning traces.

Provide concise user-facing explanations.

---

# 36. AI SAFETY AND LIMITATIONS

The application must clearly communicate that:

* AI recommendations are informational.
* Measurements may be approximate.
* Energy estimates are not utility-grade calculations.
* Security guidance is not a professional security assessment.
* Maintenance suggestions do not replace qualified professionals.
* Accessibility suggestions do not replace an accessibility assessment.
* Structural, electrical, gas, fire, or major construction work requires qualified professionals.
* Users should verify local regulations and building requirements.

Do not provide dangerous instructions.

Do not make unsupported claims about:

* Guaranteed energy savings
* Guaranteed security
* Structural safety
* Exact engineering compliance
* Medical or psychological benefits
* Exact property value increases

---

# 37. ERROR HANDLING

If the AI service fails, show a polished message:

```text
We couldn't complete your home analysis right now.

Your saved home information is still available.
Please try again.
```

Do not expose:

* API keys
* Stack traces
* Internal prompts
* Raw provider errors
* Private implementation details

Handle:

* Empty home profiles
* Missing room dimensions
* Invalid furniture data
* API timeouts
* Invalid AI JSON
* Partial agent failures
* Missing optional information

If one optional agent fails, provide a partial report and clearly identify which section could not be completed.

---

# 38. LOADING STATES

Every AI operation needs a contextual loading experience.

Examples:

```text
Preparing your home profile
Mapping your rooms
Reviewing furniture placement
Analyzing organization opportunities
Checking energy information
Reviewing maintenance details
Prioritizing improvements
Building your home intelligence report
```

Use:

* Progress indicators
* Step labels
* Skeleton states
* Disabled action states
* Retry states
* Partial completion states

Do not use a generic spinner everywhere.

---

# 39. MODALS AND DRAWERS

Create reusable accessible modals or drawers for:

* Add room
* Edit room
* Add furniture
* Add appliance
* Add maintenance item
* Add task
* Analyze home
* Analyze room
* View recommendation details
* Compare scenario
* Delete confirmation
* Feedback
* Contact form

Requirements:

* Escape closes the modal where appropriate
* Clicking outside closes non-critical modals
* Focus states are visible
* Labels are connected to inputs
* Mobile layouts are usable
* Destructive actions require confirmation

---

# 40. TOAST SYSTEM

Create a reusable toast notification system.

Examples:

```text
Room added
Room updated
Furniture added
Appliance saved
Home profile saved
Analysis completed
Recommendation saved
Task created
Task completed
Changes discarded
Feedback submitted
```

Toasts must not replace important inline validation messages.

---

# 41. EMPTY STATES

Create meaningful empty states.

Examples:

```text
Your home model is empty.

Add your first room to begin building your digital home.
```

```text
No recommendations yet.

Complete your home profile and run an analysis to discover opportunities.
```

```text
No tasks yet.

Save a recommendation or create a task to begin your improvement roadmap.
```

Never show a blank page without explanation.

---

# 42. SEARCH, FILTERING, AND SORTING

Implement functional local search where useful.

Search should support:

* Rooms
* Furniture
* Appliances
* Recommendations
* Tasks
* Maintenance items

Filtering and sorting must update the visible interface correctly.

Do not create visual-only controls.

---

# 43. EXPORT AND SHARING

Implement useful export actions where practical:

* Print home intelligence report
* Print room report
* Print task roadmap
* Download structured JSON home profile
* Copy a recommendation summary
* Copy a task list

Do not pretend to send emails or create public cloud links unless that functionality actually exists.

Use browser-native print functionality where appropriate.

---

# 44. ABOUT PAGE

Create:

```text
/about
```

Explain:

* What AI Home Intelligence Hub does
* How the digital home model works
* How recommendations are generated
* Why user-provided data matters
* What the AI can and cannot determine
* How privacy is handled
* Why professional verification is sometimes necessary

Keep the page professional and concise.

---

# 45. FAQ PAGE

Create:

```text
/faq
```

Include questions such as:

```text
How does the home analysis work?
Do I need exact room measurements?
Can I add multiple floors?
Can I edit my home later?
Are energy savings guaranteed?
Can the AI assess structural safety?
Can I save recommendations?
Can I track maintenance?
Is my home data stored permanently?
Can I print my home report?
```

---

# 46. CONTACT PAGE

Create:

```text
/contact
```

Include:

* Name
* Email
* Subject
* Message

For this no-login project, store submissions locally if needed.

Do not pretend submissions were emailed.

Show:

```text
Message received.
```

Validate the form properly.

---

# 47. FOOTER

Create a complete footer.

Example:

```text
AI Home Intelligence Hub

Understand your home.
Improve every space.

Product
Home
Rooms
Insights
Recommendations
Tasks

AI Tools
Analyze Home
Room Intelligence
Scenario Comparison
Maintenance Planner

Company
About
FAQ
Contact

Important
AI limitations
Privacy
Safety guidance

© 2026 AI Home Intelligence Hub
```

---

# 48. PROJECT STRUCTURE

Use a clean structure such as:

```text
ai-home-intelligence-hub/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── pages.py
│   │   ├── home.py
│   │   ├── rooms.py
│   │   ├── insights.py
│   │   ├── recommendations.py
│   │   ├── tasks.py
│   │   ├── ai.py
│   │   └── feedback.py
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── home_validator.py
│   │   ├── space_planning_agent.py
│   │   ├── organization_agent.py
│   │   ├── energy_agent.py
│   │   ├── maintenance_agent.py
│   │   ├── comfort_agent.py
│   │   ├── safety_agent.py
│   │   ├── accessibility_agent.py
│   │   ├── improvement_agent.py
│   │   ├── priority_agent.py
│   │   └── critic_agent.py
│   │
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── home_service.py
│   │   ├── room_service.py
│   │   ├── recommendation_service.py
│   │   ├── task_service.py
│   │   └── json_store.py
│   │
│   ├── models/
│   │   ├── home.py
│   │   ├── room.py
│   │   ├── furniture.py
│   │   ├── appliance.py
│   │   ├── analysis.py
│   │   ├── recommendation.py
│   │   ├── scenario.py
│   │   ├── task.py
│   │   └── feedback.py
│   │
│   ├── data/
│   │   ├── room_types.json
│   │   ├── furniture_catalog.json
│   │   ├── appliance_categories.json
│   │   ├── maintenance_categories.json
│   │   ├── feedback.json
│   │   └── contacts.json
│   │
│   └── utils/
│       ├── validation.py
│       ├── ids.py
│       ├── dates.py
│       └── helpers.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── home.html
│   ├── rooms.html
│   ├── room-detail.html
│   ├── insights.html
│   ├── recommendations.html
│   ├── tasks.html
│   ├── settings.html
│   ├── about.html
│   ├── faq.html
│   ├── contact.html
│   └── 404.html
│
├── static/
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── home.js
│   │   ├── rooms.js
│   │   ├── room-detail.js
│   │   ├── insights.js
│   │   ├── recommendations.js
│   │   ├── tasks.js
│   │   └── settings.js
│   │
│   └── images/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Adapt the structure if the existing project already has a better organization, but maintain clean separation of responsibilities.

---

# 49. ENVIRONMENT

Create:

```text
.env.example
```

with:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Never hardcode API keys.

Add appropriate environment-loading logic.

---

# 50. PERFORMANCE

Optimize the application.

Important requirements:

* Avoid unnecessary AI requests.
* Analyze only the relevant data for room-level operations.
* Filter and sort locally.
* Avoid sending redundant information to the model.
* Cache suitable results during the current session.
* Keep API responses clean.
* Use asynchronous FastAPI operations where appropriate.
* Minimize unnecessary JavaScript.
* Avoid blocking the entire interface during local operations.
* Use lazy rendering for large recommendation lists where practical.
* Prevent duplicate form submissions.
* Handle partial AI failures gracefully.

---

# 51. ACCESSIBILITY

Implement:

* Semantic HTML
* Proper form labels
* Keyboard navigation
* Visible focus states
* Accessible buttons
* Sufficient color contrast
* Alt text for meaningful images
* Accessible dialogs
* Accessible dropdowns
* Accessible tabs where used
* ARIA labels only when necessary
* Clear error messages
* Screen-reader-friendly status updates

Do not rely on color alone to communicate status.

---

# 52. SEO

Implement basic SEO for public pages.

Include:

* Unique page titles
* Meta descriptions
* Descriptive headings
* Open Graph metadata where practical
* Appropriate canonical URLs
* Meaningful page descriptions

Private or session-based home data must not be exposed through public indexing.

---

# 53. IMPORTANT: DO NOT BUILD A FAKE UI

Every major interaction must work.

These must actually work:

```text
Navigation
Home setup
Adding rooms
Editing rooms
Deleting rooms
Adding furniture
Editing furniture
Adding appliances
Editing appliances
Saving home data
Digital floor-plan updates
Home analysis
Room analysis
Recommendation generation
Recommendation filtering
Recommendation sorting
Saving recommendations
Completing recommendations
Creating tasks
Editing tasks
Completing tasks
Scenario comparison
Maintenance tracking
Search
Print
Download
Feedback
Contact form
Responsive mobile navigation
```

Do not create buttons that only visually respond.

Do not use placeholder actions such as:

```text
Coming soon
Demo only
Fake analysis
Static recommendations unrelated to user data
```

---

# 54. QUALITY BAR

The final application must not look like:

```text
A student project
A basic CRUD app
A generic AI chatbot
A template dashboard
A static form collection
A fake digital twin
A collection of disconnected pages
```

It should look like:

```text
A polished intelligent home-management product
with a strong visual identity,
functional home modeling,
useful AI recommendations,
and a premium user experience.
```

Pay special attention to:

* Layout hierarchy
* Typography
* Spacing
* Room visualization
* Form usability
* Recommendation readability
* Empty states
* Loading states
* Error states
* Mobile behavior
* Button states
* Data validation
* Visual consistency
* Meaningful interactions
* Clear AI limitations

---

# 55. FINAL TESTING

Before considering the project complete, test the complete journey:

```text
Home
 ↓
Build My Home
 ↓
Create Home Profile
 ↓
Add Living Room
 ↓
Add Bedroom
 ↓
Add Furniture
 ↓
Add Appliances
 ↓
Set Lifestyle Preferences
 ↓
Add Energy Information
 ↓
Add Maintenance Information
 ↓
Review Home
 ↓
Analyze Home
 ↓
View Intelligence Report
 ↓
Open Room Details
 ↓
View Space Recommendations
 ↓
View Organization Recommendations
 ↓
View Energy Insights
 ↓
View Maintenance Plan
 ↓
Compare Improvement Scenario
 ↓
Save Recommendation
 ↓
Create Task
 ↓
Complete Task
 ↓
Print Report
 ↓
Download Home Profile
 ↓
Submit Feedback
```

Test on:

```text
Desktop
Laptop
Tablet
Mobile
```

Verify:

* No broken routes
* No console errors
* No API-key exposure
* No invalid AI output reaching the UI
* No duplicate submissions
* No fake buttons
* No blank states
* No layout overflow
* No missing mobile interactions
* No lost form data during navigation
* No unsafe or unsupported claims

---

# 56. FINAL REQUIREMENT

Do not stop after creating the initial pages.

Continue implementing until the complete application works end-to-end.

Inspect the existing project before modifying it.

Reuse the existing styles file where appropriate.

Do not ask me to design the UI for you.

You are responsible for making all UI/UX decisions.

Do not wait for a reference website.

Create the visual system yourself.

Use:

```text
Python
FastAPI
Uvicorn
Pydantic
OpenAI Python SDK
Jinja2
HTML
Tailwind CSS
Vanilla JavaScript
GPT-4.1-mini
```

No login or signup.

No unnecessary infrastructure.

The final product must be a **complete AI-powered Home Intelligence Hub**, not a mockup and not a collection of static screens.

Build it to a level where the interface should require **little to no manual UI redesign after implementation**.
