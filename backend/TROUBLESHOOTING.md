# Troubleshooting Registration Errors

## Quick Checks

1. **Is the backend server running?**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Check the master log file for errors:**
   ```bash
   tail -f backend/logs/app_master.log
   ```

3. **Check browser console for frontend errors:**
   - Open browser DevTools (F12)
   - Check Console tab for detailed error messages
   - Check Network tab to see if requests are reaching the backend

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Verify database exists: `psql -l | grep strategic_futures_db`

### Module Not Found (psycopg2)
- Make sure you're using the virtual environment:
  ```bash
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Server Not Responding
- Check if server is running on port 8000:
  ```bash
  lsof -i :8000
  ```
- Check CORS settings in `backend/app/core/config.py`

## Error Logging

All errors are now logged to:
- **Backend**: `backend/logs/app_master.log` (never deleted)
- **Frontend**: Browser console (F12 → Console tab)

Registration errors will show:
- Email being registered
- Password validation errors
- Database errors with full stack traces
- Token generation errors

