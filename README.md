# Lost and Found Item Tracking Website  

## Overview  
This project is a web-based platform designed to help users report, search, and recover lost and found items efficiently.  

## Features  

### User Authentication  
- **Login and Signup**: Users can create an account or log in using their email credentials and are verified before signing up.  

### User Dashboard  
- Provides an overview of all user posts, interactions, and personal information.  

### Reporting Lost and Found Items  
- **Lost Items**: Users can submit details about their lost items, including description, date, location, and images.  
- **Found Items**: Individuals can report found items with relevant details or match them to existing lost item reports.  

### Searching and Filtering  
- **Search Lost Items**: Users can search the database for lost items using keywords.  
- **Filtered Search**: Apply filters like category, date, and location to refine search results.  

### Listings  
- **Lost Items Listing**: Publicly accessible list of all lost item reports.  
- **Found Items Listing**: Publicly accessible list of all found item reports.  

### Matching and Verification  
- **Automated Matching**: Suggests potential matches between lost and found items based on descriptions and metadata.  
- **Ownership Verification**: Claimants must provide verification (e.g., questionnaire, unique identifiers, proof of purchase) before retrieving items.  

### Post Management  
- Users can add, edit, update status, or delete their item reports.  

### Communication and Fraud Prevention  
- **Chat System**: Enables direct messaging between users to coordinate item returns.  
- **Fraud Alert**: Flags suspicious claims or activities to prevent fraudulent retrievals.  

### Community Engagement  
- **Top Contributor Recognition**: Recognizes and rewards users who frequently report and return items through leaderboards or badges.  
- **Social Media Sharing**: Allows users to share reports on platforms like Facebook and Twitter for increased visibility.  

### Admin Control  
- Admins can oversee reports, manage disputes, and ensure compliance with platform rules.  

## Technologies
- **Frontend**: HTML, CSS, Bootstrap, Jinja2
- **Backend**: Flask, Flask-SocketIO (real-time chat)
- **Database**: PostgreSQL in production (Render), SQLite for local development
- **AI Matching**: Google Gemini embeddings (`gemini-embedding-001`) + cosine similarity

## Getting Started
1. Clone the repository.
2. Create a virtualenv and install dependencies: `pip install -r requirements.txt`
3. Set required environment variables (see below), e.g. via a `.env` file.
4. Run the development server: `python run.py`

### Environment variables
| Variable | Required | Purpose |
|---|---|---|
| `SECRET_KEY` | Yes (unless `FLASK_DEBUG=true`) | Flask session/CSRF signing key. The app refuses to start without it outside debug mode. |
| `FLASK_DEBUG` | No | Set to `true` for local development to enable Flask debug mode and allow an insecure default `SECRET_KEY`. |
| `DATABASE_URL` | No | SQLAlchemy database URI. Defaults to a local `sqlite:///lostandfound.db` if unset. |
| `GOOGLE_API_KEY` | No | Enables AI-based lost/found matching via Gemini embeddings. Matching is disabled without it. |
| `SEED_DEMO_USERS` | No | Set to `true` to seed demo `admin@test.com` / `user@test.com` accounts on startup (local dev only). |
| `DEMO_ADMIN_PASSWORD` / `DEMO_USER_PASSWORD` | No | Override the seeded demo account passwords. |

## Contributing  
University group based work.

## License  
This project is licensed under the [MIT License]().