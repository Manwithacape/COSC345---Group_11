# File Management, Photos
Perhaps we just store a list of where the program can find the photo and use that path to label pre generated analyitics about the photo. Each Shoot can have its own directory somewhere with lists and probs json files for the feedback.


```
SoftwareFolder/
    ShootName.json,
    SomeOtherShootName.json
    NewYork.json
    DunedinCity.json
```

ShootName.json
```
{
    Shoot_name: "River Shoot",
    Gobal_focus_score: 67,
    global_framing_score: 30,
    global_ai_comment: 20,

    Photos: [
        {
            "path": "some/path.photo",
            "focus_score": 98,
            "framing_score": 30,
            "AI_Comment": "This is a sample photo entry used for demonstration purposes. Replace with actual photo data as needed."
        },
        {
            "path": "some/path.photo",
            "focus_score": 98,
            "framing_score": 30,
            "AI_Comment": "This is a sample photo entry used for demonstration purposes. Replace with actual photo data as needed."
        }
    ]
}
```