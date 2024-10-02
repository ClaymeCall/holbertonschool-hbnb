# Technical Documentation: HBnB Evolution

## Table of Contents
1. [Introduction](#introduction)
2. [General Architecture of the Application](#general-architecture-of-the-application)
   - [Layer Overview](#layer-overview)
   - [Explanation of the Facade Design Pattern](#explanation-of-the-facade-design-pattern)
3. [Class Diagram for the Business Logic Layer](#class-diagram-for-the-business-logic-layer)
   - [Description of the Main Entities](#description-of-the-main-entities)
   - [Relationships between Entities](#relationships-between-entities)
4. [API Call Sequence Diagrams](#api-call-sequence-diagrams)
   - [User Registration](#user-registration)
   - [Place Creation](#place-creation)
   - [Review Submission](#review-submission)
   - [Retrieving a List of Places](#retrieving-a-list-of-places)
5. [Conclusion and Implementation Perspectives](#conclusion-and-implementation-perspectives)

---

## 1. Introduction

The **HBnB Evolution** project is a web application inspired by Airbnb. It allows users to:

- Sign up and manage their profiles (regular users and administrators).
- Create, manage, and associate amenities with rental listings.
- Book places, leave reviews, and read comments from other users.

This documentation describes the **architecture** of the application, the **business logic** governing the main entities (users, places, reviews, reservations), and the **API interactions** via sequence diagrams. The project is organized into **three distinct layers**, each with specific responsibilities to ensure the system’s modularity, maintainability, and scalability.

---

## 2. General Architecture of the Application

The following diagram presents an overview of the application's architecture, which is divided into three main layers: **presentation**, **business logic**, and **persistence**. These layers communicate through the **Facade design pattern**, simplifying interactions between different parts of the system.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/HBnB%20Simple%203%20High-Level%20Architecture%20diagram.png?raw=true" alt="General Architecture Diagram" width="72"/>
</p>

### Layer Overview:

#### Presentation Layer
- **Role**: Interface between the user and the application. Handles API calls for user operations (e.g., registration, login, place creation, review submission).
- **Components**:
  - **API_UserService**: Manages user-related API calls (registration, profile management).
  - **API_PlaceService**: Handles place listings (creation, update, deletion).
  - **API_ReviewService**: Manages reviews for places.
  - **API_AmenityService**: Manages the creation and association of amenities with places.

#### Business Logic Layer
- **Role**: Applies the application's business rules. It processes data from the presentation layer, applies validations, business processes, and returns the results.
- **Components**:
  - **UserService**: Manages operations related to users (creation, deletion, updates).
  - **PlaceService**: Manages place creation and maintenance.
  - **ReviewService**: Manages the submission and maintenance of reviews.
  - **ReservationService**: Handles place reservations.

#### Persistence Layer
- **Role**: Stores and retrieves data from the database. Contains **data models** and **CRUD operations**.
- **Components**:
  - **DataModels**: Represents the entities in the database.
  - **Repositories/DAOs**: Provides interfaces to interact with stored entities.
  - **Database**: The database management system used.

### Explanation of the Facade Design Pattern
The **Facade pattern** allows the **presentation layer** to interact with the **business logic** via a simplified interface. This reduces dependencies and maintains a clear separation between layers.

---

## 3. Class Diagram for the Business Logic Layer

The following diagram describes the **main entities** of the business logic layer and the relationships between them.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/Basic%20class%20Diagram%20for%20Business%20Logic%20Layer.png?raw=true" alt="Class Diagram" width="72"/>
</p>

### Description of the Main Entities:

- **User**: Represents a person using the application. Each user can create **reservations** or **reviews**. They are associated with **places** they book or review.
  
- **Place**: Each place is a listing that users can browse and book. It is linked to **amenities** and a **city**.

- **City** and **Country**: Places are organized into cities, which are themselves located in countries.

- **Amenity**: Represents a feature or service (e.g., Wi-Fi, pool) associated with a place.

- **Review**: Each review is submitted by a user for a place. It includes a rating and a comment.

- **Reservation**: A reservation is made by a user for a place, with start and end dates.

### Relationships between Entities:

- **A user** can create **reservations** and leave **reviews** for places.
- **A place** can have several **amenities** and be reserved by multiple users through **reservations**.
- **A city** is located in a **country**, and **a place** is located in a **city**.

---

## 4. API Call Sequence Diagrams

The sequence diagrams show interactions between layers to process API calls. They highlight the flow of information between the presentation layer (API), business logic layer, and persistence layer (database).

### User Registration

In this use case, the user registers via the API. Here are the steps:

1. **The user** sends a **POST** request to the API to register with their information (name, email, password).
2. **The API** forwards the request to the **business logic**, which verifies the data and applies registration rules.
3. The **business logic** communicates with the **database** to insert a new user record.
4. The **database** confirms the insertion, and this confirmation is passed back to the API via the **business logic**.
5. **The API** sends a confirmation to the user.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/HBnB%20Sequence%20Diagram%201_%20Register%20User.png?raw=true" alt="User Registration Diagram" width="72"/>
</p>

### Place Creation

In this sequence, a user creates a new place listing.

1. The user sends a **POST** request to the API to create a new place, specifying details such as name, description, price, etc.
2. **The API** forwards the request to the **business logic**, which validates the information and applies business rules related to place creation.
3. The **business logic** communicates with the **database** to insert the place details.
4. The **database** confirms the creation of the place to the **business logic**.
5. **The API** sends this confirmation to the user.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/HBnB%20Sequence%20Diagram%202_%20Create%20Reservation9.png?raw=true" alt="Place Creation Diagram" width="72"/>
</p>

### Review Submission

Here, the user submits a review for a place they have visited.

1. The user sends a **POST** request to the API to submit a review, including a rating and a comment.
2. **The API** forwards the request to the **business logic**, which verifies the user is authorized to review the place (e.g., they have booked it).
3. Once validated, the **business logic** inserts the review into the **database**.
4. The **database** confirms the insertion, which is passed back up to the **API**.
5. **The API** sends a success message to the user, confirming the review was submitted.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/HBnB%20Sequence%20Diagram%203_%20Leave%20a%20Review.png?raw=true" alt="Review Submission Diagram" width="72"/>
</p>

### Retrieving a List of Places

In this example, a user retrieves a list of places available in a city.

1. The user sends a **GET** request to the API, specifying the **city ID** as a query parameter.
2. **The API** forwards this request to the **business logic**, which validates the request and applies any filters provided by the user.
3. The **business logic** queries the **database** to retrieve the list of places matching the city ID.
4. The **database** returns the list of places to the **business logic**.
5. **The API** sends the list of places as a response to the user.

<p align="center">
<img src="https://github.com/ClaymeCall/HBnB_project/blob/main/UML/HBnB%20Sequence%20Diagram%204_%20Fetch%20Places%20by%20City.png?raw=true" alt="Fetching Places Diagram" width="72"/>
</p>

---

## 5. Conclusion and Implementation Perspectives

This technical documentation details the architecture, entities, and interaction flows of the **HBnB Evolution** project. It serves as the **primary reference** to guide implementation, ensuring each component adheres to the defined business rules and the application remains scalable.

The next steps involve implementing these components in the codebase, using the diagrams as a guide for the system structure.