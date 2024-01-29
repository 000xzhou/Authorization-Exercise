- intall
- psycopg2-binary
- flask-sqlalchemy
- flask-wtf
- load_dotenv

## **Part 5: Log out users**

Make routes for the following:

**GET */logout :*** Clear any information from the session and redirect to **_/_**

## **Part 6: Let’s change */secret* to */users/<username>***

Now that we have some logging in and and logging out working. Let’s add some authorization! When a user logs in, take them to the following route:

**GET */users/<username> :*** Display a template the shows information about that user (everything except for their password). You should ensure that only logged in users can access this page.

## **Part 7: Give us some more feedback!**

It’s time to add another model.

Create a **_Feedback_** model for SQLAlchemy. Put this in a **_models.py_** file.

It should have the following columns:

- **_id_** - a unique primary key that is an auto incrementing integer
- **_title_** - a not-nullable column that is at most 100 characters
- **_content_** - a not-nullable column that is text
- **_username_** - a foreign key that references the username column in the users table

## **Part 8: Make/Modify Routes For Users and Feedback**

**GET */users/<username> :*** Show information about the given user. Show all of the feedback that the user has given. For each piece of feedback, display with a link to a form to edit the feedback and a button to delete the feedback. Have a link that sends you to a form to add more feedback and a button to delete the user **Make sure that only the user who is logged in can successfully view this page.**

**POST */users/<username>/delete :*** Remove the user from the database and make sure to also delete all of their feedback. Clear any user information in the session and redirect to **_/_**. **Make sure that only the user who is logged in can successfully delete their account.**

**GET */users/<username>/feedback/add :*** Display a form to add feedback  **Make sure that only the user who is logged in can see this form.**

**POST */users/<username>/feedback/add :*** Add a new piece of feedback and redirect to /users/<username> — **Make sure that only the user who is logged in can successfully add feedback.**

**GET */feedback/<feedback-id>/update :*** Display a form to edit feedback — [\*\*](https://curric.springboard.com/software-engineering-career-track/default/exercises/flask-feedback/index.html#id1)Make sure that only the user who has written that feedback can see this form \*\*

**POST */feedback/<feedback-id>/update :*** Update a specific piece of feedback and redirect to /users/<username> — **Make sure that only the user who has written that feedback can update it.**

**POST */feedback/<feedback-id>/delete :*** Delete a specific piece of feedback and redirect to /users/<username> — **Make sure that only the user who has written that feedback can delete it.**

## **Further Study**

- Make sure your registration and authentication logic is being handled in your **_models.py_**
- Make sure that if there is already a **_username_** in the session, do not allow users to see the register or login forms
- Add a 404 page when a user or feedback can not be found as well as a 401 page when users are not authenticated or not authorized.
- Add a column to the users table called **_is_admin_** which is a boolean that defaults to false. If that user is an admin, they should be able to add, update and delete any feedback for any user as well as delete users.
- Make sure that if any of your form submissions fail, you display helpful error messages to the user about what went wrong.
- Tests! Having tests around authentication and authorization is a great way to save time compared to manually QA-ing your app.
- **Challenge:** Add functionality to reset a password. This will involve learning about sending emails (take a look at the Flask Mail module. You will need to use a transactional mail server to get this to work, gmail is an excellent option) and will require you to add a column to your users table to store a password reset token. **HINT** - here is how that data flow works:
  - A user clicks a link and is taken to a form to input their email
  - If their email exists, send them an email with a link and a unique token in the query string (take a look at the built in **_secrets_** module and the **_token_urlsafe_** function. You will create this unique token and store it in the database.
  - Once the user clicks on that link, take them to a form to reset their password (make sure that the unique token is valid before letting them access this form)
  - Once the form has been submitted, update the password in the database and delete the token created for that user
