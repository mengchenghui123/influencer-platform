Influencer Platform
This project is an Influencer Platform where merchants can post tasks, influencers can apply for tasks, and an administrator oversees the platform’s activities. Each user role (merchant, influencer, and admin) has unique features, which are outlined below.

Usage Guide
This section provides a guide for each user role in the platform: merchants, influencers, and administrators.

Merchant Guide
Merchants can use this platform to post tasks, and mark tasks as completed when work is finished.

1.Register as a Merchant:

Select "Merchant" during registration to gain access to merchant-specific features.

2.Log In:

Use the credentials created at registration to log into your account.

3.Post a Task:

Navigate to the "Post Task" section to create a new task. Fill in all required fields, including title, description, budget, and deadline.
Optionally, upload any file or image attachments.

4.View and Manage Tasks:

Access the "My Posted Tasks" section to view all tasks posted by you.
For available tasks, you can update or delete them.
For tasks with in-progress status, you can mark them as completed.


Influencer Guide
Influencers can apply for tasks posted by merchants and view their application status.

1.Register as an Influencer:

Choose "Influencer" during registration to access influencer-specific features.

2.Log In:

Log in using the credentials created during registration.

3.Browse Tasks:

Go to the "All Tasks" page to view tasks posted by merchants.
You can filter tasks by status (available, in progress, completed) and search by task title or merchant name.

4.Apply for Tasks:

Click "Apply" on tasks that are available to submit your application.
If you have already applied, the system will prevent duplicate applications for the same task.

5.Manage Applications:

In "My Applications," you can view the status of all your task applications.
Cancel an application if you no longer wish to be considered for the task.

Admin Guide
The administrator oversees platform activity, manages user accounts, and has full control over applications for tasks.

1.Admin Login:

Log in with admin credentials provided during the initial setup.

2.Manage Users:

Access the user management section in the admin panel to manage merchant and influencer accounts.
Suspend or delete accounts as necessary.

3.Manage Tasks and Applications:

In the admin panel, view all tasks and applications.
Approve or reject applications from influencers on behalf of the merchant.
When an application is approved, the task status will automatically change to "in progress," and any other applications for the task will be rejected.


API Endpoints
The platform provides the following key API endpoints for use within the application:

Authentication:

/api/login/: User login with token authentication.
/api/register/: User registration.
/api/logout/: Logout and blacklist token.
User Profile:

/api/me/: Get the current user profile.
/api/update-profile/: Update user profile.
Task Management:

/api/tasks/: Retrieve all tasks.
/api/tasks/create/: Create a new task (merchant-only).
/api/tasks/<id>/: Get details of a specific task.
/api/tasks/<id>/update/: Update a task (merchant-only).
/api/tasks/<id>/delete/: Delete a task (merchant-only).
/api/tasks/<id>/mark_completed/: Mark a task as completed (merchant-only).
Task Applications:

/api/tasks/<id>/apply/: Apply for a task (influencer-only).
/api/my-applied-tasks/: View influencer’s applied tasks.
/api/my-posted-tasks/: View merchant’s posted tasks.
/api/task-applications/<id>/: Cancel task application (influencer-only).
Note: All API requests require authentication via an access token, which is provided after login.