# Posture Tracking API

Django APIs for real-time posture tracking, storing spine angle data from wearables or cameras for health applications.

## Features
- Secure APIs for posture data collection
- Real-time spine angle monitoring
- Scalable health tracking

## Prerequisites
- Python 3.8+
- Django 4.2+
- PostgreSQL

## Setup
1. Clone repo:
   ```bash
   git clone https://github.com/yourusername/posture-tracking-api.git
   cd posture-tracking-api
   ```
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env`:
   ```env
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgres://user:password@localhost:5432/posture_db
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start server:
   ```bash
   python manage.py runserver
   ```

## Usage
- APIs at `http://localhost:8000/api/`.
- POST to `/api/posture/`:
   ```bash
   curl -X POST http://localhost:8000/api/posture/ -d '{"spine_angle": 10.5, "status": "Good"}' -H "Authorization: Token your_token"
   ```
- GET logs at `/api/posture/`.

## Contributing
1. Fork repo.
2. Create branch: `git checkout -b feature/your-feature`.
3. Commit: `git commit -m "Add feature"`.
4. Push: `git push origin feature/your-feature`.
5. Submit pull request.

## License
MIT
