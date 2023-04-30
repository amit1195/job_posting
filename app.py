import streamlit as st
import users as users
import job as job
from datetime import datetime

users = users.users
jobs = job.jobs


def home():
    my_jobs=sorted(jobs, key=lambda x: x['deadline'])
    # st.table(my_jobs)
    for job in jobs:
        card_layout = (
            f"<div style='padding: 10px;background-color:#cceaeb'>"
            f"<h2>title: {job['title']}</h2>"
            f"<p>Description: {job['description']}</p>"
            f"<p>Location: {job['location']}</p>"
            f"<p>Deadline: {job['deadline']}</p>"
            f"<p>Contact: {job['number']} or {job['email']}</p>"
            f"</div>"
        )

        # Display card
        st.markdown(card_layout, unsafe_allow_html=True)


def add():
    title = st.text_input("Title")
    description = st.text_input("description")
    location = st.text_input("location")
    date_str = st.date_input("Select a date")
    time_str = st.time_input("Select a time")
    dt_str = f"{date_str} {time_str}"
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    number = st.text_input("number")
    email = st.text_input("email")

    if st.button("Add"):
        job = {
            "title" : title,
            "description" : description,
            "location" : location,
            "deadline" : str(dt_obj),
            "number" : number,
            "email" : email
        }
        jobs.append(job)

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        if st.button("Sign Up"):
            user = {
                "username": username,
                "password":password
            }
            users.append(user)            
            st.success("Account created successfully")
            # Redirect to home page with query parameter indicating successful signup
            st.experimental_set_query_params(signup_success=True)

def login():
    st.title("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        check = 0
        for user in users:
            # Add logic to check username and password
            if username == user['username'] and password == user['password']:
                st.success("Logged in successfully")
                st.experimental_set_query_params(login_success=True)
                home()
                check=1        
        if check == 0:
            st.error("Invalid username or password")

# Main app code
st.set_page_config(page_title="Login/Signup Example")

# Check for query parameters indicating successful login or signup
query_params = st.experimental_get_query_params()
login_success = query_params.get("login_success")
signup_success = query_params.get("signup_success")

if login_success:
    # Show home page with new sidebar container fields for logged in users
    option = st.sidebar.selectbox("User Options", ("","Add", "logout"))
    if option == "Add":
        add()
    if option == "logout":
        st.experimental_set_query_params(login_success=False)
    st.write("Welcome to the home page, logged in user!")
    home()
else:
    # Show login page by default
    option = st.sidebar.selectbox("Select an option", ("Log In", "Sign Up"))
    if option == "Log In":
        login()
    else:
        signup()


print(users)