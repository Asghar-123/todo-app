# Data Model: AI-powered Todo Chatbot

## Entities

### Task

Represents a single todo item managed by the chatbot.

-   **id**: Unique identifier for the task (Primary Key).
-   **description**: Textual content of the task (e.g., "Buy groceries").
-   **due_date**: Optional date when the task is due (can be null).
-   **status**: Current state of the task (e.g., "pending", "completed").
-   **created_at**: Timestamp when the task was created.
-   **updated_at**: Timestamp when the task was last modified.

**Relationships**:
-   Owned by a user (implicit, linked through conversation context/user session).

**Validation Rules**:
-   `description` cannot be empty.
-   `status` must be one of predefined values (e.g., "pending", "completed").
-   `due_date` if provided, must be a valid date format.

### ConversationHistory

Stores the dialogue turns between the user and the chatbot for context and persistence.

-   **id**: Unique identifier for the conversation entry (Primary Key).
-   **user_id**: Identifier for the user associated with the conversation.
-   **message_content**: The actual text of the message (user input or bot response).
-   **message_type**: Indicates if the message is from the "user" or "bot".
-   **timestamp**: When the message was recorded.

**Relationships**:
-   Linked to a user session or user profile.

**Validation Rules**:
-   `user_id` cannot be empty.
-   `message_content` cannot be empty.
-   `message_type` must be either "user" or "bot".
