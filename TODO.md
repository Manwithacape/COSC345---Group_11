# To do

## Notes

---

- [ ] Work flows should only run on main

### Must have

- [x] Multi-threading - ensure gui is not frozen on import and photo processing
- [X] Need progress bars for UX - import, detect duplicates, face searching
- [x] Import individual files - currently only does folders
- [x] Refactoring to be done for sidebar contents - exif, score, duplicates viewers. Too much code duplication
- [x] photo_viewer.py & filmstrip_viewer.py to be refactored. Maybe create new dependant file for more code sharing
- [x] Multi file selection within photo_viewer.py
- [ ] Collections management - create collection using selection of files
- [x] Collection viewing - load in replacement for photo_viewer.py and show list of collections
- [ ] ML for photo scores - start with being able to differenciate between good and bad
    - [x] scale the scores and store to normalize them for comparison and merging
    - [x] average relevent scaled scores to calculate photo quality and store on db
    - [ ] add a threshold param for displaying images based on quality
- [x] RAW file handling - take out thumbnails - use any library
- [x] UI beautification - probably some libraries on the internet?
- [x] Make GUI smoother? - seems thats just how tk is ?????
- [x] Show faces in RHS sidebar
- [x] Image viewer - images double clicked in photo_viewer should be shown as a big image. Filmstrip still available, image nav should also be possible through filmstrip
- [x] Image viewer zoom in on click
- [x] Filmstrip needs to be full width of window & collapsable
- [x] Cam Student ID number on report
- [x] Duplicate detection threshold value adjustment
- [ ] Face detection - save to DB
- [ ] Test duplicate detection - maybe run on import? compare each image to prev for better consistency throughout burst
- [ ] Create thumbnails on import, save thumbnails to DB, perform operations on thumbnails rather than full images for better performance
- [ ] Static analysis fixes
- [ ] Face detection accuracy needs improvment - Issue #13
- [x] Scale options for viewing image thumbnails - Issue #15
- [ ] Sidebar faces flexible grid layout? - Issue #14
- [x] Image thumbnail view portrait/landscape/differing aspect ratio handling - Issue #16
- [ ] Full image view only works on some images when multiple are imported? - Issue #17
- [ ] Highlight suggested culls based on score
- [ ] Import validation
- [ ] Collection management - highlight, add, remove photos from collections
- [ ] Filter thumbnail view using exif - date, camera, etc.
- [ ] Create new documentation for current system architecture
- [ ] Set thresholds for good photo
- [ ] Thumbnail highlighting based on photo goodness
- [ ] Show suggested photos for deletion/keeping
- [ ] photo_viewer.py needs slider for scale options in bar @ bottom above filmstrip

---

### Nice to have

- [ ] Histogram
- [ ] EXIF editor
- [ ] Focus peaking
- [ ] Add more things to top menu bar

---
