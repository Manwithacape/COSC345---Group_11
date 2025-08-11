# Notes for program architecture (Roles of each component)

This document should hopefully sufficiently describe the roles of each component which is to make up the AI photo culling/grading/educational application. It will reference the sequence diagram of general use cases. This is only a high level overview of what is probably to happen. This document is only intended to ensure that everyone is on the same page regarding the jobs of each component within the system

## Desktop GUI

Launching this should intitally give splashscreen, and launch into a GUI which shows the collections in a side bar on LHS, images from the selected collection (if any) inthe middle of the screen, and details about the image that has been selected (if any) on the RHS of the screen in a side car

pyEel - Daniel has found a good Python gui thing. Like web dev?

---

## Collections

A collection refers to a collection/selection of photographs. While this can also be referred to as a photoshoot, the word collection is used more commonly in photo editing applications on the market. 

When a user imports images, there is either the option to add to a collection, create a collection, or automatically create a collection with the current data.

---

## Thumbnail generator

On import, thumbnails for each image should be generated and stored within the database. This is to ensure that even in the even that the images are not stored on the computer, it is still possible to use the application in a more basic manner. 

---

## Database

Still TBC? Postgres?

Would have to store:
- Thumbnails
- image metrics
- image faces
- image exif data / metadata
- collections
- *probably more important things*

---

## Scoring engine

This will be some OpenCV black magic. Assuming it wouldn't be too difficult to find something online for face detection, and a solid way to score all the metrics we come up with. This should hopefully be quite well documented somewhere already and ideally not too time consuming to have working as a prototype.

The scoring engine will be heavily relied upon to find the good and bad photos. The metrics should probably be kept flexible and easy to change for easier optimisations further down the line. See last paragraph of Preference model

---

## Preference model

Probably to be the most exciting part of the entire project. This model should already be trained to some degree to recognise what is and isnt a good photo. The user should then be able to refine this model to point it in the direction it would like the model to go in with regards to what is a "good photo". The model should also be able to accept refinements during use e.g., allowing the user to tell it that a photo which has been selected is not actually a good photo. 

It probably also makes sense to have different models which expect their own type of photo e.g., landscapes, portraits, sports, still life, wildlife, etc.

This preference model will likely only look at the metrics computed by the scoring engine to determine how the image is, with no image file input required. This means that the image scoring will need to be quite robust and capable of distinguishing good and bad using the metric scores alone.  

---

## Near-duplicate detection
Should be able to detect when photos look very similar and pick out either the best or least bad. Useful for when there is a burst of photos. Probably done through the OpenCV engine as well. Would have to work out a way to make it store easily within the database. 

---