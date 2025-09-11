# To do

## Notes

---

### Must have

- [ ] Multi-threading - ensure gui is not frozen on import and proto processing
- [ ] Need progress bars for UX - import, detect duplicates, face searching
- [ ] Import individual files - currently only does folders
- [ ] Face detection - save to DB
- [x] Refactoring to be done for sidebar contents - exif, score, duplicates viewers. Too much code duplication
- [x] photo_viewer.py & filmstrip_viewer.py to be refactored. Maybe create new dependant file for more code sharing
- [ ] Multi file selection within photo_viewer.py
- [ ] Collections management - create collection using selection of files
- [ ] Collection viewing - load in replacement for photo_viewer.py and show list of collections
- [ ] ML for photo scores - start with being able to differenciate between good and bad
- [ ] Create thumbnails on import, save thumbnails to DB, perform operations on thumbnails rather than full images for better performance
- [ ] RAW file handling - take out thumbnails - use any library
- [ ] UI beautification - probably some libraries on the internet?
- [ ] Make GUI smoother?
- [ ] Test duplicate detection - maybe run on import? compare each image to prev for better consistency throughout burst
- [ ] Show faces in RHS sidebar
- [ ] Image viewer - images double clicked in photo_viewer should be shown as a big image. Filmstrip still available, image nav should also be possible through filmstrip
- [ ] Image viewer zoom in on click
- [ ] photo_viewer.py needs slider for scale options in bar @ bottom above filmstrip
- [x] Filmstrip needs to be full width of window & collapsable

---

### Nice to have

- [ ] Histogram
- [ ] EXIF editor
- [ ] Focus peaking
- [ ] Add more things to top menu bar

---
