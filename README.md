# AI Weather Chart Viewer

An interactive weather forecast viewer that displays ECMWF (European Centre for Medium-Range Weather Forecasts) charts with automatic updates every 6 hours.

## For Users

### Features
- View weather forecast charts for Southeast Asia and Indonesia 
- Navigate between charts using Previous/Next buttons
- Automatic time conversion to Taiwan time
- Charts update every 6 hours
- Easy-to-use interface

### How to Use
1. Open the application in your web browser
2. Use the navigation buttons to view different forecasts:
   - "← 上一張" (Previous)
   - "下一張 →" (Next) 
   - "回到第一張" (Return to First)
3. The current time (Taiwan time) and image count are displayed below each chart
4. New charts are automatically collected every 6 hours

## For Developers

### Technical Challenges and Solutions

#### 1. Dynamic Content Handling
**Challenge:** ECMWF's chart interface uses dynamic loading, requiring robust Selenium handling.

**Solution:**
- Implemented WebDriverWait with explicit conditions
- Added specific CSS selectors for reliable element targeting
- Built retry mechanism with page refresh

#### 2. Image Capture Reliability
**Challenge:** Ensuring complete image capture in dynamic environment.

**Solution:**
- Multiple validation steps before capture
- Added strategic delays
- Implemented element re-fetching

#### 3. Stale Element References
**Challenge:** Elements becoming stale during navigation between forecasts.

**Solution:**
- Element re-fetching strategy
- Page refresh on failure
- Robust error handling

#### 4. Memory Management
**Challenge:** Long-running scraper process leading to memory leaks.

**Solution:**
- Periodic browser restart
- Cleanup of old images
- Resource management through context managers

#### 5. Time Zone Management
**Challenge:** Handling UTC to local time conversion while maintaining accuracy.

**Solution:**
- Structured filename format with UTC time
- Conversion handling in display layer

#### 6. Deployment Considerations
**Challenge:** Running headless browser in production environment.

**Solution:**
- Chrome options optimization
- Error recovery mechanisms
- Resource limitation handling
