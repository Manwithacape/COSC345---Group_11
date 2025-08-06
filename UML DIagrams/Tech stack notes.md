# Notes for program architecture (Roles of each component)

This document should hopefully sufficiently describe the roles of each component which is to make up the AI photo culling/grading/educational application. It will reference the sequence diagram of general use cases. This is only a high level overview of what is probably to happen. This document is only intended to ensure that everyone is on the same page regarding the jobs of each component within the system

## Desktop GUI

Launching this should intitally give splashscreen, and launch into a GUI which shows the collections in a side bar on LHS, images from the selected collection (if any) inthe middle of the screen, and details about the image that has been selected (if any) on the RHS of the screen in a side car

---

## Collections

A collection refers to a collection/selection of photographs. While this can also be referred to as a photoshoot, the word collection is used more commonly in photo editing applications on the market. 

When a user imports images, there is either the option to add to a collection, create a collection, or automatically create a collection with the current data.

---

## Thumbnail generator

On import, thumbnails for each image should be generated and stored within the database. This is to ensure that even in the even that the images are not stored on the computer, it is still possible to use the application in a more basic manner. 

---
