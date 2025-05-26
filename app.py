import streamlit as st
from datetime import datetime
import json
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────
JSON_FILE = "output/latest_analysis.json"
BASE_DIR  = Path(__file__).parent

# ─── 1) Bootstrap Suspicious‐Activity in session_state ────────────────────────
if "sus_contacts_names" not in st.session_state:
    st.session_state.sus_contacts_names   = ["Diddy"]
    st.session_state.sus_contacts_numbers = ["+905063661234"]
    st.session_state.sus_times            = ["2025-05-10 14:20:12"]
    st.session_state.flagged_messages     = ["Can you send me numbers behind the vakifbank card"]
    st.session_state.summaries            = ["This contact tried to steal card account by manipulating the child to send the card numbers"]
    st.session_state.evaluation_list      = [[0, 0, 0, 5]]

# ─── 2) Bootstrap Trusted Contacts ─────────────────────────────────────────────
if "trusted_contacts" not in st.session_state:
    st.session_state.trusted_contacts = [
        {"name": "Family", "number": ""},
        {"name": "Mother", "number": ""},
        {"name": "Father", "number": ""},
    ]

# ─── 3) Page Config & Top Row ─────────────────────────────────────────────────
st.set_page_config(page_title="Growing Safely – Parent Dashboard", layout="centered")
col_title, col_refresh = st.columns([9, 1])
with col_title:
    st.title("👪 Growing Safely • Parent Dashboard")
with col_refresh:
    if st.button("🔄 Refresh"):
        try:
            raw_text = (BASE_DIR / JSON_FILE).read_text(encoding="utf-8")
            data = json.loads(raw_text)
            # if it's a list, take first element
            if isinstance(data, list):
                if not data:
                    raise ValueError("JSON list is empty")
                data = data[0]
            # if it's a string, parse it again
            if isinstance(data, str):
                data = json.loads(data)

            # overwrite your 1-contact dummy fields:
            st.session_state.sus_contacts_names   = ["Sabyr"]
            st.session_state.sus_contacts_numbers = ["+998904214104"]
            st.session_state.sus_times            = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]

            # split flagged_messages bullet list into Python list
            raw_flags = data.get("flagged_messages", "")
            st.session_state.flagged_messages = [
                line.lstrip("- ").strip()
                for line in raw_flags.splitlines()
                if line.strip()
            ]

            # single-item summary from JSON
            st.session_state.summaries = [data.get("analysis", "")]

            # leave evaluation_list alone
            st.rerun()

        except FileNotFoundError:
            st.error(f"Could not find `{JSON_FILE}` in this folder.")
        except (json.JSONDecodeError, ValueError) as e:
            st.error(f"Error parsing `{JSON_FILE}`: {e}")

# ─── 4) Suspicious Activity Section ────────────────────────────────────────────
st.header("🔍 Suspicious Activity")
if st.session_state.sus_contacts_names:
    for i, name in enumerate(st.session_state.sus_contacts_names):
        st.markdown(f"**Contact:** `{name}`")
        st.markdown(f"**Number:** `{st.session_state.sus_contacts_numbers[i]}`")
        st.markdown(f"**When:** `{st.session_state.sus_times[i]}`")

        st.markdown("**Flagged message(s):**")
        for msg in st.session_state.flagged_messages:
            st.write(f"- {msg}")

        st.markdown("**Summary of Intent:**")
        st.write(st.session_state.summaries[i])

        cats = ["🧪 Toxicity", "⚠️ Harmfulness", "🔞 Adult Content", "🛑 Phishing"]
        cols = st.columns(len(cats))
        for col, cat, score in zip(cols, cats, st.session_state.evaluation_list[i]):
            col.metric(cat, score)
        st.divider()
else:
    st.info("No suspicious activity is detected.")

# ─── 5) Trusted Contacts Dialogs ───────────────────────────────────────────────
@st.dialog("Contact Details", width="small")
def contact_dialog(idx: int):
    c = st.session_state.trusted_contacts[idx]
    st.subheader(c["name"])
    st.write(f"**Number:** `{c['number'] or '—'}`")
    if st.button("🗑️ Remove contact", key=f"remove_{idx}"):
        st.session_state.trusted_contacts.pop(idx)
        st.rerun()

@st.dialog("Add a New Trusted Contact", width="small")
def add_contact_dialog():
    name_in   = st.text_input("Contact Name")
    number_in = st.text_input("Contact Number (optional)")
    col_a, col_c = st.columns(2)
    if col_a.button("✅ Add"):
        if name_in.strip():
            st.session_state.trusted_contacts.append({
                "name": name_in.strip(),
                "number": number_in.strip()
            })
            st.rerun()
        else:
            st.error("Name cannot be empty.")
    if col_c.button("❌ Cancel"):
        st.rerun()

st.header("🤝 Trusted Contacts")
for idx, c in enumerate(st.session_state.trusted_contacts):
    if st.button(c["name"], key=f"tc_{idx}"):
        contact_dialog(idx)

if st.button("➕ Add Trusted Contact"):
    add_contact_dialog()

# ─── 6) Parent Feedback Section ───────────────────────────────────────────────
st.header("✉️ Parent Feedback")
feedback = st.text_area("Your comments or suggestions:")
if st.button("Send Feedback"):
    if feedback.strip():
        st.success("Thank you! Your feedback has been recorded.")
    else:
        st.error("Please write something before sending.")
