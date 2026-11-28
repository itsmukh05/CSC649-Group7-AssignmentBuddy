# Assignment Buddy – Frontend & Integration Test Checklist

**Tester:** Muhammad Farhan Danish bin Mohd Faizal (`farhandnish`)  
**Environment:** Local Streamlit (`http://localhost:8501`) with xAI Grok (`grok-4.3`) + Custom 47-Row CSV Dataset

| Test ID | Feature / Scenario | Steps Performed | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-01 | App Launch & Theme | Run `python -m streamlit run app/app.py` | Light theme loads cleanly with animated blue hero banner and sidebar visible | Pass |
| TC-02 | Backend & Dataset Status | Check sidebar indicators on startup | Green `Backend Live (Grok + CSV)` badge appears and Q&A counter displays `47` | Pass |
| TC-03 | Tabbed Starter Cards | Switch between `Writing`, `Referencing`, and `Study & AI` tabs and click a card | Hover animation triggers, `Question sent!` toast appears, and Grok answers the prompt | Pass |
| TC-04 | Answer Style Selector | Select `Quick Summary`, `Step-by-Step`, and `With Examples` before asking a question | Response format adapts to the selected style | Pass |
| TC-05 | Message Bubble Readability | Send multiple user queries and inspect chat history | User messages show blue-tinted `You` bubbles; bot replies show white bordered `Assignment Buddy` cards | Pass |
| TC-06 | Typing Animation Toggle | Toggle `Typing animation` on and off in the sidebar | Replies stream word-by-word when enabled and appear instantly when disabled | Pass |
| TC-07 | Graceful Exit Command | Type `exit` and `bye` in the chat input bar | Friendly sign-off message appears with reminder to download transcript (no wasted API call) | Pass |
| TC-08 | Export & Clear Session | Click `Download Chat (.txt)` and then `Clear Conversation` | `.txt` transcript downloads properly; chat resets and toast confirms clearing | Pass |